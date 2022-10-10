from flask import jsonify
from app.api import api_bp
from app.models import Tracks
from .errors import resource_not_found


@api_bp.route("/tracks/all")
def get_tracks():
    return jsonify([track.to_json() for track in Tracks.query.all()])

@api_bp.route("/tracks/<int:trackID>")
def get_track_by_id(trackID):
    track = Tracks.query.filter_by(trackID=trackID).first()
    if track:
        return jsonify(track.to_json())
    return resource_not_found(f"track with id: {trackID} was not found")

@api_bp.route("/tracks/<track_name>")
def get_track_by_name(track_name):
    track = Tracks.query.filter_by(track_name=track_name).first()
    if track:
        return jsonify(track.to_json())
    return resource_not_found(f"track with name: {track_name} was not found")