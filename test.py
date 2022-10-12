from config import TestingConfig, Config
from app import create_app, db
from app.models import UsersRegistration, CourseRegistration, User
from app.models import Schools, Tracks, Divisions, States
class Testing():

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.ctx = app.app_context()
        self.ctx.push()

    
    def test_CourseRegistration(self):
        [self.db.session.delete(cs) for cs in CourseRegistration.query.all()]
        self.db.session.commit()
        
        try:
            u1 = User(email="asd@asd.com")
            u1.set_password("asd")
            self.db.session.add(u1)
            self.db.session.commit()
            self.db.session.add(UsersRegistration(
                userID = u1.id,
                schoolID= Schools.query.first().schoolID,
                divisionID=Divisions.query.first().divisionID,
                trackID=Tracks.query.first().trackID
            ))
            self.db.session.commit()


        except Exception:
            self.db.session.rollback()
            
        # Insert CR
        self.db.session.add(CourseRegistration(
            course_number="KEST2VW05BU",
            users_registrationID=1,
            semester=4
        ))
        self.db.session.add(CourseRegistration(
            course_number="KEST1VL05AU",
            users_registrationID=1,
            semester=4
        ))
        self.db.session.commit()

        print(CourseRegistration.query.filter_by(
            course_number="KEST2VW05BU",
            users_registrationID=1,
            ).all()
        )



testing = Testing(create_app(Config), db)
testing.test_CourseRegistration()