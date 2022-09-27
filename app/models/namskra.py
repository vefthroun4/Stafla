from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app import db


class Schools(db.Model):
    __tablename__ = "Schools"
    schoolID = Column("schoolID", Integer, primary_key=True)
    school_name = Column("schoolName", String(75), unique=True)
    

class Divisions(db.Model):
    __tablename__ = "Divisions"
    division_name = Column("divisionName", String(75), nullable=False, unique=True)
    divisionID = Column("divisionID", Integer, primary_key=True)
    schoolID = Column("schoolID", Integer, ForeignKey("Schools.schoolID"), nullable=False)


class Tracks(db.Model):
    __tablename__ = "Tracks"
    trackID = Column("trackID", String(75), primary_key=True)
    track_name = Column("track_name", String(75), nullable=False)
    divisionID = Column("divisionID", Integer, ForeignKey("Divisions.divisionID"), nullable=False)
    minCredits = Column("minCredits", Integer, nullable=False)


class CourseGroups(db.Model):
    __tablename__ = "CourseGroups"
    groupID = Column("groupID",Integer, primary_key=True)
    num_required = Column("numRequired", Integer, nullable=False)


class Courses(db.Model):
    __tablename__ = "Courses"
    course_number = Column("courseNumber", String(12), primary_key=True)
    course_name = Column("courseName", String(75), nullable=False)
    course_type = Column("courseType", CHAR(4), nullable=False)
    course_credits = Column("courseCredits", TINYINT, default=5)


class Prerequisites(db.Model):
    __tablename__ = "Prerequisites"
    course_number = Column("courseNumber", String(12), ForeignKey("Courses.courseNumber"), primary_key=True)
    prerequisite = Column("prerequisite", String(12), ForeignKey("Courses.courseNumber"), primary_key=True)
    simultaneous = Column("simultaneous", Boolean, default=False)
    

class TrackCourses(db.Model):
    __tablename__ = "TrackCourses"
    trackID = Column("trackID", Integer, ForeignKey("Tracks.TrackID"), primary_key=True)
    groupID = Column("groupID", Integer, ForeignKey("CourseGroups.groupID"), default=None)
    course_number = Column("courseNumber", String(12), ForeignKey("Courses.courseNumber"), primary_key=True)
    is_required = Column("isRequired", Boolean, nullable=False)
    semester = Column("semester", TINYINT, default=None)
    currentlyActive = Column("currentlyActive", Boolean, default=True)

class UsersRegistration(db.Model):
    __tablename__ = "UsersRegistration"
    users_registrationID = Column("usersRegistrationID", Integer, autoincrement=True)
    semester = Column("semester", TINYINT)
    userID = Column("userID", Integer, ForeignKey("User.id"), primary_key=True)
    schoolID = Column("schoolID", Integer, ForeignKey("Schools.schoolID"), primary_key=True)
    divisionID = Column("divisionID", Integer, ForeignKey("Divisions.divisionID"), primary_key=True)
    trackID = Column("trackID", Integer, ForeignKey("Tracks.trackID"), primary_key=True)


class CourseRegistration(db.Model):
    course_number = Column("courseNumber", String(12), ForeignKey("Courses.courseNumber"), primary_key=True)
    users_registrationID = Column("usersRegistrationID", Integer, ForeignKey("UsersRegistration.usersRegistrationID"), primary_key=True)    






