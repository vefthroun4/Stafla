from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

# Blueprints
from app.blueprints.home import home_blueprint

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Register blueprints
    app.register_blueprint(home_blueprint)

    # Try to setup instance folder if it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Init modules        
    db.init_app(app)
    migrate.init_app(app, db)

    # allows db and User objects to be accessed from the "flask shell" command
    #TODO Move to another folder specific for CLI commands
    from app.models import User
    @app.shell_context_processor
    def make_shell_context():
        return { "db": db, "User": User }

    return app