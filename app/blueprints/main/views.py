from app.blueprints.main import main_bp
from flask_login import current_user
from datetime import datetime
from app import db
from ...models import Permissions

# Runs everytime the user requests a page
@main_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main_bp.app_context_processor
def inject_permissions():
    return dict(Permissions=Permissions)