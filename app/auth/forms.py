from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # þarf að bæta við password og submit