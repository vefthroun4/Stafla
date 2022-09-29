from flask import url_for, redirect, render_template
from flask import current_app
from app.blueprints.namskra import namskra_bp
import json
# Create routes here
@namskra_bp.route("/")
def namskra():
    gogn = None
    with open(current_app.instance_path+"\\data.json", "r") as f:
        gogn = json.load(f)
    return render_template("namsmat.html", gogn=gogn)