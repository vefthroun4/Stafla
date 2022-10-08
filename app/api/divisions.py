from flask import jsonify
from app.models import Divisions
from app.api import api_bp
from .errors import resource_not_found

#TODO implement a way to accept a header that determines what variable is filtered by to avoid making too many routes
@api_bp.route("/divisions/all")
def get_divisions():
    return jsonify([division.to_json() for division in Divisions.query.all()])

@api_bp.route("/divisions/<division_name>", methods=("GET", "POST"))
def get_divisions_by_name(division_name):
    division = Divisions.query.filter_by(division_name=division_name).first()
    if division:
        return jsonify(division.to_json(include_children=True))
    return resource_not_found(f"division with name: {division_name} was not found")

@api_bp.route("/divisions/<int:divisionID>", methods=("GET", "POST"))
def get_divisions_by_id(divisionID):
    division = Divisions.query.filter_by(divisionID=divisionID).first()
    if division:
        return jsonify(division.to_json(include_children=True))
    return resource_not_found(f"division with id: {divisionID} was not found")
