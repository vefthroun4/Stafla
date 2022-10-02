import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.db import Database
from config import Config


# Create module instances
db = SQLAlchemy()
database = Database()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"

def create_app():
    app = Flask(__name__)

    # Try to setup instance folder if it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Sets up config file
    config_file = os.environ.get("CONFIG")
    app.config.from_object(config_file or Config)
    

    # Init modules        
    db.init_app(app)
    database.init_app(app, db)
    migrate.init_app(app, db)
    login.init_app(app)


    # Blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.home import home_bp
    from app.blueprints.namskra import namskra_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.errors import error_bp
    from app.auth import auth_bp


    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(namskra_bp, url_prefix="/namskra")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(error_bp)
    

    # Setup for Flask Shell CLI
    from app.cli import setup_commands
    setup_commands(app)


    return app