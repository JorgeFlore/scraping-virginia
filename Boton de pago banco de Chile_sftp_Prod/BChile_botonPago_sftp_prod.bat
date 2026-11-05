@echo off
cd /d C:\Scraping\Boton de pago banco de Chile_sftp_Prod

rem El detalle de cada ejecucion queda en la carpeta logs\ (un archivo por dia).
rem log.txt solo acumula errores graves de Python (por ejemplo, una libreria faltante).
"C:\Users\win10\AppData\Local\Programs\Python\Python312\python.exe" main.py >> log.txt 2>&1

exit /b %ERRORLEVEL%
