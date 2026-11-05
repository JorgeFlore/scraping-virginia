#!/usr/bin/env python
"""
generar_reconfiguracion.py - Genera un .bat con los comandos schtasks
/change necesarios para que cada tarea programada llame a wrapper.py en vez
de llamar directo al .bat original. Pensado para no tener que editar 30+
tareas a mano en la interfaz grafica del Programador de tareas.

Este script NO modifica nada por si solo: solo escribe un .bat que vos
revisas y despues corres (como Administrador) cuando estes de acuerdo con
lo que va a cambiar. Solo toca la Accion de cada tarea (/tr) - el horario y
los triggers quedan exactamente igual que estaban.

Uso:
    python generar_reconfiguracion.py --manifest manifest.json ^
        --python "C:\\Python312\\python.exe" ^
        --wrapper "C:\\ScraperDashboard\\wrapper.py"
"""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="manifest.json")
    parser.add_argument("--python", default=r"C:\Python312\python.exe", help="Ruta al python.exe del servidor")
    parser.add_argument("--wrapper", default=r"C:\ScraperDashboard\wrapper.py")
    parser.add_argument("--out", default="reconfigurar_tareas.bat")
    args = parser.parse_args()

    with open(args.manifest, "r", encoding="utf-8") as f:
        data = json.load(f)
    tasks = data.get("tasks", [])

    lines = [
        "@echo off",
        "REM Generado por generar_reconfiguracion.py - revisar antes de correr.",
        "REM Corre esto como Administrador. Solo cambia la Accion de cada tarea,",
        "REM el horario/triggers existentes no se tocan.",
        "",
    ]
    incluidas, salteadas = 0, []

    for t in tasks:
        task_name = t.get("task_scheduler_name")
        scraper_id = t["id"]
        if not task_name:
            salteadas.append(scraper_id)
            continue
        tr_value = f'\\"{args.python}\\" \\"{args.wrapper}\\" --id {scraper_id}'
        lines.append(f'echo Reconfigurando: {task_name}')
        lines.append(f'schtasks /change /tn "{task_name}" /tr "{tr_value}"')
        lines.append("if errorlevel 1 (echo   -^> FALLO) else (echo   -^> OK)")
        lines.append("")
        incluidas += 1

    lines.append("echo.")
    lines.append("echo Listo.")
    lines.append("pause")

    Path(args.out).write_text("\r\n".join(lines), encoding="utf-8")

    print(f"Generado {args.out} con {incluidas} tareas para reconfigurar.")
    if salteadas:
        print(f"Se salteo {len(salteadas)} scraper(s) sin 'task_scheduler_name' "
              f"(completalos a mano en manifest.json y volve a correr este script): "
              + ", ".join(salteadas))
    print("Revisa el .bat generado antes de correrlo.")


if __name__ == "__main__":
    main()
