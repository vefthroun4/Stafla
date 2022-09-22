from flask import render_template, flash, url_for, request, redirect
from app.models import User
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app.auth import auth
from app.auth.forms import LoginForm

@auth.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)

        next = request.args.get("next")
        # Make sure next is not empty or pointing to another website
        if next is None or url_parse(next).netloc != "":
            return redirect(url_for("home.index"))
        return redirect(next)
    return render_template("auth/login.html", form=form)

@auth.route("/signup", methods=("GET", "POST"))
def register():
    return render_template("auth/signup.html")

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


