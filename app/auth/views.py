from flask import render_template, flash, url_for, request
from app.models import User
from flask_login import login_user, logout_user, current_user
from app.auth import auth

@auth.route("/login")
def login():
    return render_template("auth/login.html")

@auth.route("/signup")
def register():
    return render_template("auth/signup.html")

@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        return "Logging out"
    return "Not logged in"


