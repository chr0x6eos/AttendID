create database Visitors;
use Visitors;

create table AttendingVisitors (
	ReadingTime timestamp primary key not null unique,
    Visitors int(3) not null
);

select * from AttendingVisitors;

drop table if exists AttendingVisitors;
drop database if exists Visitors;

create database attendID;
use attendID;

	create table AttendingStudents(
	ReadingTime TIMESTAMP not null,
    Class VARCHAR(8) not null,
    AttendingStudents INT(3) not null,
    constraint AS_pk primary key(ReadingTime, Class)
);