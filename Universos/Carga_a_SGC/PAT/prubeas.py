from unittest.mock import MagicMock
import time

# Simulamos el objeto que retorna el elemento con el texto del progreso.
class FakeProgressElement:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

# Simulación de la lógica de comprobación
def test_progress_freeze(get_progress, max_wait_time=60):
    prev_progress = None
    unchanged_start_time = None

    while True:
        current_element = get_progress()
        current_progress = current_element.text.strip()
        print("Progreso actual:", current_progress)

        if prev_progress is not None:
            if current_progress == prev_progress:
                if unchanged_start_time is None:
                    unchanged_start_time = time.time()
                else:
                    elapsed = time.time() - unchanged_start_time
                    if elapsed >= max_wait_time:
                        raise Exception("El proceso se ha congelado por 60 segundos.")
            else:
                prev_progress = current_progress
                unchanged_start_time = time.time()
        else:
            prev_progress = current_progress
            unchanged_start_time = time.time()

        # Simulación de la espera entre comprobaciones
        time.sleep(1)
        # Condición de salida para la prueba, por ejemplo después de 70 segundos.
        if time.time() - unchanged_start_time > 70:
            break

# Uso de mocks para simular cambios en el progreso
progress_values = ["10%", "10%", "12%", "14%", "14%", "14%", "14%", "20%", "20%", "20%", "20%", "20%", "20%", "20%", "20%", "20%", "20%"]

def fake_get_progress():
    # Devuelve valores de la lista, simulando que el progreso se congela a "20%"
    value = progress_values.pop(0) if progress_values else "20%"
    return FakeProgressElement(value)

try:
    test_progress_freeze(fake_get_progress, max_wait_time=5)  # Usa un max_wait_time menor para probar rápidamente
except Exception as e:
    print(e)
