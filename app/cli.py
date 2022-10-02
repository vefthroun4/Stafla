# allows db and User objects to be accessed from the "flask shell" command
#TODO Move to another folder specific for CLI commands
from app import db
from app.models import User,  Role
from app.models import \
    Schools, Divisions, Tracks,\
    CourseGroups, Courses, Prerequisites,\
    TrackCourses, UsersRegistration, CourseRegistration
from app.dataparser import DataParser

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
            "CourseRegistration": CourseRegistration  
        }