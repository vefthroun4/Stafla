import json
from operator import and_
from sqlalchemy import exc
from flask import url_for, redirect, render_template
from flask import current_app, flash
from flask_login import current_user, login_required
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
                    divisionID = Divisions.query.filter_by(divisionID=form.division.data).first().divisionID,
                    trackID = Tracks.query.filter_by(trackID = form.track.data).first().trackID,
                    current_semester = 1,
                ))
                db.session.commit()
            except exc.IntegrityError:
                # Incase user attempts to register the same track again.
                db.session.rollback()
                flash(f"You have already registered the track {Tracks.query.filter_by(trackID=form.track.data).first().track_name} under your account.", category="error")
                return redirect(url_for("namskra.namskra"))
            flash("Successfully created initial table", category="success")
            return redirect(url_for("namskra.namskra"))
        else:
            #TODO find a way to support anonymous users.
            flash("Logged in users are currently only supported.", category="error")
            return redirect(url_for("auth.login", next=url_for("namskra.start")))
    return render_template("namskra/start.html", form=form)


@namskra_bp.route("/table", methods=("GET", "POST"))
@login_required
def namskra():
    from sqlalchemy import and_
    from app.models import TrackCourses, CourseGroups
    
    # Get users registration
    ur = UsersRegistration.query.filter_by(userID=current_user.id).first()
    if ur:
        # All courses without a group in the users selected track
        tc = [tc.to_json() for tc in TrackCourses.query.filter(and_(TrackCourses.trackID==ur.trackID, TrackCourses.groupID==None)).order_by(TrackCourses.semester.asc()).all()]
        
        # All courses with a group in the users selected track
        tc_groups = [[a.to_json() for a in c.courses] for c in CourseGroups.query.filter(CourseGroups.trackID==ur.trackID).all()]
        return render_template("namskra/table.html", tc=tc, tc_groups=tc_groups)
    flash("You must create a table first.", category="error")
    return redirect(url_for("namskra.start"))