import json
from sqlalchemy import exc
from flask import url_for, redirect, render_template
from flask import current_app, flash
from flask_login import current_user
from app.blueprints.namskra import namskra_bp
from app.blueprints.namskra.forms import NamskraRegisterForm
from app.models import UsersRegistration, Schools, Divisions, Tracks
from app import db


# Create routes here
@namskra_bp.route("/", methods=("GET", "POST"))
def start():
    form = NamskraRegisterForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            try: 
                db.session.add(UsersRegistration(
                    userID = current_user.id,
                    schoolID = Schools.query.filter_by(school_name=form.school.data.school_name).first().schoolID,
                    divisionID = Divisions.query.filter_by(division_name=form.division.data.division_name).first().divisionID,
                    trackID = Tracks.query.filter_by(track_name=form.track.data.track_name).first().trackID,
                    current_semester = 1,
                ))
                db.session.commit()
            except exc.IntegrityError:
                # Incase user attempts to register the same track again.
                db.session.rollback()
                flash(f"You have already registered the track {form.track.data.track_name} under your account.")
                return redirect(url_for("namskra.start"))
            flash("Successfully created initial table", category="success")
            return redirect(url_for("namskra.namskra"))
        else:
            #TODO find a way to support anonymous users.
            flash("Logged in users are currently only supported.", category="error")
            return redirect(url_for("auth.login", next=url_for("namskra.start")))
    return render_template("namskra/start.html", form=form)


@namskra_bp.route("/table", methods=("GET", "POST"))
def namskra():
    data = None
    with open(current_app.instance_path+"\\afangar.json", "r") as f:
        data = json.load(f)
    return render_template("namskra/namskra.html", data=data)