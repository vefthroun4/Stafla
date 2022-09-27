from flask import url_for, redirect, render_template
from app.blueprints.namsmat import namsmat_bp

# Create routes here
@namsmat_bp.route("/namsmat")
def namsmat():
    return render_template("namsmat.html")