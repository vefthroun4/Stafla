from re import template
from flask import Blueprint

api_bp = Blueprint("api", __name__, template_folder="api")

from app.api import divisions, tracks, schools, test, courses, table