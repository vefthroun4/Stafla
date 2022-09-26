from flask import Blueprint

namsmat_bp = Blueprint("namsmat", __name__)

from app.blueprints.namsmat import views