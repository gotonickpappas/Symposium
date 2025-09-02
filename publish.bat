@echo off
REM =================================================================
REM ==       Publishes The Symposium to GitHub and Google Drive    ==
REM =================================================================

REM Change the current directory to the script's directory.
cd /d "%~dp0"

REM Prompt for a commit message
echo.
set /p commitMessage="Enter a commit message for this update: "

REM =================================================================
echo.
echo [STEP 1] Pushing changes to GitHub...

REM Add all changes to the staging area
git add .

REM Commit the changes with the provided message
git commit -m "%commitMessage%"

REM Push the commit to the 'main' branch on the remote 'origin'
git push origin main

echo.
echo GitHub push complete.
echo =================================================================
echo.
echo [STEP 2] Syncing project to Google Drive...
echo Excluding .env, .git, __pycache__, and symposium_env...

rclone sync . "gdrive:Symposium" --exclude "/symposium_env/**" --exclude "/.git/**" --exclude "/__pycache__/**" --exclude ".env" --progress

echo.
echo Google Drive sync complete.
echo =================================================================
echo.
echo          PUBLISH COMPLETE - CONTEXT IS NOW SHARED
echo =================================================================
pause