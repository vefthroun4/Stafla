import re
import os
import json
from .utils import clean_str

class Database:
    def __init__(self):
        self.app = None
        self.db = None

    def _setup_initial_state(self):
        # Enforces FK constraints
        from sqlalchemy import event
        with self.app.app_context():    
            @event.listens_for(self.db.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    def _create_database(self):
        # Checks wheter .db file exists, if not it will create it.
        dbname = re.search("\\\\[A-Z|a-z]+\.(db|sqlite)$", self.app.config["SQLALCHEMY_DATABASE_URI"])
        if dbname and not os.path.exists(self.app.instance_path+dbname.group()):
            with self.app.app_context():
                open(os.path.join(self.app.instance_path, "app.db"), "a").close()
                from app.models import Role, CourseState
                # Insert states
                self.db.create_all()
                CourseState.insert_states()
                Role.insert_roles()
                self._insert_initial_data()
                self.db.session.commit()

    def _insert_initial_data(self):
        """ Sets initial database on first time creating a .db file"""
        from app.dataparser import DataParser, TOLVUBRAUT2_URL
        from app.models import Schools, Divisions, Courses, Tracks, Prerequisites, TrackCourses
        from app.models import CourseGroups

        # Create initial data
        # Add a check to not grab data from url if finaldata.json exists
        dp_semester = DataParser(file="app/static/data/semesters.json")
        course_data = DataParser(json_url=TOLVUBRAUT2_URL, output_file="finaldata.json")
        course_data.rename_keys(rename_keys={
            "id" : "course_number",
            "name" : "course_name",
            "parents" : "prerequisites"
        })
        course_data.add_semesters(dp_semester.data, "course_number")
        course_data.write_to_json()
        courses = course_data.data

        # Insert School
        schoolTS = Schools(school_name="T??knisk??linn", abbreviation="TS", active=True)
        self.db.session.add(schoolTS)
        self.db.session.commit()

        # Insert Division
        divisionTS = Divisions(division_name="Uppl??singat??knisk??linn", schoolID=Schools.query.filter_by(school_name="T??knisk??linn").first().schoolID)
        self.db.session.add(divisionTS)
        self.db.session.commit()
        
        # Insert Track
        trackTBR = Tracks(
            track_name = "T??lvubraut", 
            min_credits = 200,
            max_courses_per_semester = 7,
            divisionID = Divisions.query.first().divisionID
        )
        self.db.session.add(trackTBR)
        self.db.session.commit()

        # Insert initial courses

        for course in courses:
            self.db.session.add(
                Courses(
                    course_number      = clean_str(course["course_number"], "()"),
                    course_name        = course["course_name"], 
                    course_description = course["description"],
                    course_type        = course["course_number"][:4:],   # first 4 characters represent course type
                    course_credits     = int(course["course_number"][8]) # 9th character represents credits
                )
            )
        self.db.session.commit()

        # Set prerequisites
        for course in courses:
            if course["prerequisites"]:
                simultaneous = False
                # If able to take course simultaneously with prerequisite
                if course["course_number"] in ["FORK2FE02(AU)"]:
                    simultaneous = True
                for prerequisite in course["prerequisites"]:
                    self.db.session.add(Prerequisites(
                        course_number = clean_str(course["course_number"], "()"),
                        prerequisite  = clean_str(prerequisite, "()"),
                        simultaneous  = simultaneous
                    ))
        self.db.session.commit()
        
        # Insert groups
        track_trackID = trackTBR.trackID

        group =  {
            "courses" : ["??SLE3NB05(CT)", "??SLE3LF05(CT)", "??SLE3BF05(CT)"],
            "credits_required" : 10
        }
        course_group = CourseGroups(
            group_name       = "??slenska300",
            trackID          = track_trackID,
            credits_required = group["credits_required"]
        )

        self.db.session.add(course_group)
        self.db.session.commit()

        # Insert courses into TrackCourses
        for course in courses:
            self.db.session.add(TrackCourses(
                trackID       = track_trackID,
                groupID       = CourseGroups.query.first().groupID,
                course_number = clean_str(course["course_number"], "()"),
                mandatory     = course["core"],
                is_active     = course["active"],
                semester      = course.get("semester"),
            ))
        self.db.session.commit()



    def init_app(self, app, db):
        self.app = app
        self.db = db
        self._setup_initial_state()
        self._create_database()