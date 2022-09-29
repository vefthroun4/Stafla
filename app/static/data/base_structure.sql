drop database if exists Stafla;

create database Stafla;

use Stafla;

drop table if exists Users, UserStatus;
drop table if exists Schools;
drop table if exists Semesters;
drop table if exists Divisions;
drop table if exists Tracks;
drop table if exists Courses;
drop table if exists Prerequisites;
drop table if exists CourseGroups;
drop table if exists TrackCourses;


create table Schools (
	schoolID int auto_increment,
    schoolName varchar(75),
    constraint schoolName_UQ unique(schoolName),
    constraint school_PK primary key(schoolID)
);

create table Divisions
(
	divisionID int auto_increment,
    divisionName varchar(75) not null,
    schoolID int not null,
    constraint division_PK primary key(divisionID),
    constraint division_school_FK foreign key(schoolID) references Schools(schoolID)
);

create table Tracks
(
	trackID int auto_increment,
    trackName varchar(75),
    divisionID int not null,
    minCredits int not null,
    constraint track_PK primary key(trackID),
    constraint track_division_FK foreign key(divisionID) references Divisions(divisionID)
);

create table courseGroups (
	groupID int auto_increment,
    numRequired int,
    constraint group_PK primary key(groupID)
);

create table Courses (
    courseNumber varchar(12) not null,
    courseName varchar(75) not null,
    courseType char(4) not null,
    courseCredits tinyint default 5,
    constraint course_PK primary key(courseNumber)
);

create table Prerequisites (
	courseNumber varchar(12) not null,
    prerequisite varchar(12) not null,
    simultaneous bool default false,
    constraint prerequisite_PK primary key(courseNumber, prerequisite),
    constraint course_course_FK foreign key(courseNumber) references Courses(courseNumber),
    constraint prerequisite_course_FK foreign key (prerequisite) references Courses(courseNumber)    
);

create table TrackCourses (
	trackID int,
    courseNumber varchar(12),
	required boolean not null,
    semester tinyint default null,
    groupID int default null,
    currentlyActive boolean default true,
    constraint primary key(trackID, courseNumber),
    constraint trackCourses_group foreign key(groupID) references courseGroups(groupID),
	constraint track_course_tracks_FK foreign key(trackID) references Tracks(trackID),
    constraint track_course_courses_FK foreign key(courseNumber) references Courses(courseNumber)
);

create table UserStatus(
	userStatusID int auto_increment,
    statusName varchar(25),
    constraint status_PK primary key(userStatusID),
    constraint status_name_UQ unique(statusName)
);

create table Users(
	userID int auto_increment,
    email varchar(128),
    password_hash varchar(128),
    userStatus int,
    constraint primary key(userID),
    constraint userEmail_UQ unique(email),
    constraint user_status_FK foreign key(userStatus) references UserStatus(userStatusID)
);

create table UsersRegistration (
	usersRegistrationID int auto_increment unique,
    semester tinyint,
	userID int not null,
	schoolID int not null,
    divisionID int not null,
    trackID int not null,
    constraint userRegistration_PK primary key(schoolID, userID, divisionID, trackID),
    constraint usersRegistration_user_FK foreign key(userID) references Users(userID),
    constraint usersRegistration_school_FK foreign key(schoolID) references Schools(schoolID),
    constraint usersRegistration_division_FK foreign key(trackID) references Divisions(divisionID),
    constraint usersRegistration_track_FK foreign key(trackID) references Tracks(trackID)
);

create table courseRegistration (
    courseNumber varchar(12) not null,
    usersRegistrationID int not null,
	constraint courseRegistration_userRegistration_FK foreign key (usersRegistrationID) references UsersRegistration(usersRegistrationID),
    constraint courseRegistration_PK primary key(courseNumber, usersRegistrationID)
);


INSERT INTO Tracks(trackName, divisionID, minCredits) VALUES("abc", 1000, 5)