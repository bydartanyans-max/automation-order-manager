# Automation Order Manager ⚙️

A portfolio-ready **Python / Flask business automation application** that demonstrates how incoming orders can be automatically classified and routed through different operational workflows.

The project is inspired by real-world automation tools such as **Make.com** and **Zapier**: instead of manually checking every order, the backend applies business rules and determines the next action automatically.

## 🎯 Business problem

Small businesses often process orders manually. As order volume grows, this creates delays, inconsistent prioritization and missed follow-ups.

This demo shows how a backend service can automatically evaluate an order and assign the appropriate workflow.

## ✨ Features

- Responsive operations dashboard
- Create and list customer orders
- Automatic workflow selection based on order value
- Persistent SQLite storage
- REST API for order creation and retrieval
- Input validation
- Health-check endpoint
- Clean Flask project structure
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

`Python` · `Flask` · `SQLite` · `REST API` · `HTML` · `CSS`

## 🔌 API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/orders` | List orders |
| `POST` | `/api/orders` | Create an order and apply automation rules |
| `GET` | `/health` | Service health check |

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

## 💡 Portfolio focus

This repository demonstrates that I can translate a **business workflow into backend automation logic**, expose the process through REST endpoints and persist operational data.

The next production-level extensions would be webhook support, authentication, role-based access, Docker, automated tests, background jobs and integrations with services such as Shopify, WooCommerce, Telegram, Make.com or Zapier.
