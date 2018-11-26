@echo off
set /p action=Enter action:
Python save_faces_proto.py %action%
pause