from os import abort
from app.api import api_bp
from app.models import TrackCourses, CourseRegistration, UsersRegistration
from flask import request, jsonify, abort
from app.api.errors import resource_not_found
from flask_login import current_user, login_required

#TODO add pagination support
@api_bp.route("/table/all", methods=("GET",))
@login_required
def get_all_data():
    " Returns all courses user is not currently taking "
    ur = [c.course.course_number for c in UsersRegistration.query.filter_by(userID=current_user.id).first().courses.all()]
    if ur:
        q = [c.course.to_json(include_children=True) for c in TrackCourses.query.filter(TrackCourses.course_number.not_in(ur)).all()]
        return jsonify(q)
    else:
        tID = UsersRegistration.query.filter_by(userID=current_user.id).first().trackID
        if tID:
            return jsonify(TrackCourses.query.filter_by(trackID=tID))
        else:
            return resource_not_found("Unknown Error")

#TODO add pagination support
@api_bp.route("/table/active", methods=("GET",))
@login_required
def get_active_data():
    """ Returns user current courses """
    urID = request.args.get("id")
    ur = UsersRegistration.query.get(urID)
    if ur:
        ur = [u.to_json() for u in ur.courses]   
        return ur     
    return resource_not_found("Resource not found")