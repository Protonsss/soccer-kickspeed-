@echo off
REM KickSpeed Pro - Start Script for Windows

echo 🚀 Starting KickSpeed Pro...
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo 📦 Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    echo 📥 Installing Python dependencies...
    pip install -r requirements.txt
    cd ..
) else (
    echo ✅ Python environment found
)

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo 📦 Installing Node.js dependencies...
    cd frontend
    call npm install
    cd ..
) else (
    echo ✅ Node modules found
)

echo.
echo 🎯 Starting services...
echo.

REM Start backend
echo 🔧 Starting Backend API on http://localhost:8000
cd backend
start /B cmd /c "venv\Scripts\activate && python -m app.main"
cd ..

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend
echo 🎨 Starting Frontend on http://localhost:3000
cd frontend
start /B cmd /c "npm run dev"
cd ..

echo.
echo ✨ KickSpeed Pro is running!
echo.
echo 📊 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop

pause

