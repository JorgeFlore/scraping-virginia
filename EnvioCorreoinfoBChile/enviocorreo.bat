@echo off
:: ==============================================
:: Script de automatización para EnvioCorreo
:: Ejecuta el proyecto Python con logs visibles
:: ==============================================

:: Fecha y hora de inicio
echo Iniciando ejecución: %date% %time%
echo ----------------------------------------

:: Cambiar al directorio del proyecto
cd /d "C:\Scraping\informacion_de_pago\bchile\EnvioCorreoinfoBChile"

:: Ejecutar el script principal
py main.py

:: Mantener la ventana abierta tras ejecutar
echo ----------------------------------------
echo Tarea finalizada a las %time%
exit
