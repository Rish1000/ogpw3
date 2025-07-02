@echo off
echo Starting OGPW - AI Network Traffic Analysis Platform
echo.

echo Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Starting backend server...
start "OGPW Backend" cmd /k "python app.py"

echo.
echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

cd ..
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo Starting frontend development server...
npm run dev

pause