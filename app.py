from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users.db")

# DB table create (sirf first time)
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username")
    password = request.form.get("password")

    with get_db() as db:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/users")
def users():
    with get_db() as db:
        data = db.execute("SELECT * FROM users").fetchall()

    return render_template("users.html", users=data)

if __name__ == "__main__":
    app.run(debug=True)
