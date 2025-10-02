@echo off
echo Starting MoMo SMS API Server...
echo.

REM Try different Python executables
where python >nul 2>&1
if %errorlevel%==0 (
    echo Using 'python' command
    python api/rest_api.py
    goto :end
)

where python3 >nul 2>&1
if %errorlevel%==0 (
    echo Using 'python3' command
    python3 api/rest_api.py
    goto :end
)

where py >nul 2>&1
if %errorlevel%==0 (
    echo Using 'py' command
    py api/rest_api.py
    goto :end
)

echo Error: Python not found in PATH
echo Please ensure Python is installed and available in PATH
pause

:end
