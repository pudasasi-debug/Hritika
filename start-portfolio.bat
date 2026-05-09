@echo off
cd /d "%~dp0"
if exist server.pid (
    set /p SERVER_PID=<server.pid
    taskkill /PID %SERVER_PID% /F >nul 2>&1
    del server.pid >nul 2>&1
)
start "" cmd /c "timeout /t 2 >nul && start "" http://127.0.0.1:8000/"
py -3 server.py
if errorlevel 1 python server.py
