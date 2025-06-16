@echo off
call build.bat
if %errorlevel% neq 0 (
    echo Build failed. Exiting.
    exit /b %errorlevel%
)
call server.bat