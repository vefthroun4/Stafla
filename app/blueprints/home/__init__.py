from flask import Blueprint, current_app

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/")
def index():
    return "index"
    