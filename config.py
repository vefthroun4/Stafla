import os
from dotenv import load_dotenv


# Gets absolute path to this file
basedir = os.path.abspath(os.path.dirname(__file__))

    # Loads environment variables from .env
load_dotenv(os.path.join(basedir, "instance", ".env"))

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY") or "$up3r_dup3r_$3cr3t"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \ 'sqlite:///' + os.path.join(basdir, 'instance','app.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_EMAIL=["asd@asd.com"]

class ProductionConfig(Config):
    ...

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir + "\\instance\\debug.db" 


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://" 
