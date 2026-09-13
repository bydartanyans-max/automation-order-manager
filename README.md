# Automation Order Manager

A portfolio-ready Flask application demonstrating rule-based business workflow automation. Orders are automatically routed to different actions based on value, similar to lightweight Make/Zapier business rules.

## Features
- Responsive operations dashboard
- Create and list orders
- Automatic workflow selection by order value
- SQLite persistence
- REST API (`POST /api/orders`, `GET /api/orders`)
- Health endpoint (`GET /health`)
- Input validation and clean project structure

## Automation rules
- **Under 300** → standard confirmation
- **300–999.99** → priority confirmation
- **1000+** → notify sales and request manager review

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5002`.

## Stack
Python · Flask · SQLite · HTML · CSS · REST API
