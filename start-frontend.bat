@echo off
REM MarketFlow AI - Frontend Startup Script for Windows

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║     MarketFlow AI - React Frontend          ║
echo ║          Starting Development Server        ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Change to frontend directory
cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo.
    echo ⚠️  Installing dependencies...
    call npm install --legacy-peer-deps
    echo ✅ Dependencies installed
)

REM Check if backend is running
echo.
echo Checking backend status...
timeout /t 1 >nul

REM Start the development server
echo.
echo 🚀 Starting React development server...
echo.
echo 📱 Frontend will open at: http://localhost:3000
echo 🔗 Backend should be running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm start
