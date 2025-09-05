@echo off
setlocal enabledelayedexpansion

REM =================================================================
REM ==        Symposium Project Knowledge Base Updater             ==
REM ==                  (v1.1 - With Progress Indicators)            ==
REM =================================================================

cd /d "%~dp0"

echo.
echo    +----------------------------------------------------+
echo    ^|   Symposium Knowledge Base Update Orchestrator     ^|
echo    +----------------------------------------------------+
echo.

REM --- PREPARATION ---
if not exist update_instructions.txt (
    echo [ERROR] 'update_instructions.txt' not found. Nothing to do.
    pause
    exit /b 1
)
echo [PREP] Instructions file found. The update process will now begin.
echo.
echo.

REM --- STEP 1: AI Execution ---
echo [STEP 1/3] EXECUTING INSTRUCTIONS
echo -----------------------------------------------------------------
echo   -- Tasking Gemini Code to process 'update_instructions.txt'.
echo   -- This may take a moment. Please wait for completion...
echo.
call .\scripts\sgemini.bat "Carefully read the file 'update_instructions.txt' and execute ALL the actions it describes, in order."

if %errorlevel% neq 0 (
    echo.
    echo [FATAL ERROR] AI agent reported an error during execution.
    echo   -- Halting script to prevent inconsistent state.
    echo   -- The 'update_instructions.txt' file will NOT be archived.
    pause
    exit /b 1
)
echo.
echo   -- Gemini Code task complete.
echo [STEP 1/3] COMPLETE
echo.

REM --- STEP 2: Code Snapshot ---
echo [STEP 2/3] GENERATING CODE SNAPSHOT
echo -----------------------------------------------------------------
call python scripts/generate_code_snapshot.py
echo [STEP 2/3] COMPLETE
echo.

REM --- STEP 3: Archiving ---
echo [STEP 3/3] ARCHIVING LOG FILE
echo -----------------------------------------------------------------
for /f %%i in ('python -c "import datetime; print(datetime.datetime.now().strftime('%%Y-%%m-%%d_%%H-%%M-%%S'))"') do set "timestamp=%%i"
set "archive_filename=%timestamp%_update_executed.txt"
set "archive_dir=docs\PastUpdates"

echo   -- Generating timestamp: %timestamp%
echo   -- Preparing to archive instructions as: %archive_filename%

if not exist "%archive_dir%" (
    echo   -- Archive directory not found. Creating '%archive_dir%'...
    mkdir "%archive_dir%"
)

move update_instructions.txt "%archive_dir%\%archive_filename%"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to move and rename the instruction file!
    echo   -- It may be locked by another process.
) else (
    echo   -- Instruction file successfully archived.
)
echo [STEP 3/3] COMPLETE
echo.

echo.
echo    +----------------------------------------------------+
echo    ^|      PROJECT KNOWLEDGE BASE IS NOW SYNCED          ^|
echo    +----------------------------------------------------+
echo.
pause