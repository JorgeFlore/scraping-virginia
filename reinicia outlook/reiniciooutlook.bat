@echo off
echo ==========================================================
echo Reinicio automático de Microsoft Outlook
echo ==========================================================
echo Cerrando Outlook si está abierto...
taskkill /f /im outlook.exe >nul 2>&1

echo Esperando 5 segundos...
timeout /t 5 /nobreak >nul

echo Iniciando Outlook en modo minimizado...
start "" /min "C:\Program Files\Microsoft Office 15\root\office15\OUTLOOK.EXE"

echo Outlook reiniciado (minimizado) correctamente.
exit
