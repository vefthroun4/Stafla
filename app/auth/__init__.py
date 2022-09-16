from flask import Blueprint

auth = Blueprint("auth", __name__, template_folder="auth")

from app.auth import views