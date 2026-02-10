@echo off
REM FlashMaster Setup Script for Windows

echo ======================================
echo   FlashMaster Setup Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo + Python found
python --version
echo.

REM Install Django
echo Installing Django...
pip install django

if %errorlevel% neq 0 (
    echo X Failed to install Django
    pause
    exit /b 1
)

echo + Django installed successfully
echo.

REM Make migrations
echo Creating database migrations...
python manage.py makemigrations accounts
python manage.py makemigrations flashcards
echo.

REM Apply migrations
echo Applying migrations to database...
python manage.py migrate
echo.

REM Ask if user wants to create a superuser
set /p CREATE_SUPER="Create admin account now? (y/n): "
if /i "%CREATE_SUPER%"=="y" (
    python manage.py createsuperuser
)

echo.
echo ======================================
echo   Setup Complete!
echo ======================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then open your browser to:
echo   http://127.0.0.1:8000
echo.
echo Admin panel:
echo   http://127.0.0.1:8000/admin
echo.
echo Happy studying!
echo.
pause
