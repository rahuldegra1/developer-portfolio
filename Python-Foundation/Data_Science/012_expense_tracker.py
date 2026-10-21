import os
from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd

app = Flask(__name__)

# Production-ready database pathing
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Adding an 'id' column to keep track of individual rows
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    # Use Pandas to calculate the total spent instantly
    total_spent = df["amount"].sum() if not df.empty else 0.0

    # Convert Pandas DataFrame to a dictionary so HTML can read it easily
    expense_records = df.to_dict("records")

    return render_template("expense.html", expenses=expense_records, total=total_spent)


@app.route("/add", methods=["POST"])
def add():
    desc = request.form.get("description")
    amount = request.form.get("amount")
    category = request.form.get("category")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)",
        (desc, amount, category),
    )
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    # Running on port 5002 to avoid conflicts
    app.run(debug=True, port=5002)
