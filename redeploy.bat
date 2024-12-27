@echo off

call build.bat

git add .

git commit --amend --no-edit

git push --force