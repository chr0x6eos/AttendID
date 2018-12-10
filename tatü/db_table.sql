create database Visitors;
use Visitors;

create table AttendingVisitors (
	ReadingTime timestamp primary key not null unique,
    Visitors int(3) not null
);

select * from AttendingVisitors;

drop table if exists AttendingVisitors;
drop database if exists Visitors;