# Engineering Projects & Systems Portfolio
**Distributed Systems · Production Microservices · Autonomous Agents**

A consolidated technical archive documenting the end-to-end architecture, implementations, and verified pipelines across my flagship engineering systems.

---

## 🏗️ Master Architecture Map

```
Flagship Systems/
├── 1. AuraFlow                      # Distributed Heterogeneous DAG Workflow Orchestrator
├── 2. Lead Ingestion Service        # Hardened High-Throughput REST Ingestion & Observability Microservice
└── 3. Local PC Assistant            # Cross-Platform Desktop Automation & Local Agent Controller
```

---

## 1. AuraFlow (`auraflow`)
*Distributed Heterogeneous DAG Workflow Orchestrator*  
**Repository:** [github.com/rahuldegra1/auraflow](https://github.com/rahuldegra1/auraflow)

### System Overview
A fault-tolerant distributed DAG workflow orchestrator engineered to coordinate dependencies across isolated sandboxed execution environments (CPU) and dynamic batching pipelines (GPU / CUDA), complete with durable state persistence and distributed concurrency locking.

```
                 +------------------------------------+
                 |       AuraFlow Control Plane       |
                 |  (FastAPI / SQLAlchemy Async ORM)  |
                 +-----------------+------------------+
                                   |
                     +-------------+-------------+
                     |                           |
              +------v------+             +------v------+
              | PostgreSQL  |             |  Telemetry  |
              | (16 Alpine) |             | Prometheus  |
              +------+------+             +-------------+
                     |
+--------------------+----------------------------------+
|      Scheduler Daemon & Concurrency Controller        |
|      - Dynamic graph resolver (Kahn's Topological)    |
|      - Distributed lease coordinator (SKIP LOCKED)    |
|      - Orphan sweeper & DLQ recovery                  |
+--------------------+----------------------------------+
                     |
                     | gRPC (HTTP/2 streaming)
                     v
+-------------------------------------------------------+
|                 AuraFlow Worker Nodes                 |
|      +---------------------+ +---------------------+  |
|      | Subprocess Sandbox  | | Dynamic Batching    |  |
|      | (CPU Workloads)     | | (CUDA VRAM Guard)   |  |
|      +---------------------+ +---------------------+  |
+-------------------------------------------------------+
```

### Key Capabilities & Mechanics
* **Dynamic GPU Batching**: Aggregates incoming inference requests into batches (up to $N = 4$ or within an adaptive $\Delta t = 30\text{ ms}$ window), yielding a **2.87x lower pipeline latency** and **2.63x higher token throughput** than sequential execution while safeguarding against CUDA Out-of-Memory (OOM) crashes.
* **Race-Free Concurrency**: Atomic lease acquisition via PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED` eliminates contention and distributed deadlocks across concurrent workers.
* **Orphan Sweeper & Dead Letter Queue (DLQ)**: Autonomous daemon tracks worker heartbeat health ($T > 30\text{ s}$), recovering interrupted tasks or safely routing poisoned executions to the DLQ.
* **Dependency Chaining**: Dynamic Jinja-style parameter resolution (`{{upstream_task.output_key}}`) links outputs between arbitrary pipeline steps.
* **Task Hardening**: Cryptographic payload verification via HMAC-SHA256 and AST scanning to neutralize malicious shell escapes and process injections prior to execution.

---

## 2. Production Lead Ingestion Service (`lead-ingestion-service`)
*Hardened High-Throughput REST Ingestion & Observability Microservice*  
**Repository:** [github.com/rahuldegra1/lead-ingestion-service](https://github.com/rahuldegra1/lead-ingestion-service)

### System Overview
A containerized FastAPI backend microservice backed by PostgreSQL persistence, zero-downtime database migrations, custom rate limiting, constant-time API security, and an automated GitHub Actions CI/CD test harness.

```
Incoming Request
│
▼
┌───────────────────────────────────────────────┐
│ Observability Middleware                      │
│ - Injects X-Request-ID                        │
│ - Tracks execution duration (X-Process-Time) │
│ - Prometheus latency & error counters         │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│ SlowAPI Rate Limiting (Burst & abuse control) │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│ Auth Layer (secrets.compare_digest)           │
│ - Constant-time check on X-API-Key header     │
│ - Public endpoints (/health, /metrics) exempt │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│ FastAPI Core & Pydantic v2 Pipeline          │
│ - Strict payload sanitization & validation    │
│ - E.164 phone formatting & currency cleanups  │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│ PostgreSQL 16 (SQLAlchemy 2.0 ORM)            │
│ - Composite B-Tree indexing (EXPLAIN ANALYZE) │
│ - Automatic migration on boot (alembic)       │
└───────────────────────────────────────────────┘
```

### Key Capabilities & Mechanics
* **Data Sanitization & Integrity**: Pydantic v2 validators normalize dirty payloads, enforce uppercase/lowercase standards, and sanitize currency strings into integer units.
* **Side-Channel Timing Defense**: Enforces custom API key authentication via Python’s `secrets.compare_digest` across protected CRUD routes (`POST /leads`, `GET /leads`, `PATCH /leads/{id}`, `DELETE /leads/{id}`).
* **Observability & Health Probes**:
  * `/health`: Live database readiness ping (`SELECT 1`) returning `503 Service Unavailable` on connection drop.
  * `/metrics`: Native Prometheus endpoint exposing HTTP request rates, response times, and status distributions.
  * Custom distributed tracing middleware injecting `X-Request-ID` and `X-Process-Time` headers on every response.
* **Container Hardening**: Multi-stage `python:3.12-slim` Docker image stripped of build toolchains and executed under an unprivileged user (`appuser`, UID `10000`).
* **Automated CI/CD Quality Gate**:
  * Ruff linting and formatting enforcement.
  * 14 Pytest unit/integration tests running against an isolated in-memory SQLite `StaticPool` (preventing fixture collisions and unmocked network socket hangs).
  * End-to-end integration smoke tests running inside Docker Compose.

---

## 3. Local PC Assistant (`agent_workspace`)
*Cross-Platform Desktop Automation & Local Agent Controller*  
**Repository:** [github.com/rahuldegra1/agent_workspace](https://github.com/rahuldegra1/agent_workspace)

### System Overview
A cross-platform desktop automation assistant combining CustomTkinter, local Small Language Models (SLMs via Ollama), and OS-native UI automation to execute multi-step desktop tasks.

### Key Capabilities & Mechanics
* **Pluggable Model Architecture**: Supports zero-overhead provider switching between local inference (`qwen2.5-coder:7b` via Ollama) and remote endpoints (OpenAI, Gemini, Anthropic, or OpenAI-compatible gateways) through `.pc_assistant/model_config.json`.
* **Desktop Vision & Interaction**:
  * Integrated Tesseract OCR and Windows UI Automation (`uiautomation` / `pynput` / `pyautogui`) for coordinate mapping and button targeting.
  * Automatic desktop shortcut discovery and double-click launching.
* **Safety & Privacy Shields**:
  * Screen capture sanitizer masks sensitive fields (passwords, tokens, API keys, credit cards, bank forms) using bounding box heuristics and regex scrubbing.
  * Shell safety guard blocks arbitrary command execution, constraining system calls strictly to an allowlist (`git`, `notepad`, `code`, `python`).
* **Emergency Halt & Isolation**:
  * Low-level global hotkey listener (`Ctrl+Alt+Shift+Q`) immediately terminates controller operations and spawns.
  * Packaged into a standalone Windows executable (`PC Assistant.exe`) via automated PyInstaller PowerShell workflows (`build_windows_app.ps1`).

---

## 🛠️ Consolidated Technology Stack

| Domain | Technologies & Libraries |
|---|---|
| **Languages & Runtimes** | Python 3.12, PowerShell, Bash, SQL, C |
| **Backend & Web APIs** | FastAPI, Flask, Pydantic v2, Uvicorn, gRPC, Protobuf, HTTPX |
| **Databases & ORM** | PostgreSQL 16, SQLite, SQLAlchemy 2.0 (Async/Sync), Alembic, Redis |
| **Observability & Security** | Prometheus, SlowAPI, `secrets.compare_digest`, Structured Logging |
| **Automation & Agentic Tools** | CustomTkinter, PyAutoGUI, Windows UI Automation, Tesseract OCR, PyInstaller |
| **Container & CI/CD** | Docker, Docker Compose, Multi-stage builds, GitHub Actions |
| **Testing & Quality** | Pytest, TestClient, Ruff, Mypy |
