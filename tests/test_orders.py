import importlib

import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("ORDERS_DB", str(tmp_path / "orders.db"))

    import app as app_module

    app_module = importlib.reload(app_module)
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["service"] == "automation-order-manager"


def test_automation_rules(client):
    cases = [
        (100, "send_standard_confirmation"),
        (500, "send_priority_confirmation"),
        (1500, "notify_sales_and_request_manager_review"),
    ]

    for amount, expected_action in cases:
        response = client.post(
            "/api/orders",
            json={"customer": f"Customer {amount}", "amount": amount},
        )
        assert response.status_code == 201
        assert response.get_json()["action"] == expected_action


def test_order_status_update(client):
    create = client.post(
        "/api/orders",
        json={"customer": "Example Customer", "amount": 450},
    )
    order_id = create.get_json()["id"]

    update = client.patch(
        f"/api/orders/{order_id}", json={"status": "completed"}
    )
    assert update.status_code == 200
    assert update.get_json()["status"] == "completed"


def test_invalid_amount_is_rejected(client):
    response = client.post(
        "/api/orders",
        json={"customer": "Example Customer", "amount": "not-a-number"},
    )
    assert response.status_code == 400


def test_invalid_status_is_rejected(client):
    create = client.post(
        "/api/orders",
        json={"customer": "Example Customer", "amount": 50},
    )
    order_id = create.get_json()["id"]

    response = client.patch(
        f"/api/orders/{order_id}", json={"status": "unknown"}
    )
    assert response.status_code == 400
