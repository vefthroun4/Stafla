from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="auth")

from app.auth import views