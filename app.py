from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required, apology
import sqlite3
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.exceptions import InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

db = SQL("sqlite:///clients.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Main page. Accepts GET and POST
@app.route("/")
@login_required
def index():

    return render_template("onboarding.html")


# Form for user to log in
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Link to create an account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        password_hash = generate_password_hash(password)

        if username == "":
            return apology("Empty username")

        unique = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(unique) != 0:
            return apology("Username already used")

        if password == "" or confirmation == "":
            return apology("Empty password")

        if password != confirmation:
            return apology("Passwords don't match")

        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, password_hash)

        return redirect("/login")
  


@app.route("/change", methods=["GET", "POST"])    
@login_required
def change():

    return render_template("change.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    return render_template("add.html")


@app.route("/logout", methods=["GET"])
def logout():

    return render_template("login.html")
