setlocal EnableDelayedExpansion

set /p msg=Enter message:
git add .
git commit -am "%time:~0,8%-%COMPUTERNAME%-%msg%"
git push
pause