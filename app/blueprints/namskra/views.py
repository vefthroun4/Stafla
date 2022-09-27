from flask import url_for, redirect, render_template
from app.blueprints.namskra import namskra_bp

# Create routes here
@namskra_bp.route("/")
def namskra():
    return render_template("namsmat.html")