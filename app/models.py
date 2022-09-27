from datetime import timezone
from email.policy import default
from xmlrpc.client import DateTime
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db, login
from sqlalchemy import Integer, String, Column
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

class Note(db.Model):
    id = Column(Integer, primery_key=True)
    data = Column(String(100000))
    date = Column(DateTime(timezone=True), default=func.now())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
