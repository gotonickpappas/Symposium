@echo off
setlocal enabledelayedexpansion

REM =================================================================
REM ==        Symposium Project Knowledge Base Updater             ==
REM ==               (v1.5 - With Error Surfacing)                 ==
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

REM --- STEP 1: AI Execution ---
echo [STEP 1/3] EXECUTING INSTRUCTIONS
echo -----------------------------------------------------------------
echo   -> Tasking Claude Code for automated execution.
echo   -> A detailed log is being written to 'claude_run.log'.
echo   -> This may take several moments...

REM Delete the old log and redirect all new output to the log file.
del claude_run.log 2>nul
call .\scripts\sclaude.bat "Carefully read the file 'update_instructions.txt' and execute ALL the actions it describes, in order." > claude_run.log 2>&1

REM ** GROK'S REFINEMENT: Check the exit code AND surface the specific error. **
if %errorlevel% neq 0 (
    echo.
    echo [FATAL ERROR] AI agent reported an error during execution.
    echo   -> The 'update_instructions.txt' file will NOT be archived.
    echo   -> Surfacing relevant error lines from log:
    echo.
    findstr /C:"\"is_error\":true" /C:"\"type\":\"error\"" /C:"ERROR" /I claude_run.log
    echo.
    pause
    exit /b 1
)
echo.
echo   -> Claude Code task complete.
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

echo   -> Generating timestamp: %timestamp%
echo   -> Preparing to archive instructions as: %archive_filename%

if not exist "%archive_dir%" ( mkdir "%archive_dir%" )

move update_instructions.txt "%archive_dir%\%archive_filename%"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to move and rename the instruction file!
) else (
    echo   -> Instruction file successfully archived.
)
echo [STEP 3/3] COMPLETE
echo.

echo.
echo    +----------------------------------------------------+
echo    ^|      PROJECT KNOWLEDGE BASE IS NOW SYNCED          ^|
echo    +----------------------------------------------------+
echo.
pause