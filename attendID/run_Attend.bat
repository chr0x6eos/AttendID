@echo off
set /p class=Enter Class:
set /p students=Enter Students:
set /p debug=Enter debug:

python checkAttendingStudents.py %class% %students% %debug%
pause