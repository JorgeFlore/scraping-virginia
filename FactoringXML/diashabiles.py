# La lógica de días hábiles vive en ..\comun\diashabiles.py (una sola copia
# para todas las automatizaciones). Este archivo solo la reexporta para que
# "import diashabiles" siga funcionando sin tocar main.py ni index.py.
import os as _os
import sys as _sys

_raiz = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _raiz not in _sys.path:
    _sys.path.insert(0, _raiz)

from comun.diashabiles import es_habil, previo, today  # noqa: E402,F401
