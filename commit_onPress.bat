setlocal EnableDelayedExpansion
for /L %%i in (1,0,2) do (
set /p msg=Enter message:
git add .
git commit -am "%time:~0,8%-%COMPUTERNAME%-%msg%"
git push
timeout /T 1 > nul
pause
)