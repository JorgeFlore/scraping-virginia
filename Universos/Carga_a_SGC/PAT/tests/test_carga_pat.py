"""
Pruebas del manejo de archivos de carga_universo_pat.py con un navegador simulado.
No abre Chrome ni se conecta a SGC. Ejecutar:  python -m pytest tests -q   (desde la carpeta PAT)
"""
import importlib, json, os, sys, tempfile, types
from unittest import mock
import pytest

PAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVOS = ["96703230_1_TBUNIVERSO.TXT", "76215634_2_TBUNIVERSO.TXT", "76850128_9_TBUNIVERSO.TXT",
            "76215637_7_TBUNIVERSO.TXT", "76215628_8_TBUNIVERSO.TXT"]


class Elem:
    def click(self): pass
    def send_keys(self, *a): pass


class Driver:
    def __init__(self): self.window_handles = ["principal", "carga"]; self.cerrado = False
    def find_element(self, *a): return Elem()
    def switch_to_window(self, *a): pass
    @property
    def switch_to(self): return types.SimpleNamespace(window=lambda *a: None)
    def quit(self): self.cerrado = True
    def save_screenshot(self, p): open(p, "wb").write(b"png"); return True


class Wait:
    def __init__(self, *a, **k): pass
    def until(self, cond): return Elem()


@pytest.fixture
def entorno(monkeypatch):
    raiz = tempfile.mkdtemp()
    ruta = raiz + os.sep
    correos = []
    # módulos utils que en el servidor leen rutas C:\ y \\columbia
    chrome = types.ModuleType("utils.chrome"); chrome.ruta_descargas = lambda: ruta; chrome.opciones_chrome = lambda: Driver()
    correo = types.ModuleType("utils.envio_correo"); correo.correo = lambda msg, emp, captura=None: correos.append((emp, msg, captura))
    monkeypatch.setitem(sys.modules, "utils.chrome", chrome)
    monkeypatch.setitem(sys.modules, "utils.envio_correo", correo)
    monkeypatch.setenv("SGC_PASSWORD", "x")
    monkeypatch.syspath_prepend(PAT)
    import utils
    monkeypatch.setattr(utils, "chrome", chrome, raising=False)
    monkeypatch.setattr(utils, "envio_correo", correo, raising=False)
    sys.modules.pop("carga_universo_pat", None)
    m = importlib.import_module("carga_universo_pat")
    m.LOG_DIR = os.path.join(raiz, "logs"); m.BLOQUEO = os.path.join(m.LOG_DIR, "carga_pat.lock")
    monkeypatch.setattr(m, "sleep", lambda s: None)
    monkeypatch.setattr(m, "WebDriverWait", Wait)
    monkeypatch.setattr(m, "cargar_pagina", lambda *a, **k: Driver())
    monkeypatch.setattr(m, "verificar_contenido_pagina_inicial", lambda d, *a, **k: d)
    monkeypatch.setattr(m, "seleccionar_empresa", lambda d, e: True)
    monkeypatch.setattr(m, "inicar_sesion", lambda driver, **k: driver)
    monkeypatch.setattr(m, "ingresar_opciones_recaudacion", lambda d: None)
    monkeypatch.setattr(m, "comprobar_alerta", lambda *a: None)
    monkeypatch.setattr(m, "monitorear_proceso_archivos", lambda *a: None)
    monkeypatch.setattr(m, "guardar_excel", lambda *a: True)
    logging_reset = __import__("logging").getLogger(); logging_reset.handlers.clear()
    return types.SimpleNamespace(m=m, ruta=ruta, correos=correos)


def poner(env, nombres=ARCHIVOS):
    for n in nombres:
        open(os.path.join(env.ruta, n), "w").write("contenido " + n)


def test_todo_ok(entorno):
    poner(entorno)
    assert entorno.m.main() == 0
    for n in ARCHIVOS:
        assert not os.path.exists(os.path.join(entorno.ruta, n))           # original retirado
        assert os.path.exists(os.path.join(entorno.m.RUTA_PROCESADOS, n))  # respaldo
    assert not os.path.exists(entorno.m.ARCHIVO_CARGA)
    assert not os.path.exists(entorno.m.BLOQUEO)
    estado = json.load(open(entorno.m.ESTADO))
    assert all(v["estado"] == "ok" for v in estado.values()) and len(estado) == 5
    assert len([c for c in entorno.correos if c[0] != "Resumen"]) == 5 and entorno.correos[-1][0] == "Resumen"


def test_reejecucion_mismo_dia_no_borra_respaldos_ni_avisa(entorno):
    poner(entorno); entorno.m.main(); entorno.correos.clear()
    assert entorno.m.main() == 0
    assert entorno.correos == []                                            # nada nuevo, sin correos
    for n in ARCHIVOS:
        assert os.path.exists(os.path.join(entorno.m.RUTA_PROCESADOS, n))  # respaldos intactos


def test_segundo_archivo_mismo_dia_no_pisa_respaldo(entorno):
    poner(entorno, ARCHIVOS[:1]); entorno.m.main()
    poner(entorno, ARCHIVOS[:1]); entorno.m.main()
    respaldos = [f for f in os.listdir(entorno.m.RUTA_PROCESADOS) if f.startswith("96703230_1_TBUNIVERSO")]
    assert len(respaldos) == 2


def test_sin_archivo_avisa_y_no_abre_navegador(entorno, monkeypatch):
    abiertos = []
    monkeypatch.setattr(entorno.m, "cargar_pagina", lambda *a, **k: abiertos.append(1) or Driver())
    poner(entorno, ARCHIVOS[1:])
    assert entorno.m.main() == 2
    assert len(abiertos) == 4
    assert any("No se encontró el archivo 96703230_1" in c[1] for c in entorno.correos)


def test_falla_login_conserva_archivo_y_sigue(entorno, monkeypatch):
    llamadas = []
    def login(driver, **k):
        llamadas.append(k["empresa"])
        return None if k["empresa"] == "Aguas Décima" else driver
    monkeypatch.setattr(entorno.m, "inicar_sesion", login)
    poner(entorno)
    assert entorno.m.main() == 2
    assert os.path.exists(os.path.join(entorno.ruta, ARCHIVOS[0]))         # se reintenta mañana
    assert len(llamadas) == 5                                               # siguió con las demás
    err = [c for c in entorno.correos if c[0] == "Aguas Décima"][0][1]
    assert "se volverá a intentar" in err


def test_falla_despues_de_enviar_no_permite_doble_carga(entorno, monkeypatch):
    def monitor(driver, empresa, carpeta, proceso):
        if empresa == "Nueva Atacama" and proceso == 2:
            raise entorno.m.ErrorCarga("congelado", None)
    monkeypatch.setattr(entorno.m, "monitorear_proceso_archivos", monitor)
    poner(entorno)
    assert entorno.m.main() == 2
    assert not os.path.exists(os.path.join(entorno.ruta, "76850128_9_TBUNIVERSO.TXT"))
    assert os.path.exists(os.path.join(entorno.m.RUTA_PROCESADOS, "76850128_9_TBUNIVERSO.TXT"))
    err = [c for c in entorno.correos if c[0] == "Nueva Atacama"][0]
    assert "YA había sido enviado a SGC" in err[1] and err[2]               # con captura


def test_error_en_una_empresa_no_detiene_y_driver_quit_protegido(entorno, monkeypatch):
    class DriverRoto(Driver):
        def quit(self): raise RuntimeError("ya cerrado")
    monkeypatch.setattr(entorno.m, "cargar_pagina", lambda *a, **k: DriverRoto())
    monkeypatch.setattr(entorno.m, "ingresar_opciones_recaudacion", lambda d: (_ for _ in ()).throw(Exception("menú")))
    poner(entorno)
    assert entorno.m.main() == 2
    assert len([c for c in entorno.correos if c[0] != "Resumen"]) == 5


def test_bloqueo_evita_ejecucion_simultanea(entorno):
    os.makedirs(entorno.m.LOG_DIR, exist_ok=True); open(entorno.m.BLOQUEO, "w").write("otro")
    poner(entorno)
    assert entorno.m.main() == 0
    assert os.path.exists(os.path.join(entorno.ruta, ARCHIVOS[0]))         # no tocó nada


def test_monitor_recupera_ventana_cerrada_sin_typeerror(monkeypatch):
    """Antes: comprobar_alerta() se llamaba sin 'proceso' y fallaba con TypeError."""
    sys.path.insert(0, PAT)
    from selenium.common.exceptions import NoSuchWindowException
    from utils import proceso
    monkeypatch.setattr(proceso, "sleep", lambda s: None)
    llamadas = []
    monkeypatch.setattr(proceso, "comprobar_alerta", lambda d, e, c, p: llamadas.append(p))
    class D(Driver):
        n = 0
        @property
        def window_handles(self):
            D.n += 1
            if D.n == 2: raise NoSuchWindowException("cerrada")
            return ["a", "b", "c"] if D.n < 4 else ["a", "b"]
        @window_handles.setter
        def window_handles(self, v): pass
    monkeypatch.setattr(proceso, "WebDriverWait", Wait)
    proceso.monitorear_proceso_archivos(D(), "Empresa", tempfile.mkdtemp(), 2)
    assert llamadas == [2]
