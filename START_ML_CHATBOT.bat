@echo off
echo ========================================
echo Starting ML Jewelry Chatbot Server
echo ========================================
cd /d "%~dp0"
".venv\Scripts\python.exe" ml_chatbot_final.py
pause
