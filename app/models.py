from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, Boolean, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, MEDIUMINT
from app import db, login
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Permissions:
    ANONYMOUS = 1
    USER = 2
    MODERATOR = 4
    ADMIN = 8
    roles = {
            "Anonymous" : [ANONYMOUS],
            "User" : [ANONYMOUS, USER],
            "Moderator":  [ANONYMOUS, USER, MODERATOR],
            "Admin":  [ANONYMOUS, USER, MODERATOR, ADMIN]
        }

class Role(db.Model):
    __tablename__ = "Role"
    id = Column(Integer, primary_key = True)
    name = Column(String(32), unique=True)
    permissions = Column(Integer)
    default = Column(Boolean, default=False, index=True)
    users = relationship("User", back_populates="role", lazy="dynamic")

    # Set staticmethod so this method can be called without initializing the class
    @staticmethod
    def insert_roles():
        roles = Permissions.roles
        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = 0
            for perm in roles[r]:
                role.add_permissions(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permissions(self, perm):
        if not self.has_permissions(perm):
            self.permissions += perm

    def remove_permissions(self, perm):
        if self.has_permissions(perm):
            self.permissions -= perm

    def has_permissions(self, perm):
        """Checks if uses has a certain permission that has been declared in Permissions"""
        return self.permissions & perm == perm


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    last_seen = Column(DateTime, default=datetime.utcnow)
    user_registrations = relationship("UsersRegistration", back_populates="user")
    role_id = Column(Integer, ForeignKey(Role.id))
    role = relationship("Role", back_populates="users")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Sets initial role
        if self.role is None:
            if self.email == current_app.config["ADMIN_EMAIL"]:
                self.role = Role.query.filter_by(name="Admin").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permissions(perm)

    def is_admin(self):
        return self.can(Permissions.ADMIN)

    def __repr__(self):
        return f"<User {self.email}>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False
    
    def is_admin(self):
        return False

login.anonymous_user = AnonymousUser


class Tracks(db.Model):
    __tablename__ = "Tracks"
    trackID = Column("trackID", Integer, primary_key=True)
    track_name = Column("trackName", String(75), nullable=False, unique=True)
    divisionID = Column("divisionID", Integer, ForeignKey("Divisions.divisionID"), nullable=False)
    min_credits = Column("minCredits", Integer, nullable=False)
    max_courses_per_semester = Column("maxCoursesPerSemester", Integer, nullable=False)
    division = relationship("Divisions", back_populates="tracks")
    groups = relationship("CourseGroups", back_populates="track", lazy="dynamic")

    def __repr__(self):
        return f"<Tracks - {self.trackID}: track_name={self.track_name}, division={self.division.division_name}>"


class Divisions(db.Model):
    __tablename__ = "Divisions"
    divisionID = Column("divisionID", Integer, primary_key=True)
    division_name = Column("divisionName", String(75), nullable=False, unique=True)
    schoolID = Column("schoolID", Integer, ForeignKey("Schools.schoolID"), nullable=False)
    tracks = relationship("Tracks", back_populates="division", lazy="joined")
    school = relationship("Schools", back_populates="divisions")

    def __repr__(self):
        return f"<Divisions - {self.divisionID}: division_name={self.division_name}, School={self.school}>"

class Schools(db.Model):
    __tablename__ = "Schools"
    schoolID = Column("schoolID", Integer, primary_key=True)
    abbreviation = Column("abbreviation", String(5), nullable=False)
    school_name = Column("schoolName", String(75), unique=True)
    divisions = relationship("Divisions", back_populates="school", lazy="joined")

    def __repr__(self):
        return f"<Schools - {self.schoolID}: school_name={self.school_name}>"

class Prerequisites(db.Model):
    __tablename__ = "Prerequisites"
    course_number = Column("courseNumber", String(12), ForeignKey("Courses.courseNumber"), primary_key=True, index=True)
    prerequisite =  Column("prerequisite", String(12), ForeignKey("Courses.courseNumber"), primary_key=True, index=True)
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
    
    def __repr__(self):
        return f"<Courses: course_number={self.course_number}, course_name={self.course_name}, course_credits={self.course_credits}>"


class CourseGroups(db.Model):
    __tablename__ = "CourseGroups"
    groupID = Column("groupID",Integer, primary_key=True)
    group_name = Column("groupName", String(30), nullable=False)
    trackID = Column("trackID", Integer, ForeignKey(Tracks.trackID), nullable=False)
    credits_required = Column("creditsRequired", Integer, nullable=False)
    courses = relationship("TrackCourses", back_populates="group")
    track = relationship("Tracks", back_populates="groups")
    __table_args__ = tuple(UniqueConstraint("group_name", "trackID", name="group_track_UQ"))


class TrackCourses(db.Model):
    __tablename__ = "TrackCourses"
    trackID = Column("trackID", Integer, ForeignKey(Tracks.trackID), primary_key=True)
    groupID = Column("groupID", Integer, ForeignKey("CourseGroups.groupID"), default=None)
    course_number = Column("courseNumber", String(12), ForeignKey(Courses.course_number), primary_key=True)
    mandatory = Column("mandatory", Boolean, nullable=False)
    semester = Column("semester", INTEGER(unsigned=True), default=None)
    is_active = Column("isActive", Boolean, default=True)
    course = relationship("Courses")
    group = relationship("CourseGroups", back_populates="courses")

    def __repr__(self):
        return f"<TrackCourses - {self.trackID}: groupID={self.groupID}, course_number={self.course_number}, mandatory={self.mandatory}, is_active={self.is_active}>"

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
    def __repr__(self):
        return f"<UsersRegistration: userID={self.userID}, user={self.user}, school={self.school}, division={self.division}, track={self.track}>"

class States:
    FAILED = 1
    ACTIVE = 2
    FINISHED = 3
    states = {
        "FAILED": 1,
        "ACTIVE": 2,
        "FINISHED": 3
    }


class CourseState(db.Model):
    course_stateID = Column("courseStateID", Integer, primary_key=True, autoincrement=False)
    name = Column("name", String(24), nullable=False)
    
    @staticmethod
    def insert_states():
        states = States.states
        for state, identifier in states.items():
            db.session.add(CourseState(course_stateID=identifier, name=state))
        db.session.commit()

class CourseRegistration(db.Model):
    __tablename__ = "CourseRegistration"
    course_number = Column("courseNumber", String(12), ForeignKey(Courses.course_number), primary_key=True)
    semester = Column("semester", INTEGER(unsigned=True))
    stateID = Column("state", ForeignKey(CourseState.course_stateID), nullable=False)
    users_registrationID = Column("usersRegistrationID", Integer, ForeignKey(UsersRegistration.users_registrationID), primary_key=True)
    state = relationship("CourseState")
    users_registration = relationship("UsersRegistration", back_populates="courses") 

    def __repr__(self):
        return f"<CourseRegistration: course_number={self.course_number}, semester={self.semester}, users_registrationID={self.users_registrationID}>"   