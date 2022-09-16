from flask import Blueprint

admin = Blueprint("admin", __name__, template_folder="admin")

from app.blueprints.admin import admin