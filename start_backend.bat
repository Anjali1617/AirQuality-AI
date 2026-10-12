@echo off
title AirQuality-AI Backend (FastAPI)
echo ==============================================
echo   Starting AirQuality-AI Backend API
echo   Endpoint: http://localhost:8000
echo   Docs:     http://localhost:8000/docs
echo ==============================================
cd /d "%~dp0backend"
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
