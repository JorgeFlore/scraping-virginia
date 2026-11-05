# Scraping Virginia

Automatizaciones (bots Python + `.bat` del Programador de tareas de Windows) para
cartolas bancarias, botones de pago, transferencias SFTP a recaudadores, correos de
información de pago, factoring, SAP/SII y consultas Oracle.

## Estructura actual

| Grupo | Carpetas |
|---|---|
| Librería común | `comun/` (hoy: `diashabiles`) |
| Botones de pago | `botonPagoBCI*`, `Boton de pago banco de Estado_*`, `Boton de pago banco de Chile_sftp_Prod`, `BestadoCompraAqui*` |
| SFTP recaudadores | `SFTPServipag`, `SFTPServipagExpress`, `SFTPBPServipag`, `SFTPUnired`, `SFTPPrestoRED`, `SFTPSantander`, `SFTPBancoEstado`, `toku_subida_pac` |
| Correos info de pago | `Envio correo*`, `EnvioCorreoinfoBChile`, `CorreoBancoEstado`, `reinicia outlook`, `informacion_de_pago` |
| Cartolas | `bci`, `descargaCartolasBancoestado` |
| Factoring | `FactoringPDF`, `FactoringXML`, `FactoringXML2.0`, `XML/` (versiones antiguas) |
| SAP / SII / otros | `Bot Licencias SAP`, `Generación nóminas SAP`, `Boletas_honorarios`, `Descarga decretos`, `Carga archivo C`, `Universos` |
| Oracle | `PLSQL Python` |
| Mantenimiento | `limpiarS3-*` |
| Panel | `scraper-dashboard` |

Los scrapers AWS (`AWS_Scraping`, `Aws_scraping_conciliacion_bancaria`,
`AWS_Scraping_depositos_transbank`) viven en sus propios repositorios de la organización.

## Credenciales

Ninguna contraseña está en el código. Cada bot las lee con `os.getenv(...)`.
La lista completa de variables está en [`.env.ejemplo`](.env.ejemplo).

En el servidor/PC donde corren los bots, definirlas una vez:

```bat
setx SFTP_SERVIPAG_PASSWORD "valor"
```

> Importante: la copia de este código que está **en el PC** todavía tiene las claves
> escritas. Antes de reemplazarla por la de este repositorio, define las variables.

Las llaves SFTP (`llaveprod`, etc.) y los CSV de credenciales **no** se suben (ver `.gitignore`).

## Qué no se versiona

Archivos generados (`enviados/`, `descargas/`, logs, `historial.json`), binarios
(`msedgedriver.exe`, instantclient de Oracle) y secretos. Ver `.gitignore`.
