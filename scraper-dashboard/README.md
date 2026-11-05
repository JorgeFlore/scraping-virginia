# Panel de Scrapers

Panel web liviano para visualizar el estado y lanzar manualmente los scrapers
que hoy corren como archivos `.bat` desde el Programador de tareas de Windows.

No reemplaza el Programador de tareas: lo sigue usando para las corridas
automáticas. Lo único que cambia es que cada tarea, en lugar de llamar
directo al `.bat`, llama a `wrapper.py`, que ejecuta el `.bat`, guarda el log
y actualiza un `status.json`. El panel lee esos archivos para mostrar todo,
y el botón "Ejecutar ahora" simplemente dispara la misma tarea programada
(`schtasks /run`), así que corridas manuales y automáticas quedan
registradas exactamente igual.

## Dos formas de desplegarlo

- **Modo servidor** (el panel corre en el mismo servidor donde están los
  scrapers): es lo más simple, no necesita el campo `host` ni carpetas
  compartidas. Ir directo al paso 1.
- **Modo notebook** (el panel corre en tu notebook y controla uno o varios
  servidores remotos por red): agregá `host` y usá rutas de red (`\\SERVIDOR\...`)
  en `log_dir`. Ver la sección [Modo notebook](#modo-notebook-controlar-servidores-remotos)
  más abajo además de los pasos normales.

## Cargar automáticamente 30+ scrapers (en vez de uno por uno)

Si tenés muchos scrapers, no hace falta escribir cada bloque de
`manifest.json` a mano ni reconfigurar cada tarea en la interfaz gráfica.
Corré esto **en el servidor** donde están los `.bat` y las tareas
programadas (necesita disco y PowerShell locales):

**Paso A — descubrir los scrapers y armar `manifest.json`:**

```bat
python discover_scrapers.py --root C:\scraping
```

Sin `--apply` solo te muestra un resumen (cuántos encontró, a cuáles les
pudo encontrar la tarea programada real y a cuáles no). Cuando el resumen
te cierre, agregá `--apply` para que escriba `manifest.json`:

```bat
python discover_scrapers.py --root C:\scraping --apply
```

Esto arma una entrada por cada `.bat` que encuentra (sin importar cuántos
niveles de subcarpetas haya) y, consultando el Programador de tareas,
completa `task_scheduler_name` solo cuando logra identificar con certeza
qué tarea corre ese `.bat`. Los que no pudo emparejar (o donde dos tareas
apuntan al mismo `.bat`) te los lista aparte para que los completes/revises
vos en `manifest.json`. Si el panel va a correr en tu notebook contra este
servidor, agregá `--host SERVIDOR1` para que `log_dir` quede como ruta de
red en vez de local.

Revisá el `manifest.json` resultante — sobre todo los nombres (`name`) y
que no haya quedado ninguna entrada de un `.bat` que en realidad no sea un
scraper (por ejemplo un `.bat` auxiliar dentro de una carpeta) — antes de
seguir.

**Paso B — reconfigurar las tareas en bloque** (para que pasen por
`wrapper.py` y así queden logs y estado consistentes):

```bat
python generar_reconfiguracion.py --python "C:\Python312\python.exe" --wrapper "C:\ScraperDashboard\wrapper.py"
```

Esto no cambia nada todavía: genera `reconfigurar_tareas.bat` con un
`schtasks /change` por cada tarea que sí tiene `task_scheduler_name` (solo
toca la Acción de la tarea, el horario queda intacto). Abrilo, revisá que
los comandos tengan sentido, y corrélo una sola vez **como Administrador**
para aplicar los 30+ cambios de una.

Después de esto, seguí directo con el paso 4 (contraseña) — los pasos 2 y 3
de más abajo ya quedaron resueltos por estos dos scripts.

## 1. Instalar

En el servidor (requiere Python 3.10+ ya instalado):

```bat
cd C:\ScraperDashboard
pip install -r requirements.txt
```

Copiá toda esta carpeta a `C:\ScraperDashboard` (o donde prefieras, solo
ajustá las rutas de más abajo).

## 2. Configurar `manifest.json`

Un registro por scraper. Editá las rutas reales:

```json
{
  "id": "precios_competencia",
  "name": "Scraper de precios - competencia",
  "bat_path": "C:\\Scrapers\\precios_competencia\\run.bat",
  "task_scheduler_name": "Scrapers\\PreciosCompetencia",
  "schedule": "Diario 06:00",
  "log_dir": "C:\\ScraperDashboard\\logs\\precios_competencia"
}
```

- `id`: identificador corto, sin espacios, único.
- `bat_path`: ruta real del `.bat` que ya tenés.
- `task_scheduler_name`: nombre exacto de la tarea en el Programador de
  tareas (podés organizarlas en una carpeta, ej. `Scrapers\NombreTarea`).
- `schedule`: solo texto informativo para la pantalla.
- `log_dir`: carpeta donde se van a guardar los logs y el `status.json` de
  ese scraper (se crea sola si no existe).
- `host` *(opcional)*: nombre o IP del servidor donde vive la tarea
  programada. Se usa solo si el panel corre en una máquina distinta
  (modo notebook, ver más abajo). Si el panel corre en el mismo servidor
  que la tarea, se puede omitir.

Agregar un scraper nuevo = agregar un bloque acá + el paso 3.

## 3. Apuntar cada tarea programada al wrapper

Para **cada** tarea existente, en el Programador de tareas → pestaña
**Acciones** → Editar:

| Campo | Valor |
|---|---|
| Programa/script | `C:\Python312\python.exe` (ruta real de tu Python) |
| Agregar argumentos | `C:\ScraperDashboard\wrapper.py --id precios_competencia` |

Usá el `id` correspondiente de cada scraper. El wrapper busca en
`manifest.json` la ruta real del `.bat` y lo ejecuta por vos, así que ya no
hace falta que la tarea programada sepa la ruta del `.bat` directamente.

## 4. Configurar contraseña del panel

El panel pide login porque permite ejecutar procesos en el servidor.
Definí estas variables de entorno antes de levantarlo (o cambiá los
valores por defecto en `app.py`, pero las variables de entorno son más
seguras):

```bat
setx DASHBOARD_PASSWORD "una-clave-fuerte"
setx DASHBOARD_SECRET_KEY "otra-cadena-aleatoria-larga"
```

## 5. Levantar el panel

Para probar rápido:

```bat
python app.py
```

Para dejarlo corriendo en producción (el servidor de desarrollo de Flask no
es apto para eso), usá `waitress`, que ya está en `requirements.txt`:

```bat
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

Para que sobreviva reinicios del servidor, lo más simple es envolver ese
comando como una tarea programada más (ejecutar al iniciar el sistema) o
instalarlo como servicio de Windows con **NSSM** (`nssm install
PanelScrapers waitress-serve --host=0.0.0.0 --port=5000 app:app`).

Después entrás desde cualquier navegador de la red interna a
`http://nombre-del-servidor:5000`.

## Modo notebook: controlar servidores remotos

Si preferís correr el panel desde tu notebook (en vez de instalarlo en el
servidor) y desde ahí controlar uno o varios servidores donde corren los
scrapers, hace falta esto:

**1. Que tu usuario pueda administrar tareas programadas en remoto.**
Cada servidor necesita tener habilitada la regla de firewall "Administración
remota de tareas programadas" (*Remote Scheduled Tasks Management*, se
activa en Firewall de Windows con seguridad avanzada → Reglas de entrada).
Esto normalmente lo activa el equipo de sistemas si el servidor es
compartido con otros equipos.

**2. Guardar las credenciales una sola vez por servidor** (evita tener que
escribir usuario/clave en ningún archivo del proyecto):

```bat
cmdkey /add:SERVIDOR1 /user:TUDOMINIO\tu_usuario /pass
```

Windows te va a pedir la contraseña de forma interactiva y la guarda cifrada
en el Administrador de credenciales de tu notebook. A partir de ahí,
cualquier `schtasks /s SERVIDOR1 ...` usa esa credencial automáticamente.
Repetí esto por cada servidor distinto que quieras controlar.

**3. Compartir la carpeta de logs de cada servidor.**
En el servidor, click derecho sobre la carpeta de logs (por ejemplo
`C:\ScraperDashboard\logs`) → Propiedades → Compartir, y dale a tu usuario
(o a un grupo) permiso de lectura. Anotá el nombre del recurso compartido,
por ejemplo `\\SERVIDOR1\ScraperLogs`.

**4. Completar `manifest.json` con `host` y rutas UNC en `log_dir`**, como en
el ejemplo que trae el proyecto:

```json
{
  "id": "precios_competencia",
  "host": "SERVIDOR1",
  "log_dir": "\\\\SERVIDOR1\\ScraperLogs\\precios_competencia",
  "bat_path": "C:\\Scrapers\\precios_competencia\\run.bat",
  "...": "..."
}
```

`bat_path` queda igual (una ruta local del servidor) porque solo la usa
`wrapper.py`, que sigue corriendo *en* ese servidor sin cambios.

**5. Correr el panel en tu notebook:**

```bat
python app.py
```

Y abrir `http://localhost:5000` en el navegador de tu propia notebook. Como
en este modo el panel es para uso personal, no hace falta exponerlo a la
red (no necesitás `waitress` ni dejarlo corriendo como servicio) — con
tenerlo abierto mientras trabajás alcanza. Si en algún momento otras
personas del equipo necesitan verlo también, conviene volver al modo
servidor (correrlo en una máquina que esté siempre encendida) en vez de
depender de que tu notebook esté prendida.

**Nota:** si `schtasks /s SERVIDOR1 ...` falla con error de acceso denegado
aun con la credencial guardada, normalmente es el firewall del paso 1 (el
puerto RPC 135 y el rango dinámico deben estar abiertos entre tu notebook y
el servidor) — es un tema para conversar con sistemas si no administrás
vos mismo esos servidores.

## Seguridad — importante

Este panel puede disparar ejecuciones en el servidor, así que:

- No lo expongas a internet. Solo debería ser accesible dentro de la red
  interna de la empresa (o detrás de VPN).
- Cambiá `DASHBOARD_PASSWORD` por algo que no sea el valor por defecto.
- Si varias personas lo van a usar y necesitás saber quién ejecutó qué,
  este login básico no alcanza — habría que sumar autenticación por
  usuario (por ejemplo integrando con Active Directory vía IIS).

## Qué hace cada estado

| Estado | Significado |
|---|---|
| `nunca_ejecutado` | Todavía no corrió ni una vez desde que existe el wrapper |
| `running` | Está corriendo en este momento |
| `ok` | Terminó con código de salida 0 |
| `error` | Terminó con código de salida distinto de 0 |
| `revisar` | Lleva "running" más de 2 horas — probablemente se colgó |

El umbral de "revisar" se ajusta en `app.py`, variable `STALE_MINUTES`.

## Estructura del proyecto

```
scraper-dashboard/
  app.py            Backend Flask (panel + API)
  wrapper.py         Envoltorio que ejecuta cada .bat y registra el resultado
  manifest.json       Lista de scrapers (editar con tus datos reales)
  requirements.txt
  templates/
    index.html
    login.html
  static/
    style.css
    script.js
```

## Ideas para más adelante (no incluidas, por si las querés sumar)

- Notificación por email o Slack cuando un scraper termina en `error`.
- Historial/gráfico de duración de cada scraper en el tiempo.
- Botón "Cancelar" para tareas colgadas (`schtasks /end /tn ...`).
- Autenticación por usuario en vez de una sola contraseña compartida.
