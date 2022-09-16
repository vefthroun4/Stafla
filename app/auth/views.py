from flask import render_template, flash, url_for, request
from app.models import User
from flask_login import login_user, logout_user, current_user
from app.auth import auth

@auth.route("/login")
def login():
    return "login"

@auth.route("/register")
def register():
    return "register"

@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        return "Logging out"
    return "Not logged in"


