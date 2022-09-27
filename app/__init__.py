import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

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
    from app.blueprints.namskra import namskra_bp
    from app.blueprints.admin import admin_bp
    from app.auth import auth_bp


    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(namskra_bp, url_prefix="/namskra")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")


    # Init modules        
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)


    # allows db and User objects to be accessed from the "flask shell" command
    #TODO Move to another folder specific for CLI commands
    from app.models import User, UserStatus
    from app.models import \
         Schools, Divisions, Tracks,\
         CourseGroups, Courses, Prerequisites,\
         TrackCourses, UsersRegistration, CourseRegistration

    from app.dataparser import DataParser
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User, "UserStatus":UserStatus,
            "DataParser":DataParser,
            "Schools":Schools, "Divisions":Divisions, 
            "Tracks":Tracks, "CourseGroups":CourseGroups,
            "Courses":Courses, "Prerequisites":Prerequisites,
            "TrackCourses":TrackCourses,
            "UsersRegistration": UsersRegistration,
            "CourseRegistration": CourseRegistration  
        }


    # Checks wheter .db file exists, if not it will create it.
    dbname = re.search("\\\\[A-Z|a-z]+\.db", app.config["SQLALCHEMY_DATABASE_URI"])
    if dbname and not os.path.exists(app.instance_path+dbname.group()):
        with app.app_context():
            db.create_all()

    return app