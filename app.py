from flask import Flask, request, jsonify, render_template
import sqlite3
from pathlib import Path
DB=Path(__file__).with_name("orders.db")
app=Flask(__name__)

def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
    c=conn(); c.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT, amount REAL, status TEXT DEFAULT "new", action TEXT)'); c.commit(); c.close()

def automation(amount):
    if amount >= 1000: return "notify_sales_and_request_manager_review"
    if amount >= 300: return "send_priority_confirmation"
    return "send_standard_confirmation"

@app.get("/")
def dashboard():
    init()
    return render_template("dashboard.html")

@app.post("/api/orders")
def add():
    d=request.get_json(force=True)
    customer=str(d.get("customer", "")).strip()
    try: amount=float(d.get("amount", 0))
    except (TypeError, ValueError): return jsonify(error="Invalid amount"),400
    if not customer or amount < 0: return jsonify(error="Customer and a valid amount are required"),400
    action=automation(amount); c=conn(); cur=c.execute("INSERT INTO orders(customer,amount,action) VALUES(?,?,?)",(customer,amount,action)); c.commit(); row=c.execute("SELECT * FROM orders WHERE id=?",(cur.lastrowid,)).fetchone(); c.close(); return jsonify(dict(row)),201

@app.get("/api/orders")
def list_orders():
    c=conn(); rows=c.execute("SELECT * FROM orders ORDER BY id DESC").fetchall(); c.close(); return jsonify([dict(r) for r in rows])

@app.get("/health")
def health(): return jsonify(status="ok")

if __name__ == "__main__":
    init(); app.run(debug=True, port=5002)
