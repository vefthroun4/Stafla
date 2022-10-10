from app.blueprints.errors import error_bp
from flask import render_template

@error_bp.app_errorhandler(404)
def not_found_error(err):
    return render_template("errors/404.html"), 404


@error_bp.app_errorhandler(500)
def internal_error(err):
        return render_template("errors/500.html"), 500