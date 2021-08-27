import sqlite3
import re
import datetime
import json
import jsonify

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_restful import Resource, Api
from tempfile import mkdtemp
from helpers import login_required, apology
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.exceptions import InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application and database
app = Flask(__name__)
api = Api(app)
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


# Error handler as was found in pset9
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Form for user to log in
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Deve preencher o campo usuario")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Deve preencher o campo senha")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("usuário ou senha inválidos")

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
            return apology("Campo usuário vazio")

        unique = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(unique) != 0:
            return apology("Nome de usuário já foi usado")

        if password == "" or confirmation == "":
            return apology("Campo senha vazio")

        if password != confirmation:
            return apology("As senhas são diferentes")

        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, password_hash)

        return redirect("/login")


# Form to change user's password
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():

    # Render html to change password
    if request.method == "GET":
        return render_template("change.html")
    else:
        # Get information needed
        username = request.form.get("username")
        currentpassword = request.form.get("currentpassword")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        password_hash = generate_password_hash(confirmation)

        # Error checking
        if username == "":
            return apology("Campo usuário vazio")

        unique = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(unique) != 1:
            return apology("Usuário não encontrado")

        if password == "" or confirmation == "" or currentpassword == "":
            return apology("Campo senha vazio")

        if password != confirmation:
            return apology("As senhas são diferentes")

        # Check if current password is correct
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("currentpassword")):
            return apology("Usuário ou senha inválidos", 403)

        # Update database with new password
        db.execute("UPDATE users SET password = ? WHERE username = ?", password_hash, username)

        return redirect("/")


# Simple log out link
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# Form to add a new client to onboarding
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']
    status = "Aguardando assinatura de documentos"
    date = datetime.datetime.now()
    cpf = name = ""

    if request.method == "POST":

        if not request.form.get("name"):
            return apology("Preencha o nome do cliente")

        if not request.form.get("cpf"):
            return apology("Preencha o CPF do cliente")

        cpf = request.form.get("cpf")
        name = request.form.get("name")

        if not re.search("^[0-9]*", cpf):
            return apology("Preencha o CPF apenas com números")
        elif len(cpf) != 11:
            return apology("Digite apenas os 11 dígitos do CPF")

        rows = db.execute("SELECT * FROM onboarding WHERE (cpf = ?)", cpf)
        if len(rows) != 0:
            return apology("Cliente já existe")

        db.execute("INSERT INTO onboarding (name, cpf, status, username, date) VALUES(?, ?, ?, ?, ?)", name, cpf, status, username, date)

        return redirect("/")

    else:

        return render_template("add.html")


# Main page with clients table. Accepts GET and POST
@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    status = {"Aguardando assinatura de documentos", "Aguardando transferência de recursos", "Gestão de patrimônio ativa"}
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']

    if request.method == "POST":
        excluir = request.form.get("del")
        # Updating client status from database
        if excluir == "nao":
            atualizacao_cliente = request.form.get("status")
            cpf = request.form.get("cpf")
            db.execute("UPDATE onboarding SET status = ? WHERE (cpf = ?)", atualizacao_cliente, cpf)
        # Deleting client from database
        else:
            cpf = request.form.get("cpf")
            db.execute("DELETE FROM onboarding WHERE (cpf = ?)", cpf)

    things = db.execute("SELECT name, cpf, status, username, date FROM onboarding")
    return render_template("onboarding.html", things=things, status=status)


@app.route("/adjust", methods=["GET", "POST"])
@login_required
def adjust():

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']

    if request.method == "POST":
        cpf = request.form.get("cpf")
        current_name = db.execute("SELECT name FROM onboarding WHERE (cpf = ?)", cpf)
        novo_cpf = request.form.get("novocpf")
        novo_nome = request.form.get("name")

        if request.form.get("novocpf") == "":
            novo_cpf = cpf

        if request.form.get("name") == "":
            novo_nome = current_name

        if not request.form.get("cpf"):
            return apology("Preencha o CPF atual do cliente")

        if not re.search("^[0-9]*", cpf):
            return apology("Preencha o CPF apenas com números")
        elif len(cpf) != 11:
            return apology("Digite apenas os 11 dígitos do CPF")

        db.execute("UPDATE onboarding SET name = ? WHERE (cpf = ?)", novo_nome, cpf)
        db.execute("UPDATE onboarding SET cpf = ? WHERE (cpf = ?)", novo_cpf, cpf)
        return redirect("/")
    else:
        return render_template("adjust.html")


    things = db.execute("SELECT name, cpf, status, username, date FROM onboarding")
    return render_template("onboarding.html", things=things, status=status)


@app.route("/api", methods=["GET", "POST", "PUT", "DELETE"])
def api():

    x = db.execute("SELECT name, cpf, status, username, date FROM onboarding")
    x = json.dumps(x)

    if request.method == "GET":
        return x

    elif request.method == "POST":
        # Still have to make it so that if post from api sends a client that already exists, it deletes him
        data = request.json
        username = "API"
        status = "Aguardando assinatura de documentos"
        date = datetime.datetime.now()
        cpf = data["cpf"]
        name = data["name"]

        if name == "":
            return "Preencha o nome do cliente"

        if cpf == "":
            return "Preencha o CPF do cliente"

        if not re.search("^[0-9]*", cpf):
            return "Preencha o CPF apenas com números"
        elif len(cpf) != 11:
            return "Digite apenas os 11 dígitos do CPF"

        rows = db.execute("SELECT * FROM onboarding WHERE (cpf = ?)", cpf)
        if len(rows) != 0:
            return "Cliente já existe"

        db.execute("INSERT INTO onboarding (name, cpf, status, username, date) VALUES(?, ?, ?, ?, ?)", name, cpf, status, username, date)

        return "sucesso"

    elif request.method == "PUT":
        possiveis = ["Aguardando assinatura de documentos", "Aguardando transferência de recursos", "Gestão de patrimônio ativa"]
        data = request.json
        status = data["status"]
        status = possiveis[status]
        cpf = data["cpf"]

        db.execute("UPDATE onboarding SET status = ? WHERE (cpf = ?)", status, cpf)

        return "sucesso"

    elif request.method == "DELETE":
        data = request.json
        cpf = data["cpf"]

        db.execute("DELETE FROM onboarding WHERE (cpf = ?)", cpf)

        return "sucesso"
