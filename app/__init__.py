from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# Blueprints
from app.blueprints.home import home_blueprint

db = SQLAlchemy()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Register bp
    app.register_blueprint(home_blueprint)

    # Try to setup instance folder if it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    db.init_app(app)

    return app