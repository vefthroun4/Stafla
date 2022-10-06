from app.api import api_bp
from app.models import Schools
from flask import jsonify
from .errors import resource_not_found

@api_bp.route("/schools/all")
def get_schools():
    return jsonify([school.to_json(include_children=True) for school in Schools.query.all()])

@api_bp.route("/schools/<int:schoolID>")
def get_school_by_id(schoolID):
    school = Schools.query.filter_by(schoolID=schoolID).first()
    if school:
       return jsonify(school.to_json(include_children=True))
    return resource_not_found(f"school with id: {schoolID} was not found.")
    

@api_bp.route("/schools/<school_name>")
def get_school_by_name(school_name):
    school = Schools.query.filter_by(school_name=school_name).first()
    if school:
        school = school.to_json(include_children=True)
        return jsonify(school) 
    else:
        return resource_not_found(f"school with name: {school_name} was not found")