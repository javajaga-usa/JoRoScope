@echo off
rem JoRoScope launcher for Windows: double-click to start. Launch.ps1 does the work
rem (Python check, a private .venv on first run, then the server).
title JoRoScope - Vedic Astrology
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Launch.ps1" %*
if %ERRORLEVEL% EQU 3 exit /b 3
if errorlevel 1 pause
