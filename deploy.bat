@echo off

if "%~1"=="" (
    echo forgot commit message
    exit /b 1
)

call build.bat

git add .

git commit -m %1

git push