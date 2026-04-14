from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "salon.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_: Any) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = sqlite3.connect(DB_PATH)
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()
    db.close()


@app.route("/")
def home() -> str:
    db = get_db()
    services = db.execute(
        "SELECT id, name, duration_minutes, price_usd FROM services ORDER BY price_usd"
    ).fetchall()

    next_bookings = db.execute(
        """
        SELECT b.id, b.client_name, b.phone, b.appointment_date, b.appointment_time,
               s.name AS service_name, s.price_usd
        FROM bookings b
        JOIN services s ON s.id = b.service_id
        ORDER BY b.appointment_date, b.appointment_time
        LIMIT 10
        """
    ).fetchall()

    return render_template("index.html", services=services, bookings=next_bookings)


@app.route("/book", methods=["GET", "POST"])
def book() -> str:
    db = get_db()
    services = db.execute(
        "SELECT id, name, duration_minutes, price_usd FROM services ORDER BY name"
    ).fetchall()

    if request.method == "POST":
        client_name = request.form.get("client_name", "").strip()
        phone = request.form.get("phone", "").strip()
        service_id = request.form.get("service_id", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()
        notes = request.form.get("notes", "").strip()

        if not all([client_name, phone, service_id, appointment_date, appointment_time]):
            flash("Please fill in all required fields.", "error")
            return render_template("book.html", services=services)

        db.execute(
            """
            INSERT INTO bookings (client_name, phone, service_id, appointment_date, appointment_time, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (client_name, phone, service_id, appointment_date, appointment_time, notes),
        )
        db.commit()
        flash("Booking created successfully!", "success")
        return redirect(url_for("home"))

    return render_template("book.html", services=services)


@app.route("/admin")
def admin() -> str:
    db = get_db()
    bookings = db.execute(
        """
        SELECT b.id, b.client_name, b.phone, b.appointment_date, b.appointment_time,
               b.notes, b.created_at, s.name AS service_name, s.price_usd
        FROM bookings b
        JOIN services s ON s.id = b.service_id
        ORDER BY b.appointment_date, b.appointment_time
        """
    ).fetchall()
    return render_template("admin.html", bookings=bookings)


@app.post("/booking/<int:booking_id>/delete")
def delete_booking(booking_id: int) -> str:
    db = get_db()
    db.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    db.commit()
    flash("Booking deleted.", "success")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
