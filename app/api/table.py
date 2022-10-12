from os import abort
from app.api import api_bp
from app.models import TrackCourses, CourseRegistration, UsersRegistration
from flask import request, jsonify, abort
from app.api.errors import resource_not_found
from flask_login import current_user, login_required

@api_bp.route("/table/all", methods=("GET",))
@login_required
def get_all_data():
    " Returns all courses user is not currently taking "
    items_per_page = request.args.get("items_per_page")
    page = request.args.get("page")
    ur = [c.course.course_number for c in UsersRegistration.query.filter_by(userID=current_user.id).first().courses.all()]
    if ur and items_per_page and page:
        results = [c.course.to_json(include_children=True) for c in TrackCourses.query.filter(TrackCourses.course_number.not_in(ur)).paginate(int(page), int(items_per_page), False).items]
        return jsonify(results)
    else:
        tID = UsersRegistration.query.filter_by(userID=current_user.id).first().trackID
        if tID:
            return jsonify(TrackCourses.query.filter_by(trackID=tID))
        else:
            return resource_not_found("Unknown Error")

@api_bp.route("/table/active", methods=("GET",))
@login_required
def get_active_data():
    """ Returns user current courses """
    page = request.args.get("page")
    items_per_page = request.args.get("items_per_page")
    ur = UsersRegistration.query.filter_by(userID=current_user.id)
    if ur:
        if items_per_page and page:
            ur = [c.course.to_json(include_children=True) for c in CourseRegistration.query.filter_by(users_registrationID=ur.first().users_registrationID).paginate(int(page), int(items_per_page), False).items]
        else:
            ur = [c.course.to_json(include_children=True) for c in ur.first().courses.all()]
        return jsonify(ur)     
    return resource_not_found("Resource not found")