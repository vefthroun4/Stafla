from flask import Blueprint 

admin_bp = Blueprint("admin", __name__, template_folder="admin")

from app.blueprints.admin import views