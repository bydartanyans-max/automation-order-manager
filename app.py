from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("ORDERS_DB", BASE_DIR / "orders.db"))
PORT = int(os.getenv("PORT", "5002"))

app = Flask(__name__)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0),
                status TEXT NOT NULL DEFAULT 'new',
                action TEXT NOT NULL
            )
            """
        )
        connection.commit()


def choose_automation_action(amount: float) -> str:
    """Route an order to the appropriate business workflow."""
    if amount >= 1000:
        return "notify_sales_and_request_manager_review"
    if amount >= 300:
        return "send_priority_confirmation"
    return "send_standard_confirmation"


def serialize_order(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "customer": row["customer"],
        "amount": row["amount"],
        "status": row["status"],
        "action": row["action"],
    }


@app.get("/")
def dashboard():
    return render_template("dashboard.html")


@app.post("/api/orders")
def create_order():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON body is required"), 400

    customer = str(data.get("customer", "")).strip()
    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify(error="Amount must be a valid number"), 400

    if not customer:
        return jsonify(error="Customer is required"), 400
    if amount < 0:
        return jsonify(error="Amount must be non-negative"), 400

    action = choose_automation_action(amount)

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO orders(customer, amount, action) VALUES (?, ?, ?)",
            (customer, amount, action),
        )
        connection.commit()
        row = connection.execute(
            "SELECT * FROM orders WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()

    return jsonify(serialize_order(row)), 201


@app.get("/api/orders")
def list_orders():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM orders ORDER BY id DESC"
        ).fetchall()
    return jsonify([serialize_order(row) for row in rows])


@app.patch("/api/orders/<int:order_id>")
def update_order_status(order_id: int):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON body is required"), 400

    status = str(data.get("status", "")).strip().lower()
    allowed_statuses = {"new", "processing", "completed", "cancelled"}
    if status not in allowed_statuses:
        return jsonify(
            error=f"status must be one of: {', '.join(sorted(allowed_statuses))}"
        ), 400

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        if existing is None:
            return jsonify(error="Order not found"), 404

        connection.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (status, order_id)
        )
        connection.commit()
        row = connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()

    return jsonify(serialize_order(row))


@app.get("/health")
def health():
    return jsonify(status="ok", service="automation-order-manager")


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
