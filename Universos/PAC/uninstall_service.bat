@echo off
echo Desinstalando servicio PAC API...
python service_installer.py stop
python service_installer.py remove
echo Servicio desinstalado
pause