from app.blueprints.admin import admin_bp

# Create routes here
@admin_bp.route("/dashboard")
def dashboard():
    return "dashboard"