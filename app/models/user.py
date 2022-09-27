from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db, login
from sqlalchemy import Integer, String, Column

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    # Þarf að bæta við userStatus

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

class UserStatus(db.Model):
    user_statusID = Column("userStatusID", Integer, primary_key=True)
    status_name = Column("statusName", String(20), unique=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
