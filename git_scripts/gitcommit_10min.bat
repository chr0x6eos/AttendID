setlocal EnableDelayedExpansion

for /L %%i in (1,0,2) do (
git add .
git commit -am "%time:~0,8%-%COMPUTERNAME%-%USERNAME%"
git push
timeout /T 120 > nul
)