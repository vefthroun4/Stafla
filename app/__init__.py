from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Try to setup instance folder if it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    return app