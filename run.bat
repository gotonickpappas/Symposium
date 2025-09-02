@echo off
REM =================================================================
REM ==       Runner for The Multi-LLM Symposium                  ==
REM =================================================================

REM Change the current directory to the script's directory.
cd /d "%~dp0"

echo [STEP 1] Activating virtual environment...
call "symposium_env\Scripts\activate.bat"

echo.
echo [STEP 2] Executing the Python script...
python src/symposium_manager_v2.py

echo.
echo =================================================================
echo ==                   SCRIPT FINISHED                           ==
echo =================================================================
pause