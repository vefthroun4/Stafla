from flask import Blueprint, current_app

home = Blueprint("home", __name__)

from app.blueprints.home import views
    