from flask import url_for, redirect
from app.blueprints.namsmat import namsmat

# Create routes here
@namsmat.route("/namsmat")
def namsmat():
    return redirect(url_for("home.index"))