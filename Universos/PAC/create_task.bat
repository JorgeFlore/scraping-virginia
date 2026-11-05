@echo off
set SCRIPT_PATH=%~dp0run_api.py
schtasks /create /tn "PAC_API" /tr "python \"%SCRIPT_PATH%\"" /sc onstart /ru SYSTEM /f
echo Tarea programada creada
pause