const STATE_LABELS = {
  ok: "OK",
  error: "Error",
  running: "Corriendo",
  revisar: "Revisar (colgado?)",
  nunca_ejecutado: "Nunca ejecutado",
  desconocido: "Desconocido",
};

const grid = document.getElementById("taskGrid");
const summaryEl = document.getElementById("summary");
const logModal = document.getElementById("logModal");
const logModalTitle = document.getElementById("logModalTitle");
const logModalBody = document.getElementById("logModalBody");
document.getElementById("logModalClose").addEventListener("click", closeLogModal);
logModal.addEventListener("click", (e) => { if (e.target === logModal) closeLogModal(); });

let pollTimer = null;

function fmtDate(iso) {
  if (!iso) return "-";
  const d = new Date(iso);
  return d.toLocaleString("es-CL", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
}

function fmtDuration(seconds) {
  if (seconds === null || seconds === undefined) return "-";
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  const m = Math.floor(seconds / 60);
  const s = Math.round(seconds % 60);
  return `${m}m ${s}s`;
}

function renderSummary(tasks) {
  const counts = { total: tasks.length, ok: 0, running: 0, error: 0 };
  tasks.forEach((t) => {
    const state = t.status.state;
    if (state === "ok") counts.ok++;
    else if (state === "running") counts.running++;
    else if (state === "error" || state === "revisar") counts.error++;
  });
  summaryEl.querySelectorAll(".chip").forEach((chip) => {
    const key = chip.dataset.key;
    chip.querySelector(".chip-value").textContent = counts[key] ?? 0;
  });
}

function cardTemplate(task) {
  const status = task.status;
  const state = status.state || "desconocido";
  const label = STATE_LABELS[state] || state;
  const isRunning = state === "running";

  const card = document.createElement("article");
  card.className = `card state-${state}`;
  card.dataset.id = task.id;

  card.innerHTML = `
    <div class="card-top">
      <div>
        <div class="card-name">${task.name}</div>
        <div class="card-schedule">${task.schedule || ""}</div>
      </div>
      <span class="status-dot"></span>
    </div>
    <div class="card-meta">
      <span class="state-label">${label}</span>
      <span>Ultima corrida: ${fmtDate(status.start)}</span>
      <span>Duracion: ${fmtDuration(status.duration_seconds)}</span>
    </div>
    <div class="card-actions">
      <button class="btn" data-action="log">Ver log</button>
      <button class="btn btn-primary" data-action="run" ${isRunning ? "disabled" : ""}>
        ${isRunning ? "Corriendo..." : "Ejecutar ahora"}
      </button>
    </div>
  `;

  card.querySelector('[data-action="log"]').addEventListener("click", () => openLogModal(task));
  card.querySelector('[data-action="run"]').addEventListener("click", (e) => runTask(task, e.target));

  return card;
}

async function loadTasks() {
  try {
    const res = await fetch("/api/tasks");
    if (res.status === 401) { window.location.href = "/login"; return; }
    const tasks = await res.json();
    grid.innerHTML = "";
    tasks.forEach((t) => grid.appendChild(cardTemplate(t)));
    renderSummary(tasks);

    const anyRunning = tasks.some((t) => t.status.state === "running");
    schedulePoll(anyRunning ? 4000 : 15000);
  } catch (err) {
    console.error("Error cargando tareas", err);
    schedulePoll(15000);
  }
}

function schedulePoll(delay) {
  if (pollTimer) clearTimeout(pollTimer);
  pollTimer = setTimeout(loadTasks, delay);
}

async function runTask(task, buttonEl) {
  buttonEl.disabled = true;
  buttonEl.textContent = "Lanzando...";
  try {
    const res = await fetch(`/api/tasks/${task.id}/run`, { method: "POST" });
    const data = await res.json();
    if (!data.ok) {
      alert(`No se pudo lanzar "${task.name}": ${data.error || "error desconocido"}`);
    }
  } catch (err) {
    alert(`No se pudo lanzar "${task.name}": ${err}`);
  }
  setTimeout(loadTasks, 1200);
}

async function openLogModal(task) {
  logModalTitle.textContent = task.name;
  logModalBody.textContent = "Cargando...";
  logModal.classList.add("open");
  try {
    const res = await fetch(`/api/tasks/${task.id}/log?lines=300`);
    const data = await res.json();
    logModalBody.textContent = data.log || "(sin contenido)";
    logModalBody.scrollTop = logModalBody.scrollHeight;
  } catch (err) {
    logModalBody.textContent = `Error cargando el log: ${err}`;
  }
}

function closeLogModal() {
  logModal.classList.remove("open");
}

loadTasks();
