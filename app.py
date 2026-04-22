from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "internship_tracker_secret"


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREATE TABLES
# -----------------------------
def create_tables():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            deadline TEXT,
            notes TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


create_tables()


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# REGISTER PAGE
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Username already exists. Please choose another one."
        finally:
            conn.close()

    return render_template("register.html")


# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return "Invalid username or password."

    return render_template("login.html")


# -----------------------------
# DASHBOARD PAGE + SEARCH/FILTER
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")
    status_filter = request.args.get("status", "")

    query = "SELECT * FROM internships WHERE user_id = ?"
    params = [session["user_id"]]

    if search:
        query += " AND (company LIKE ? OR role LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    conn = get_db()
    jobs = conn.execute(query, params).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        jobs=jobs,
        username=session["username"],
        search=search,
        status_filter=status_filter
    )


# -----------------------------
# ADD INTERNSHIP
# -----------------------------
@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    company = request.form["company"]
    role = request.form["role"]
    status = request.form["status"]
    deadline = request.form["deadline"]
    notes = request.form["notes"]

    conn = get_db()
    conn.execute("""
        INSERT INTO internships (company, role, status, deadline, notes, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, role, status, deadline, notes, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# -----------------------------
# UPDATE STATUS
# -----------------------------
@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    if "user_id" not in session:
        return redirect("/login")

    new_status = request.form["status"]

    conn = get_db()
    conn.execute(
        "UPDATE internships SET status = ? WHERE id = ? AND user_id = ?",
        (new_status, id, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# -----------------------------
# DELETE INTERNSHIP
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "DELETE FROM internships WHERE id = ? AND user_id = ?",
        (id, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)