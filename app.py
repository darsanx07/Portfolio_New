import sqlite3
import os
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "contacts.db")


def init_db():
    """Create the contacts table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            email     TEXT    NOT NULL,
            message   TEXT    NOT NULL,
            submitted_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"success": False, "error": "Please enter a valid email address."}), 400

    submitted_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, message, submitted_at) VALUES (?, ?, ?, ?)",
        (name, email, message, submitted_at)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Message received! I'll be in touch soon."}), 201


@app.route("/api/messages", methods=["GET"])
def messages():
    """Admin endpoint — view all submitted messages."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY submitted_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
