# Allow models to be accessed from flask shell
from app import db
from app.models import User,  Role
from app.models import \
    Schools, Divisions, Tracks,\
    CourseGroups, Courses, Prerequisites,\
    TrackCourses, UsersRegistration, CourseRegistration
from app.dataparser import DataParser
from app.models import States, CourseState

def setup_commands(app):
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User, "Role":Role,
            "DataParser":DataParser,
            "Schools":Schools, "Divisions":Divisions, 
            "Tracks":Tracks, "CourseGroups":CourseGroups,
            "Courses":Courses, "Prerequisites":Prerequisites,
            "TrackCourses":TrackCourses,
            "UsersRegistration": UsersRegistration,
            "CourseRegistration": CourseRegistration,
            "State":States, "CourseState":CourseState   
        }