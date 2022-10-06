from flask import request
from app.api import api_bp
from flask_login import login_required, current_user
from flask import abort

@api_bp.route("/test")
def test():
    return request.remote_addr
