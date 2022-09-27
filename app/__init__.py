import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DB_Name
from config import Config
from flask_login import LoginManager
from os import path
from datetime import timezone


# Create module instances
db = SQLAlchemy()
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

    # Blueprints
    from app.blueprints.home import home_bp
    from app.blueprints.namsmat import namsmat_bp
    from app.blueprints.admin import admin_bp



    from app.auth import auth_bp


    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(namsmat_bp, url_prefix="/namsmat")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

     


    # Init modules        
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # allows db and User objects to be accessed from the "flask shell" command
    #TODO Move to another folder specific for CLI commands
    from app.models import User
    from app.dataparser import DataParser
    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": User, "DataParser":DataParser}


    from .models import Note

    create_database(app)



    return app

def create_database(app):
    if not path.exists('app/' + DB_Name):
        db.create_all(app=app)
        print('Created Database!')

    