@echo off
echo ========================================
echo    COMPLETE APPOINTMENT SYSTEM FIX
echo ========================================
echo.

cd /d "F:\Aarushi1.0\aarushi_salon_project"

echo [1/3] Running complete fix script...
python complete_fix.py

echo.
echo [2/3] Starting Django server...
echo Please test the website at: http://127.0.0.1:5600/book-appointment/
echo.
echo Press Ctrl+C to stop the server when done testing
echo.

python manage.py runserver 5600

pause
