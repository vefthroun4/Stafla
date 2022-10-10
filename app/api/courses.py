from app.api import api_bp
from app.models import Courses
from flask import jsonify

@api_bp.route("/courses/all")
def get_courses():
    return jsonify([course.to_json(include_children=True) for course in Courses.query.all()])