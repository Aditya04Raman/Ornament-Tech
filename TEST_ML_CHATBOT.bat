@echo off
echo ========================================
echo Testing ML Chatbot
echo ========================================
cd /d "%~dp0"
timeout /t 3 /nobreak >nul
echo.
echo Testing health endpoint...
curl http://localhost:5000/health
echo.
echo.
echo Testing inventory question...
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"what types of jewellery do you have?\"}"
echo.
echo.
echo Testing search...
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"show me diamond rings\"}"
echo.
pause
