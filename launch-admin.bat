@echo off
cd /d "%~dp0"
echo Installing dependencies if needed...
python -m pip install -r requirements.txt -q
echo.
echo Starting Fake Burg CMS...
echo Open http://127.0.0.1:5050 in your browser
echo Close this window to stop the dashboard.
echo.
python admin.py
pause
