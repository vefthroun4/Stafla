from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms import SelectField, SubmitField
from app.models import Divisions, Schools, Tracks



class NamskraRegisterForm(FlaskForm):
    school = QuerySelectField("School", validators=[DataRequired()], query_factory=Schools.get_all_schools, get_label="school_name", allow_blank=True)
    division = SelectField("Division", choices=[""], validate_choice=False, validators=[DataRequired()])
    track = SelectField("Track", choices=[""], validate_choice=False, validators=[DataRequired()])
    submit = SubmitField("Setup table")

    #TODO validate that division and track belong to their respective school/division
    def validate_school(self, school):
        school = Schools.query.filter_by(school_name=school.data.school_name).first()
        if school is None:
            raise ValidationError("School does not exist.")

    def validate_division(self, division):
        division = Divisions.query.filter_by(divisionID=division.data).first()
        if division is None:
            raise ValidationError("Division does not exist.")

    def validate_track(self, track):
        track = Tracks.query.filter_by(trackID=track.data).first()
        if track is None:
            raise ValidationError("Track does not exist.")

