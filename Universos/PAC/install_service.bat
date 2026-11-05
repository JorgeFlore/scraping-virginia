@echo off
echo Instalando servicio PAC API...
python service_installer.py install
python service_installer.py start
echo Servicio instalado y iniciado
pause