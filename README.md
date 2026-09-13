# Automation Order Manager ⚙️

A portfolio-ready **Python / Flask business automation application** that demonstrates how incoming orders can be automatically classified, routed and tracked through different operational workflows.

The project is inspired by real-world automation tools such as **Make.com** and **Zapier**: instead of manually checking every order, the backend applies business rules and determines the next action automatically.

## 🎯 Business problem

Small businesses often process orders manually. As order volume grows, this creates delays, inconsistent prioritization and missed follow-ups.

This demo shows how a backend service can automatically evaluate an order, assign the appropriate workflow and update its operational status.

## ✨ Features

- Responsive operations dashboard
- Create and list customer orders
- Automatic workflow selection based on order value
- Update order workflow status through REST API
- Persistent SQLite storage
- Input validation and clear API errors
- Environment-based database and port configuration
- Health-check endpoint
- Automated API tests with `pytest`
- GitHub Actions CI on pushes and pull requests
- Easy foundation for webhooks, email, Telegram, CRM or e-commerce integrations

## 🤖 Automation rules

| Order value | Automated action |
|---|---|
| `< 300` | Standard confirmation |
| `300 – 999.99` | Priority confirmation |
| `1000+` | Notify sales and request manager review |

In a production automation, these actions could trigger integrations such as:

```text
New Shopify / WooCommerce order
        ↓
Flask webhook / REST API
        ↓
Business-rule engine
        ↓
├── Standard confirmation
├── Priority handling
└── Sales / manager notification
        ↓
Email · Telegram · CRM · Make.com · Zapier
```

## 🧰 Tech stack

`Python` · `Flask` · `SQLite` · `REST API` · `HTML` · `CSS` · `pytest` · `GitHub Actions`

## 🔌 API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/orders` | List orders |
| `POST` | `/api/orders` | Create an order and apply automation rules |
| `PATCH` | `/api/orders/<id>` | Update order status |
| `GET` | `/health` | Service health check |

Allowed order statuses:

```text
new · processing · completed · cancelled
```

## ▶️ Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5002
```

## ✅ Run tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

The test suite verifies health checks, automation routing rules, status updates and invalid input handling.

## 🔄 Continuous integration

GitHub Actions automatically runs the test suite whenever code is pushed to `main` or a pull request is opened.

## 💡 Portfolio focus

This repository demonstrates that I can translate a **business workflow into backend automation logic**, expose that workflow through REST APIs, persist operational data and verify the behavior with automated tests.

A production version could add real incoming webhooks, authentication, role-based access, background jobs, Docker and integrations with Shopify, WooCommerce, Telegram, Make.com, Zapier or a CRM.
