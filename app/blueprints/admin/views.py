from flask import render_template
from app.blueprints.admin import admin_bp

# Create routes here
@admin_bp.route("/")
def admin():
    return render_template("admin/admin.html")


@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")