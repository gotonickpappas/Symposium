@echo off
echo Creating MVC folder structure...

REM Backup existing file
if exist symposium_manager.py (
    copy symposium_manager.py symposium_manager_v1.py
    echo Backed up symposium_manager.py to symposium_manager_v1.py
)

REM Create directory structure
mkdir models 2>nul
mkdir models\tools 2>nul
mkdir controllers 2>nul
mkdir views 2>nul

REM Create empty Python files
echo. > models\__init__.py
echo. > models\agent.py
echo. > models\symposium.py
echo. > models\workflow.py
echo. > models\tools\__init__.py
echo. > models\tools\calculator.py
echo. > models\tools\python_executor.py
echo. > models\tools\google_search.py
echo. > controllers\__init__.py
echo. > controllers\orchestrator.py
echo. > controllers\workflow_controller.py
echo. > views\__init__.py
echo. > views\cli.py
echo. > symposium_manager_v2.py

echo.
echo Structure created successfully!
echo.
dir /b /s *.py | findstr /v "__pycache__"