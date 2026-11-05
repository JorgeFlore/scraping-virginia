#!/usr/bin/env python
"""
wrapper.py - Envoltorio de ejecucion para los scrapers .bat

Se invoca desde el Programador de tareas de Windows EN LUGAR de llamar al
.bat directamente. Se encarga de:

  - Ejecutar el .bat definido en manifest.json para el id dado
  - Guardar un log con marca de tiempo
  - Mantener un status.json con el estado de la ultima corrida, que el
    panel web (app.py) usa para mostrar el estado de cada scraper

Uso (esto es lo que va en la Accion de la tarea programada de Windows):
    Programa/script:  C:\\Python312\\python.exe
    Argumentos:       C:\\ScraperDashboard\\wrapper.py --id precios_competencia
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_MANIFEST = Path(__file__).resolve().parent / "manifest.json"
MAX_LOGS_PER_TASK = 30  # cuantos logs viejos conservar por scraper


def load_manifest(manifest_path: Path) -> dict:
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {t["id"]: t for t in data.get("tasks", [])}


def find_task(tasks: dict, task_id: str) -> dict:
    if task_id not in tasks:
        print(f"ERROR: no existe el id '{task_id}' en manifest.json", file=sys.stderr)
        sys.exit(2)
    return tasks[task_id]


def write_status(log_dir: Path, status: dict) -> None:
    status_path = log_dir / "status.json"
    tmp_path = log_dir / "status.json.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    tmp_path.replace(status_path)  # escritura casi-atomica


def rotate_logs(log_dir: Path, task_id: str) -> None:
    logs = sorted(log_dir.glob(f"{task_id}_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old_log in logs[MAX_LOGS_PER_TASK:]:
        try:
            old_log.unlink()
        except OSError:
            pass


def run_task(task: dict) -> int:
    task_id = task["id"]
    bat_path = task["bat_path"]
    log_dir = Path(task["log_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)

    start_dt = datetime.now()
    timestamp = start_dt.strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{task_id}_{timestamp}.log"

    write_status(log_dir, {
        "id": task_id,
        "state": "running",
        "start": start_dt.isoformat(timespec="seconds"),
        "end": None,
        "exit_code": None,
        "duration_seconds": None,
        "log_file": str(log_file),
    })

    bat_dir = Path(bat_path).parent
    with open(log_file, "w", encoding="utf-8", errors="replace") as lf:
        lf.write(f"=== INICIO {start_dt.isoformat(timespec='seconds')} ===\n")
        lf.write(f"Comando: {bat_path}\n\n")
        lf.flush()
        try:
            result = subprocess.run(
                [bat_path],
                stdout=lf,
                stderr=subprocess.STDOUT,
                shell=True,
                cwd=str(bat_dir) if bat_dir.exists() else None,
            )
            exit_code = result.returncode
        except Exception as exc:
            lf.write(f"\nERROR AL EJECUTAR: {exc}\n")
            exit_code = -1

        end_dt = datetime.now()
        duration = (end_dt - start_dt).total_seconds()
        lf.write(f"\n=== FIN {end_dt.isoformat(timespec='seconds')} - EXIT_CODE {exit_code} ===\n")

    state = "ok" if exit_code == 0 else "error"
    write_status(log_dir, {
        "id": task_id,
        "state": state,
        "start": start_dt.isoformat(timespec="seconds"),
        "end": end_dt.isoformat(timespec="seconds"),
        "exit_code": exit_code,
        "duration_seconds": round(duration, 1),
        "log_file": str(log_file),
    })

    rotate_logs(log_dir, task_id)
    return exit_code


def main():
    parser = argparse.ArgumentParser(description="Ejecuta un scraper y registra su resultado.")
    parser.add_argument("--id", required=True, help="Id del scraper segun manifest.json")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Ruta al manifest.json")
    args = parser.parse_args()

    tasks = load_manifest(Path(args.manifest))
    task = find_task(tasks, args.id)
    exit_code = run_task(task)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
