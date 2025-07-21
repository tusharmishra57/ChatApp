@echo off
echo ========================================
echo   ChatApp - Simple Render Deployment
echo ========================================
echo.

echo [1/4] Backing up current files...
if exist app.py copy app.py app_backup.py >nul
if exist requirements.txt copy requirements.txt requirements_backup.txt >nul
if exist Procfile copy Procfile Procfile_backup >nul

echo [2/4] Using simplified versions...
copy app_simple.py app.py >nul
echo ✓ app.py updated (database-free version)

echo [3/4] Files ready for deployment:
echo ✓ app.py (simplified, no database)
echo ✓ requirements.txt (Python 3.11 compatible)
echo ✓ Procfile (eventlet worker)
echo ✓ runtime.txt (Python 3.11.9)
echo ✓ templates/ (all HTML files)
echo ✓ static/ (CSS, JS, images)

echo [4/4] Ready to push to GitHub:
echo.
echo Run these commands to deploy:
echo   git add .
echo   git commit -m "Simplified for Render deployment"
echo   git push origin main
echo.
echo Then create a Web Service on Render with:
echo   Build Command: pip install -r requirements.txt
echo   Start Command: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
echo.
echo ✅ Deployment files ready!
echo 📖 See SIMPLE_DEPLOY.md for detailed instructions
pause