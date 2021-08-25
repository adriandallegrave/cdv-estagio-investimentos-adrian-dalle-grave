from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required
import sqlite3
from cs50 import SQL

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

    return render_template("layout.html")

@app.route("/login")
def login():

    return render_template("layout.html")

@app.route("/register")
def login():

    return render_template("layout.html")    

