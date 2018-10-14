setlocal EnableDelayedExpansion
set /p msg=Enter message:
for /L %%i in (1,0,2) do (
git add .
git commit -am "%time:~0,8%-%COMPUTERNAME%-%msg%"
git push
timeout /T 1 > nul
pause
)