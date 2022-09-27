from flask import Blueprint

namskra_bp = Blueprint("namskra", __name__)

from app.blueprints.namskra import views