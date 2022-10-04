from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms import SelectField, SubmitField
from app.models import Divisions, Schools, Tracks


class NamskraRegisterForm(FlaskForm):
    school = QuerySelectField("School", validators=[DataRequired()], query_factory=Schools.get_all_schools, get_label="school_name")
    division = QuerySelectField("Division", validators=[DataRequired()], query_factory=Divisions.get_all_divisions, get_label="division_name")
    track = QuerySelectField("Track", validators=[DataRequired()], query_factory=Tracks.get_all_tracks, get_label="track_name")
    semester = SelectField("Current Semester", choices=[n for n in range(1, 4)]) 
    submit = SubmitField("Setup table")

    def validate_school(self, school):
        school = Schools.query.filter_by(school_name=school)
        if school is None:
            raise ValidationError("School does not exist.")

    def validate_division(self, division):
        division = Divisions.query.filter_by(division_name=division)
        if division is None:
            raise ValidationError("Division does not exist.")

    def validate_semester(self, semester):
        data = None
        try:
            data = int(semester.data)
        except ValueError:
            ValidationError("I have no clue how you triggered this error lol")
        if data < 1 and data > 3:
            raise ValidationError("Semester is not within the range 1 to 3.")