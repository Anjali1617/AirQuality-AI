@echo off
title AirQuality-AI Launcher
echo ==============================================
echo   Launching AirQuality-AI Full Stack App
echo ==============================================
start "AirQuality-AI Backend" cmd /c "%~dp0start_backend.bat"
timeout /t 3 /nobreak >nul
start "AirQuality-AI Frontend" cmd /c "%~dp0start_frontend.bat"
echo Applications launched in separate windows.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
