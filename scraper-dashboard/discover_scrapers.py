#!/usr/bin/env python
"""
discover_scrapers.py - Escanea una carpeta con muchos scrapers y arma (o
actualiza) manifest.json automaticamente, en vez de cargar cada scraper a
mano.

Se corre LOCALMENTE en el servidor donde estan los .bat y las tareas
programadas (necesita acceso al disco y a PowerShell locales para poder
emparejar cada .bat con su tarea).

Que hace:
  1. Busca todos los .bat dentro de --root, sin importar la profundidad de
     subcarpetas (una carpeta por scraper, o varios .bat sueltos, ambos
     casos andan).
  2. Consulta las tareas programadas de Windows (via PowerShell) y trata de
     encontrar, para cada .bat, cual tarea lo ejecuta - asi no hay que
     tipear 30 nombres de tarea a mano.
  3. Escribe/actualiza manifest.json: agrega los scrapers nuevos, deja sin
     tocar los que ya estaban (por si los editaste a mano), y avisa cuales
     no pudo emparejar con ninguna tarea para que los revises vos.

Uso tipico (parado en la carpeta del proyecto, en el servidor):
    python discover_scrapers.py --root C:\\scraping --apply

Sin --apply, solo muestra un resumen (modo simulacion) y no escribe nada -
conviene correrlo asi primero para revisar que va a encontrar.

Si el panel corre en tu notebook controlando este servidor en remoto,
agregale --host para que el log_dir quede como ruta de red:
    python discover_scrapers.py --root C:\\scraping --host SERVIDOR1 --apply
"""

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "scraper"


def find_bat_candidates(root: Path):
    """Devuelve una lista de (id_sugerido, nombre_sugerido, ruta_bat), sin
    importar cuantos niveles de subcarpetas haya entre root y cada .bat."""
    if not root.exists():
        print(f"ERROR: no existe la carpeta {root}", file=sys.stderr)
        sys.exit(1)

    by_folder = {}
    for bat in sorted(root.rglob("*.bat")):
        by_folder.setdefault(bat.parent, []).append(bat)

    candidates = []
    for folder, bats in by_folder.items():
        rel = folder.relative_to(root)
        label = str(rel) if str(rel) != "." else (bats[0].stem if len(bats) == 1 else folder.name)
        if len(bats) == 1:
            candidates.append((slugify(label), label.replace("\\", " ").replace("_", " "), bats[0]))
        else:
            for bat in bats:
                combo = f"{label}_{bat.stem}" if label != bat.stem else bat.stem
                candidates.append((slugify(combo), combo.replace("\\", " ").replace("_", " "), bat))

    return sorted(candidates, key=lambda c: c[0])


def query_scheduled_tasks():
    """Devuelve una lista de dicts con FullName y Actions de cada tarea
    programada, usando PowerShell (evita problemas de idioma que tiene
    parsear la salida de 'schtasks' directamente)."""
    ps_script = (
        "Get-ScheduledTask | ForEach-Object { "
        "[PSCustomObject]@{ "
        "FullName = ($_.TaskPath + $_.TaskName); "
        "Actions = (($_.Actions | ForEach-Object { \"$($_.Execute) $($_.Arguments)\" }) -join ' | ') "
        "} } | ConvertTo-Json -Depth 4"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"AVISO: no se pudo consultar el Programador de tareas ({exc}). "
              f"Vas a tener que completar 'task_scheduler_name' a mano.", file=sys.stderr)
        return []

    if result.returncode != 0 or not result.stdout.strip():
        print("AVISO: PowerShell no devolvio tareas programadas. "
              "Vas a tener que completar 'task_scheduler_name' a mano.", file=sys.stderr)
        return []

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("AVISO: no se pudo interpretar la salida de PowerShell.", file=sys.stderr)
        return []

    if isinstance(data, dict):  # PowerShell devuelve un objeto solo (no lista) si hay 1 tarea
        data = [data]
    return data


def match_task(bat_path: Path, tasks: list):
    """Devuelve (nombre_tarea_o_None, es_ambiguo)."""
    bat_str = str(bat_path).lower()
    matches = [t for t in tasks if bat_str in (t.get("Actions") or "").lower()]
    if not matches:
        return None, False
    task_name = matches[0]["FullName"].strip("\\")
    return task_name, len(matches) > 1


def build_entry(scraper_id, name, bat_path, host, log_root, task_name):
    if host:
        log_dir = f"\\\\{host}\\ScraperLogs\\{scraper_id}"
    else:
        log_dir = str(Path(log_root) / scraper_id)
    entry = {
        "id": scraper_id,
        "name": name.strip().capitalize(),
        "bat_path": str(bat_path),
        "task_scheduler_name": task_name or "",
        "schedule": "",
        "log_dir": log_dir,
    }
    if host:
        entry["host"] = host
    return entry


def main():
    parser = argparse.ArgumentParser(description="Descubre scrapers en una carpeta y arma manifest.json")
    parser.add_argument("--root", default=r"C:\scraping", help="Carpeta raiz donde estan los scrapers")
    parser.add_argument("--manifest", default="manifest.json", help="manifest.json a crear/actualizar")
    parser.add_argument("--host", default=None, help="Nombre del servidor (solo si el panel corre en otra maquina)")
    parser.add_argument("--log-root", default=r"C:\ScraperDashboard\logs", help="Carpeta base de logs (modo local)")
    parser.add_argument("--apply", action="store_true", help="Escribe manifest.json (sin esto solo muestra el resumen)")
    args = parser.parse_args()

    root = Path(args.root)
    manifest_path = Path(args.manifest)

    candidates = find_bat_candidates(root)
    if not candidates:
        print(f"No se encontro ningun .bat dentro de {root}")
        return

    tasks = query_scheduled_tasks()

    existing = {}
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        existing = {t["id"]: t for t in existing_data.get("tasks", [])}

    seen_ids = set(existing.keys())
    nuevos, ya_existian, sin_match, ambiguos = [], [], [], []

    for scraper_id, name, bat_path in candidates:
        if scraper_id in existing:
            ya_existian.append(scraper_id)
            continue

        original_id = scraper_id
        n = 2
        while scraper_id in seen_ids:
            scraper_id = f"{original_id}_{n}"
            n += 1
        seen_ids.add(scraper_id)

        task_name, ambiguous = match_task(bat_path, tasks)
        nuevos.append(build_entry(scraper_id, name, bat_path, args.host, args.log_root, task_name))
        if not task_name:
            sin_match.append(scraper_id)
        elif ambiguous:
            ambiguos.append(scraper_id)

    print(f"Encontrados: {len(candidates)} scrapers en {root}")
    print(f"  Ya estaban en el manifest:  {len(ya_existian)}")
    print(f"  Nuevos para agregar:        {len(nuevos)}")
    if sin_match:
        print(f"\n  Sin tarea programada encontrada (completar 'task_scheduler_name' a mano):")
        for sid in sin_match:
            print(f"    - {sid}")
    if ambiguos:
        print(f"\n  Mas de una tarea apunta al mismo .bat (se tomo la primera, revisar):")
        for sid in ambiguos:
            print(f"    - {sid}")

    if not args.apply:
        print("\n(modo simulacion, no se escribio nada - agrega --apply para guardar)")
        return

    all_tasks = list(existing.values()) + nuevos
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"tasks": all_tasks}, f, ensure_ascii=False, indent=2)
    print(f"\n{manifest_path} actualizado con {len(all_tasks)} scrapers en total.")


if __name__ == "__main__":
    main()
