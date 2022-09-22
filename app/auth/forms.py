from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[EqualTo("password"), DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.get(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use another username.")