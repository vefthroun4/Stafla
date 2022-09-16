from flask import Blueprint

namsmat = Blueprint("namsmat", __name__)

from app.blueprints.namsmat import views