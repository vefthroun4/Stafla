from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, Boolean, DateTime, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, MEDIUMINT
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class UserStatus(db.Model):
    __tablename__ = "UserStatus"
    status_name = Column("statusName", String(20), primary_key=True)


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    last_seen = Column(DateTime, default=datetime.utcnow)
    user_status = Column(Integer, db.ForeignKey(UserStatus.status_name), nullable=False)
    user_registrations = relationship("UsersRegistration", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Tracks(db.Model):
    __tablename__ = "Tracks"
    trackID = Column("trackID", String(75), primary_key=True)
    track_name = Column("trackName", String(75), nullable=False, unique=True)
    divisionID = Column("divisionID", Integer, ForeignKey("Divisions.divisionID"), nullable=False)
    minCredits = Column("minCredits", Integer, nullable=False)
    max_courses_per_semester = Column("maxCoursesPerSemester", Integer(), nullable=False)



class Divisions(db.Model):
    __tablename__ = "Divisions"
    divisionID = Column("divisionID", Integer, primary_key=True)
    division_name = Column("divisionName", String(75), nullable=False, unique=True)
    schoolID = Column("schoolID", Integer, ForeignKey("Schools.schoolID"), nullable=False)
    track = relationship("Tracks", foreign_keys=[Tracks.divisionID], backref=db.backref("division", lazy="joined"))


class Schools(db.Model):
    __tablename__ = "Schools"
    schoolID = Column("schoolID", Integer, primary_key=True)
    school_name = Column("schoolName", String(75), unique=True)
    divisions = relationship("Divisions", foreign_keys=[Divisions.schoolID], backref=db.backref("school", lazy="joined"))  


class Prerequisites(db.Model):
    __tablename__ = "Prerequisites"
    course_number = Column("courseNumber", String(12), ForeignKey("Courses.courseNumber"), primary_key=True)
    prerequisite =  Column("prerequisite", String(12), ForeignKey("Courses.courseNumber"), primary_key=True)
    simultaneous =  Column("simultaneous", Boolean, default=False)
    CheckConstraint(prerequisite != course_number)
    
    def __repr__(self):
        return f"<Prerequisites: courseNumber={self.course_number}, prerequisite={self.prerequisite}>"


class Courses(db.Model):
    __tablename__ = "Courses"
    course_number = Column("courseNumber", String(12), primary_key=True)
    course_name = Column("courseName",   String(75), nullable=False)
    course_description = Column("courseDescription", String(200))
    course_type = Column("courseType", CHAR(4), nullable=False)
    course_credits = Column("courseCredits", INTEGER(unsigned=True), default=5)
    prerequisites = relationship("Prerequisites",
                                foreign_keys=[Prerequisites.course_number],
                                cascade="all, delete-orphan")
    continuations = relationship("Prerequisites", 
                                foreign_keys=[Prerequisites.prerequisite],
                                cascade="all, delete-orphan")


class CourseGroups(db.Model):
    __tablename__ = "CourseGroups"
    groupID = Column("groupID",Integer, primary_key=True)
    track_name = Column("trackName", ForeignKey("Tracks.trackName"), nullable=False)
    courses = relationship("TrackCourses", back_populates="group")
    credits_required = Column("creditsRequired", Integer, nullable=False)


class TrackCourses(db.Model):
    __tablename__ = "TrackCourses"
    trackID = Column("trackID", Integer, ForeignKey(Tracks.trackID), primary_key=True)
    groupID = Column("groupID", Integer, ForeignKey("CourseGroups.groupID"), default=None)
    group = relationship("CourseGroups", back_populates="courses")
    course_number = Column("courseNumber", String(12), ForeignKey(Courses.course_number), primary_key=True)
    courses = relationship("Courses")
    mandatory = Column("mandatory", Boolean, nullable=False)
    semester = Column("semester", INTEGER(unsigned=True), default=None)
    currentlyActive = Column("currentlyActive", Boolean, default=True)


class UsersRegistration(db.Model):
    __tablename__ = "UsersRegistration"
    users_registrationID = Column("usersRegistrationID", Integer, autoincrement=True)
    current_semester = Column("currentSemester", INTEGER(unsigned=True), default=0)
    userID = Column("userID", Integer, ForeignKey(User.id), primary_key=True)
    schoolID = Column("schoolID", Integer, ForeignKey(Schools.schoolID), primary_key=True)
    divisionID = Column("divisionID", Integer, ForeignKey(Divisions.divisionID), primary_key=True)
    trackID = Column("trackID", Integer, ForeignKey(Tracks.trackID), primary_key=True)
    school = relationship("Schools")
    division = relationship("Divisions")
    track = relationship("Tracks")
    user = relationship("User", back_populates="user_registrations")
    # Apply lazy to allow filtering
    courses = relationship("CourseRegistration",
                            back_populates="users_registration", 
                            cascade="all, delete-orphan",
                            lazy="dynamic"
                            )


class CourseRegistration(db.Model):
    __tablename__ = "CourseRegistration"
    course_number = Column("courseNumber", String(12), ForeignKey(Courses.course_number), primary_key=True)
    semester = Column("semester", INTEGER(unsigned=True))
    users_registrationID = Column("usersRegistrationID", Integer, ForeignKey(UsersRegistration.users_registrationID), primary_key=True)
    users_registration = relationship("UsersRegistration", back_populates="courses")    