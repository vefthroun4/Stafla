from flask import Blueprint

home_bp = Blueprint("home", __name__, template_folder="templates")

from app.blueprints.home import views