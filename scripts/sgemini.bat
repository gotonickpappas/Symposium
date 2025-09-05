@echo off
setlocal

rem =================================================================
rem ==        True Interactive Wrapper for Gemini CLI             ==
rem ==   (v4.0 - Correct Interactive Prompt & Manual Control)    ==
rem =================================================================

rem First, capture the arguments for a security check.
set "ARGS=%*"

rem --- SECURITY CHECK ---
rem Block attempts to use absolute paths (C:\) or traverse directories (..)
echo "%ARGS%" | findstr /R /C:"[a-zA-Z]:" /C:"\.\." >nul
if %errorlevel% == 0 (
    echo [SECURITY] Blocked attempt to access outside of the project directory.
    echo [COMMAND] %ARGS%
    exit /b 1
)

rem --- EXECUTION ---
rem This launches the CLI in true interactive mode (-i) and passes
rem the entire initial prompt (%*) as the first command. The user
rem retains full keyboard control for subsequent y/n approvals.
rem The script will HALT here and wait for the user to manually
rem quit the Gemini session before it continues.

gemini -i %*

endlocal