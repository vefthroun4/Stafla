from app.blueprints.home import home

# Create routes here
@home.route("/")
def index():
    return "index"