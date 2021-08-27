import os
import requests

from flask import redirect, render_template, request, session
from functools import wraps


# Function to redirect users to login page when not logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Renders error messages when needed
def apology(message, code=400):

    return render_template("apology.html", code=code, message=message)
