@echo off
REM Generado por generar_reconfiguracion.py - revisar antes de correr.
REM Corre esto como Administrador. Solo cambia la Accion de cada tarea,
REM el horario/triggers existentes no se tocan.

echo Reconfigurando: Scrapers\PreciosCompetencia
schtasks /change /tn "Scrapers\PreciosCompetencia" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id precios_competencia"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Scrapers\StockProveedores
schtasks /change /tn "Scrapers\StockProveedores" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id stock_proveedores"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Scrapers\NoticiasSector
schtasks /change /tn "Scrapers\NoticiasSector" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id noticias_sector"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Conciliacion Santander
schtasks /change /tn "Conciliacion Santander" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id aws_scraping_conciliacion_bancaria"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Boton de pago compra aqui sftp
schtasks /change /tn "Boton de pago compra aqui sftp" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id bestadocompraaqui_sftp"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Bestado_compraAqui_sftp_prod
schtasks /change /tn "Bestado_compraAqui_sftp_prod" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id bestadocompraaqui_sftp_prod"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: ejecutar boletas de honorarios
schtasks /change /tn "ejecutar boletas de honorarios" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id boletas_honorarios"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Ejecutar licencias SAP
schtasks /change /tn "Ejecutar licencias SAP" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id bot_licencias_sap"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Bchile_Bpago_Sftp_Prod
schtasks /change /tn "Bchile_Bpago_Sftp_Prod" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id boton_de_pago_banco_de_chile_sftp_prod"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: BEstado_botonpago_sftp_prod
schtasks /change /tn "BEstado_botonpago_sftp_prod" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id boton_de_pago_banco_de_estado_sftp_prod"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Boton de pago BCI SFTP
schtasks /change /tn "Boton de pago BCI SFTP" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id botonpagobci_sftp"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Bci_boton_sftp_prod
schtasks /change /tn "Bci_boton_sftp_prod" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id botonpagobci_sftp_prod"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Factoring PDF
schtasks /change /tn "Factoring PDF" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id factoringpdf"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: ejecutar factoringXML
schtasks /change /tn "ejecutar factoringXML" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id factoringxml"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Limpiar S3 boton BancoEstado
schtasks /change /tn "Limpiar S3 boton BancoEstado" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id limpiars3_boton_de_pago_bestado_bchile"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: LimpiezaS3Transbank
schtasks /change /tn "LimpiezaS3Transbank" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id limpiars3_transbank"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Limpia S3 Carpeta Recauadcion
schtasks /change /tn "Limpia S3 Carpeta Recauadcion" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id limpiars3ypacpat"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Archivo Excel TBK
schtasks /change /tn "Archivo Excel TBK" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id plsql_python"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Archivo Excel TBK con OC
schtasks /change /tn "Archivo Excel TBK con OC" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id plsql_python_copia"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: reincio outlook
schtasks /change /tn "reincio outlook" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id reinicia_outlook"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Descarga Universo PAT TransData
schtasks /change /tn "Descarga Universo PAT TransData" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id scraping_botpat"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP_BancoEstado
schtasks /change /tn "SFTP_BancoEstado" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpbancoestado"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP_BPServipag
schtasks /change /tn "SFTP_BPServipag" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpbpservipag"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP_PrestoRed
schtasks /change /tn "SFTP_PrestoRed" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpprestored"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP_Santander_Prod
schtasks /change /tn "SFTP_Santander_Prod" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpsantander"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP_Servipag
schtasks /change /tn "SFTP_Servipag" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpservipag"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP_ServipagExpress
schtasks /change /tn "SFTP_ServipagExpress" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpservipagexpress"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: SFTP Unired
schtasks /change /tn "SFTP Unired" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id sftpunired"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: descarga_info_medidores_athena
schtasks /change /tn "descarga_info_medidores_athena" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id telelectura_consultar_medidores_athena"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: descargaInfoMedidoresBecoy
schtasks /change /tn "descargaInfoMedidoresBecoy" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id telelectura_obtenermedidoresgatewaybecoy"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: descargar_medidores_gateway
schtasks /change /tn "descargar_medidores_gateway" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id telelectura_obtenermedidorgateway"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Envio Correo Universos PAC
schtasks /change /tn "Envio Correo Universos PAC" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id universos_envio_correo_iuniversospac"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo Reconfigurando: Envio correo Universo PAT
schtasks /change /tn "Envio correo Universo PAT" /tr "\"C:\Python312\python.exe\" \"C:\ScraperDashboard\wrapper.py\" --id universos_envio_correo_iuniversospat"
if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)

echo.
echo Listo.
pause