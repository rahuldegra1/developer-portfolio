import os
from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd

app = Flask(__name__)

# 1. Absolute Pathing: Forces the DB to always generate in the exact same folder as this Python script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "client_data.db")


# 2. Production Initialization: Builds the database dynamically if Render's hard drive is empty
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes_table (
            Quote TEXT,
            Author TEXT
        )
    """)
    conn.commit()
    conn.close()


# Run the initialization exactly once when Gunicorn boots up
init_db()


@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    # The table is guaranteed to exist now, even if it is empty
    df = pd.read_sql_query("SELECT * FROM quotes_table", conn)
    conn.close()

    # Handle the empty state cleanly so Pandas doesn't crash on an empty table
    if df.empty:
        html_table = (
            "<p style='padding: 15px;'>No data available. Add a record below.</p>"
        )
    else:
        html_table = df.to_html(index=False, border=1)

    return render_template("index.html", table_data=html_table)


@app.route("/add", methods=["POST"])
def add_record():
    new_quote = request.form.get("quote")
    new_author = request.form.get("author")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quotes_table (Quote, Author) VALUES (?, ?)",
        (new_quote, new_author),
    )
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
