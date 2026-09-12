@echo off
title JoRoScope v2.0 - Vedic Astrology
cd /d "%~dp0"
py -3.12 server.py
if %ERRORLEVEL% NEQ 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Launch.ps1"
)
pause
