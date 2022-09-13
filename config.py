import os
from dotenv import load_dotenv

# Gets absolute path to this file
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY") or "$up3r_dup3r_$3cr3t"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///" + basedir + "\\instance\\app.db" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False