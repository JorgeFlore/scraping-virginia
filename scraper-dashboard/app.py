#!/usr/bin/env python
"""
app.py - Panel web para visualizar y lanzar los scrapers.

Lee manifest.json para saber que scrapers existen, lee el status.json que
escribe wrapper.py para mostrar el estado de cada uno, y permite relanzarlos
manualmente disparando la tarea correspondiente en el Programador de tareas
de Windows (schtasks /run) - por lo que respeta los permisos/credenciales
que ya tengas configurados alli.
"""

import json
import os
import subprocess
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "manifest.json"

app = Flask(__name__)
app.secret_key = os.environ.get("DASHBOARD_SECRET_KEY", "cambia-esta-clave")
ADMIN_PASSWORD = os.environ.get("DASHBOARD_PASSWORD")

STALE_MINUTES = 120  # si algo queda en "running" mas de esto, se marca para revisar


def load_tasks():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("tasks", [])


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        error = "Contrasena incorrecta"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


def read_status(log_dir: Path) -> dict:
    status_path = log_dir / "status.json"
    if not status_path.exists():
        return {"state": "nunca_ejecutado"}
    try:
        with open(status_path, "r", encoding="utf-8") as f:
            status = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"state": "desconocido"}

    if status.get("state") == "running" and status.get("start"):
        try:
            start_dt = datetime.fromisoformat(status["start"])
            elapsed_min = (datetime.now() - start_dt).total_seconds() / 60
            if elapsed_min > STALE_MINUTES:
                status["state"] = "revisar"
        except ValueError:
            pass
    return status


@app.route("/api/tasks")
@login_required
def api_tasks():
    tasks = load_tasks()
    out = []
    for t in tasks:
        status = read_status(Path(t["log_dir"]))
        out.append({**t, "status": status})
    return jsonify(out)


@app.route("/api/tasks/<task_id>/run", methods=["POST"])
@login_required
def api_run_task(task_id):
    tasks = {t["id"]: t for t in load_tasks()}
    task = tasks.get(task_id)
    if not task:
        return jsonify({"ok": False, "error": "Scraper no encontrado"}), 404

    scheduler_name = task["task_scheduler_name"]
    host = task.get("host")  # si esta seteado, dispara la tarea en ese servidor remoto

    cmd = ["schtasks"]
    if host:
        cmd += ["/s", host]
    cmd += ["/run", "/tn", scheduler_name]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return jsonify({"ok": False, "error": detail or f"schtasks devolvio codigo {result.returncode}"}), 500

    return jsonify({"ok": True})


@app.route("/api/tasks/<task_id>/log")
@login_required
def api_task_log(task_id):
    tasks = {t["id"]: t for t in load_tasks()}
    task = tasks.get(task_id)
    if not task:
        return jsonify({"ok": False, "error": "Scraper no encontrado"}), 404

    log_dir = Path(task["log_dir"])
    logs = sorted(log_dir.glob(f"{task_id}_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        return jsonify({"ok": True, "log": "(todavia no hay logs para este scraper)", "file": None})

    n_lines = int(request.args.get("lines", 200))
    with open(logs[0], "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    tail = "".join(lines[-n_lines:])
    return jsonify({"ok": True, "log": tail, "file": logs[0].name})


if __name__ == "__main__":
    # Para pruebas. En produccion usar waitress o correrlo como servicio (ver README.md)
    app.run(host="0.0.0.0", port=5000, debug=False)
