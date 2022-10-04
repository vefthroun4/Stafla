from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from app.models import User, Schools, Divisions
from wtforms_sqlalchemy.fields import QuerySelectField
from app import db

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("ReType Password", validators=[EqualTo("password", "Password must match"), DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use another email.")

# Temporary fix for forms that require information asap
def get_divisions():
    return Divisions.query.all()

def get_schools():
    return Schools.query.all()


class NamskraRegisterForm(FlaskForm):
    school = QuerySelectField("School", validators=[DataRequired()], query_factory=get_schools, get_label="school_name")
    division = QuerySelectField("Divisions", validators=[DataRequired()], query_factory=get_divisions, get_label="division_name")
    semester = SelectField("Current Semester", choices=[n for n in range(1, 4)]) 
    submit = SubmitField("Go away ╰(*°▽°*)╯")

    def validate_school(self, school):
        school = Schools.query.filter_by(school_name=school)
        if school is None:
            raise ValidationError("School does not exist.")

    def validate_division(self, division):
        division = Divisions.query.filter_by(division_name=division)
        if division is None:
            raise ValidationError("Division does not exist.")

