from flask import Blueprint

error_bp = Blueprint("error", __name__, template_folder="errors")

from app.blueprints.errors import views