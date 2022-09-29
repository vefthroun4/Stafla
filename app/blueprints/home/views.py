from flask import render_template
from app.blueprints.home import home_bp

@home_bp.route('/index', methods=['GET', 'POST'])
@home_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")