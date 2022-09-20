from flask import render_template
from app.blueprints.home import home

@home.route('/', methods=['GET', 'POST'])
@home.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")