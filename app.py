from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "internship_tracker_secret"


# XAMPP MySQL settings. The default XAMPP user is root with a blank password.
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "internship_tracker",
}

STATUSES = ["Applied", "Interview", "Offered", "Rejected"]
PASSWORD_HASH_METHOD = "pbkdf2:sha256"


def get_db():
    """Open a new connection to the internship_tracker MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def create_database():
    """Create the database if it does not already exist."""
    config = DB_CONFIG.copy()
    database_name = config.pop("database")

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.close()
    conn.close()


def create_tables():
    """Create the tables used by the app."""
    create_database()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company VARCHAR(150) NOT NULL,
            role VARCHAR(150) NOT NULL,
            status VARCHAR(50) NOT NULL,
            deadline DATE,
            notes TEXT,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def login_required(route_function):
    """Send users to the login page if they are not signed in."""
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)

    return wrapper


def password_is_correct(saved_password, typed_password):
    """Check hashed passwords, plus old plain-text passwords from earlier versions."""
    try:
        if check_password_hash(saved_password, typed_password):
            return True
    except ValueError:
        pass

    return saved_password == typed_password


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password, method=PASSWORD_HASH_METHOD)

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password_hash)
            )
            conn.commit()
        except Error as error:
            if error.errno == 1062:
                flash("Username already exists. Try another one.", "error")
            else:
                flash("Registration failed. Check that MySQL is running.", "error")
            return redirect(url_for("register"))
        finally:
            if "cursor" in locals():
                cursor.close()
            if "conn" in locals() and conn.is_connected():
                conn.close()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and password_is_correct(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            if user["password"] == password:
                new_password_hash = generate_password_hash(password, method=PASSWORD_HASH_METHOD)
                cursor.execute(
                    "UPDATE users SET password = %s WHERE id = %s",
                    (new_password_hash, user["id"])
                )
                conn.commit()

            cursor.close()
            conn.close()

            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))

        cursor.close()
        conn.close()
        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "")

    query = "SELECT * FROM internships WHERE user_id = %s"
    params = [session["user_id"]]

    if search:
        query += " AND (company LIKE %s OR role LIKE %s)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    if status_filter in STATUSES:
        query += " AND status = %s"
        params.append(status_filter)

    query += " ORDER BY deadline IS NULL, deadline, company"

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        jobs=jobs,
        username=session["username"],
        search=search,
        status_filter=status_filter,
        statuses=STATUSES
    )


@app.route("/add", methods=["POST"])
@login_required
def add():
    company = request.form["company"].strip()
    role = request.form["role"].strip()
    status = request.form["status"]
    deadline = request.form["deadline"] or None
    notes = request.form["notes"].strip()

    if not company or not role or status not in STATUSES:
        flash("Company, role, and a valid status are required.", "error")
        return redirect(url_for("dashboard"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO internships
        (company, role, status, deadline, notes, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        company,
        role,
        status,
        deadline,
        notes,
        session["user_id"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Application added.", "success")
    return redirect(url_for("dashboard"))


@app.route("/update_status/<int:internship_id>", methods=["POST"])
@login_required
def update_status(internship_id):
    new_status = request.form["status"]

    if new_status not in STATUSES:
        flash("Choose a valid status.", "error")
        return redirect(url_for("dashboard"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE internships
        SET status = %s
        WHERE id = %s AND user_id = %s
    """, (
        new_status,
        internship_id,
        session["user_id"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Status updated.", "success")
    return redirect(url_for("dashboard"))


@app.route("/delete/<int:internship_id>", methods=["POST"])
@login_required
def delete(internship_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM internships
        WHERE id = %s AND user_id = %s
    """, (
        internship_id,
        session["user_id"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Application deleted.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    try:
        create_tables()
        app.run(debug=True)
    except Error as error:
        print("Could not connect to MySQL.")
        print("Make sure XAMPP MySQL is running and try again.")
        print(f"MySQL error: {error}")
