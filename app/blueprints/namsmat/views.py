from flask import url_for, redirect
from app.blueprints.namsmat import namsmat_bp

# Create routes here
@namsmat_bp.route("/namsmat")
def namsmat():
    return redirect(url_for("home.index"))