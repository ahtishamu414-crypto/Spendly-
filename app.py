import os
import re

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    name_clean = name.strip()
    email_clean = email.strip().lower()

    if not name_clean or not email_clean or not password:
        return render_template("register.html", error="All fields are required.",
                                name=name_clean, email=email_clean), 400

    if not EMAIL_RE.match(email_clean):
        return render_template("register.html", error="Please enter a valid email address.",
                                name=name_clean, email=email_clean), 400

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.",
                                name=name_clean, email=email_clean), 400

    conn = get_db()
    try:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email_clean,)).fetchone()
        if existing is not None:
            return render_template("register.html", error="An account with that email already exists.",
                                    name=name_clean, email=email_clean), 400

        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name_clean, email_clean, password_hash),
        )
        conn.commit()
        user_id = cursor.lastrowid
    finally:
        conn.close()

    session["user_id"] = user_id
    return redirect(url_for("profile"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "")
    password = request.form.get("password", "")

    email_clean = email.strip().lower()

    if not email_clean or not password:
        return render_template("login.html", error="Invalid email or password.",
                                email=email_clean), 400

    conn = get_db()
    try:
        user = conn.execute("SELECT id, password_hash FROM users WHERE email = ?", (email_clean,)).fetchone()
    finally:
        conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.",
                                email=email_clean), 400

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
