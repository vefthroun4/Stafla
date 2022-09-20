from flask import render_template
from app.blueprints.home import home
from flask import Blueprint, render_template


home = Blueprint("home", __name__, static_folder="static", template_folder="templates")
# Create routes here
@home.route("/")
def index():
    return render_template("home/home.html")