from app.blueprints.admin import admin

# Create routes here
@admin.route("/dashboard")
def dashboard():
    return "dashboard"