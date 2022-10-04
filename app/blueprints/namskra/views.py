from flask import url_for, redirect, render_template
from flask import current_app
from app.blueprints.namskra import namskra_bp
from app.auth.forms import NamskraRegisterForm
import json

# Create routes here
@namskra_bp.route("/")
def start():
    form = NamskraRegisterForm()
    return render_template("namskra/start.html", form=form)


@namskra_bp.route("/table")
def namskra():
    data = None
    with open(current_app.instance_path+"\\afangar.json", "r") as f:
        data = json.load(f)
    return render_template("namskra/namskra.html", data=data)