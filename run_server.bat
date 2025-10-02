@echo off
echo ============================================
echo  MoMo SMS API Server - Starting...
echo ============================================
echo.
echo Server will start on http://localhost:8000
echo Use Ctrl+C to stop the server
echo.
echo Valid credentials:
echo   admin:password123
echo   user:momo2024
echo   api:sms_data
echo.
echo ============================================
echo.

REM Try to find Python and start the server
python --version >nul 2>&1
if %errorlevel%==0 (
    echo Using 'python' command
    python api/rest_api.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel%==0 (
    echo Using 'py' command
    py api/rest_api.py
    goto :end
)

echo ERROR: Python not found!
echo Please install Python or ensure it's in your PATH
pause

:end
