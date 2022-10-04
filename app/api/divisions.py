from flask import jsonify, request, url_for, current_app
from app.models import Divisions, Schools
from app.api import api_bp

#TODO implement a way to accept a header that determines what variable is filtered by to avoid making too many routes
@api_bp.route("/divisions/<school_name>", methods=("GET", "POST"))
def get_divisions_by_name(school_name):
    """ Returns a given division by the name of a school """

    #TODO implement custom Basequery for filtering by name
    school = Schools.query.filter_by(school_name=school_name).first()
    resp = []
    if school:
        resp = jsonify([division.to_json() for division in Divisions.query.filter_by(schoolID=school.schoolID).all()]) 
    return resp

@api_bp.route("/divisions/<int:schoolID>", methods=("GET", "POST"))
def get_divisions_by_id(schoolID):
    school = Schools.query.get_or_404(schoolID)
    resp = jsonify([division.to_json() for division in Divisions.query.filter_by(schoolID=school.schoolID).all()])
    return resp