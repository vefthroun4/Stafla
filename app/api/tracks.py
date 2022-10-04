from flask import jsonify
from app.api import api_bp
from app.models import Tracks, Divisions

@api_bp.route("/tracks/<int:divisionID>", methods=("GET", "POST"))
def get_track_by_id(divisionID):
    division = Tracks.query.get_or_404(divisionID)
    resp = jsonify([track.to_json() for track in Tracks.query.filter_by(divisionID=division.divisionID)])
    return resp

@api_bp.route("/tracks/<division_name>", methods=("GET", "POST"))
def get_track_by_name(division_name):
    division = Divisions.query.filter_by(division_name=division_name).first()
    resp = []
    if division:
        resp = jsonify([track.to_json() for track in Tracks.query.filter_by(divisionID=division.divisionID)])
    return resp