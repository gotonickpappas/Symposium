@echo off

REM =================================================================
REM ==           Symposium Project Publishing Script             ==
REM ==          (v1.1 - With Progress Indicators)                ==
REM =================================================================

cd /d "%~dp0"

echo.
echo    +----------------------------------------------------+
echo    ^|        Symposium Project Publishing Utility        ^|
echo    +----------------------------------------------------+
echo.

set "commitMessage=%~1"
if not defined commitMessage set "commitMessage=Automated project update"
echo.

REM --- STEP 1: Push to GitHub ---
echo [STEP 1/2] PUSHING CHANGES TO GITHUB
echo -----------------------------------------------------------------
echo   -- Adding all changes to the staging area...
git add .
echo   -- Committing changes with message: "%commitMessage%"
git commit -m "%commitMessage%"
echo   -- Pushing commit to the 'main' branch on 'origin'...
git push origin main
echo [STEP 1/2] COMPLETE
echo.

REM --- STEP 2: Sync to Google Drive ---
echo [STEP 2/2] SYNCING PROJECT TO GOOGLE DRIVE
echo -----------------------------------------------------------------
echo   -- Excluding: .env, .git, __pycache__, symposium_env
rclone sync . "gdrive:Symposium" --exclude "/symposium_env/**" --exclude "/.git/**" --exclude "/__pycache__/**" --exclude ".env" --progress
echo [STEP 2/2] COMPLETE
echo.

echo.
echo    +----------------------------------------------------+
echo    ^|      PUBLISH COMPLETE - CONTEXT IS NOW SHARED      ^|
echo    +----------------------------------------------------+
echo.