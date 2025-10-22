@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
REM Ensure we run from repo root (this file's directory)
cd /d "%~dp0"
echo ========================================
echo STARTING COMPLETE ORNAMENT TECH SYSTEM
echo ========================================
echo.

echo [1/2] Starting ML Chatbot Server...
if not exist .venv\Scripts\python.exe (
	echo   - Creating Python venv and installing requirements...
	py -m venv .venv
)
call .venv\Scripts\activate
pip install --upgrade pip >nul
if exist requirements.txt (
	echo   - Installing Python deps from requirements.txt
	pip install -r requirements.txt
)
if exist ml-chatbot\requirements.txt (
	echo   - Installing ML service deps from ml-chatbot\requirements.txt (this may take a while)
	pip install -r ml-chatbot\requirements.txt || (
		echo   - Falling back to minimal deps for ML service
		pip install flask flask-cors pandas
	)
) else (
	echo   - Installing minimal deps for ML service
	pip install flask flask-cors pandas
)
deactivate

set "PYEXE=.venv\Scripts\python.exe"
set "ML_ENTRY=ml_chatbot_final.py"
if not exist "%ML_ENTRY%" (
	if exist "ml-chatbot\api\app.py" (
		set "ML_ENTRY=ml-chatbot\api\app.py"
	) else if exist "ml-chatbot\lightweight_ml_service.py" (
		set "ML_ENTRY=ml-chatbot\lightweight_ml_service.py"
	)
)

start "ML Chatbot" cmd /k "cd /d "%~dp0" && "%PYEXE%" "%ML_ENTRY%""

echo Waiting for ML server health (http://localhost:5000/health)...
for /l %%i in (1,1,15) do (
	>nul 2>&1 powershell -Command "try { (Invoke-RestMethod -Uri 'http://localhost:5000/health' -TimeoutSec 1) | Out-Null; exit 0 } catch { exit 1 }"
	if !errorlevel! EQU 0 (
		echo   - ML server is healthy.
		goto :ml_ready
	) else (
		>nul timeout /t 1 /nobreak
	)
)
echo   - ML server health not detected. The website will use dataset fallback.
:ml_ready

echo.
echo [2/2] Starting Website...
if not exist node_modules (
	echo   - Installing npm dependencies...
	call npm install
)
start "Website" cmd /k "cd /d "%~dp0" && npm run dev"

echo.
echo ========================================
echo STARTUP COMPLETE!
echo ========================================
echo.
echo ML Chatbot: http://localhost:5000
echo Website: Usually http://localhost:3000 (Next.js auto-switches to next free port)
echo   - Check the Website window for the exact URL printed as "Local: http://localhost:PORT"
echo.
echo Two windows opened:
echo - Window 1: ML Chatbot (must stay running)
echo - Window 2: Website (must stay running)
echo.
echo Press any key to close THIS window...
echo (The other windows will keep running)
pause >nul
endlocal
