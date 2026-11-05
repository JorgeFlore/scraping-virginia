# Cambios bot Botón de Pago Banco de Chile (SFTP Prod) — 29-10-2026

Los originales quedaron en `_respaldo_20261029\`.

## Correcciones
- **Año dinámico**: ya no está "2026" fijo en el código. Se suben los archivos con el año actual en el nombre (y en enero también los del año anterior).
- **Si el SFTP falla, ya no se informa éxito**: llega un correo `[ERROR]` y los archivos se quedan en `C:\Rendicion\bchile` para el siguiente intento.
- **Solo se mueven a `enviados` los archivos que se subieron bien**. Se verifica el tamaño remoto de cada uno.
- **El correo muestra lo que realmente se subió**, por empresa, y lista los archivos que fallaron. El asunto lleva `[INCOMPLETO]` o `[ERROR]` cuando corresponde.
- **API de feriados**: tiene reintentos y timeout. Si no responde en un día de semana, el bot se ejecuta igual y lo avisa en el correo.
- **Detección de empresa**: busca el código como palabra (evita que "DATA" cuente como ATA). Si no lo encuentra así, usa la búsqueda original.

## Mejoras
- `config.py`: rutas, servidor, empresas y destinatarios en un solo lugar.
- **Logs con fecha y hora** en `logs\bot_AAAAMMDD.log`. `log.txt` acumula solo avisos y errores.
- **Fecha del proceso** = día hábil anterior (antes era siempre "ayer").
- **Reintentos de conexión SFTP** (3) y timeouts.
- **Huella del servidor SFTP** queda en el log. Para activar la validación, copiarla en `SFTP_HUELLA_SERVIDOR` de `config.py`.
- **Si falla el correo**, los archivos ya subidos igual se mueven, para no reenviarlos.
- **Códigos de salida del .bat**: 0 OK, 1 incompleto, 2 error.

## Sin cambios
- **`carga_rend`**: se sigue subiendo y no se mueve a `enviados`, igual que antes. Por eso se sube en cada ejecución; revisar si es lo esperado.
- **Destinatarios, banner y formato del correo**: iguales que antes.
