# Cyber Workbench

> A modular cybersecurity workbench: browser-side analysis tools, passive cloud lookups and a sandboxed Go runner behind a single interface.

![Status](https://img.shields.io/badge/status-showcase-38f0c0?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![Go](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat-square&logo=go&logoColor=white)

> **ℹ️ Showcase repository.** This is the *public skeleton* of a private project: it shows the architecture, the service boundaries and the technical choices. The tool implementations, the network logic and the key features stay private — every endpoint here is a stub that answers `501 Not Implemented`.

---

## Table of contents

- [Overview](#overview)
- [Architecture](#architecture)
- [What this repository contains](#what-this-repository-contains)
- [Documented target platform](#documented-target-platform)
- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Tech stack](#tech-stack)
- [Design principles](#design-principles)

## Overview

Cyber Workbench is designed as a single workspace where security analysts run small, focused tools: decode and inspect data, analyse headers and certificates, look up passive OSINT sources, and run network checks through a local runner. The goal is a consistent interface and a strict execution contract for every tool, rather than a pile of unrelated scripts.

## Architecture

```text
┌──────────────────────┐        HTTPS         ┌─────────────────────────┐
│  Frontend (Next.js)  │ ───────────────────► │   API (FastAPI)         │
│  React + TypeScript  │                      │   /health               │
│  tool catalogue, UI  │ ◄─────────────────── │   /api/tools/*          │
└──────────────────────┘                      └────────────┬────────────┘
                                                           │ dispatch
                                              ┌────────────▼────────────┐
                                              │   Runner (Go)           │
                                              │   sandboxed network     │
                                              │   checks (tcp, tls)     │
                                              └─────────────────────────┘
```

Three execution modes are described in the design documents:

| Mode | Where it runs | Used for |
|---|---|---|
| **Browser** | Client side (JavaScript) | Offline analysis of pasted data — nothing leaves the machine |
| **Cloud** | Backend, passive only | Public lookups (DNS, RDAP, certificate fetch) with anti-SSRF validation |
| **Runner** | Local Go binary | Network checks that must originate from the user's own machine |

## What this repository contains

| Component | Status in this repository |
|---|---|
| `GET /health` | ✅ Returns `{"status":"ok"}` |
| `GET /api/tools/catalog` | ⛔ Stub — HTTP 501 |
| `POST /api/tools/tcp-connect` | ⛔ Stub — HTTP 501 |
| `POST /api/tools/tls-audit` | ⛔ Stub — HTTP 501 |
| Go runner (`tcp-connect`, `tls-audit`) | ⛔ Command dispatch only, **no network code** |
| Next.js frontend | ✅ Landing page |
| Settings (`CW_*` environment variables) | ✅ Pydantic Settings |

The older documents in `docs/` describe the *target* private architecture. They are not features shipped in this repository. Supabase integration, orchestration and the advanced tools are **not** implemented here, and the historical `compose.yaml` does not apply to this skeleton — use the commands below.

## Documented target platform

The design documents ([`PRD.MD`](PRD.MD), [`ETAT_PROJET.md`](ETAT_PROJET.md), [`docs/CATALOGUE_OUTILS.md`](docs/CATALOGUE_OUTILS.md), [`docs/E2EE.md`](docs/E2EE.md)) describe the full platform:

- **53 tools across 10 domains**, among them OSINT & recon, web application security, network & infrastructure, cryptography & encoders, blue team & forensics, cloud & DevSecOps, threat intelligence & GRC and mail security.
- Most tools run **in the browser** (45 of 53), a few use passive cloud lookups, and the network tools go through the **runner**.
- A **plan-based access model** (free / pro / elite) filtering the catalogue and the sidebar.
- A strict **execution contract** per tool: declared inputs, size limits and output format.
- Privacy by design: pasted data stays client side whenever the tool allows it.

## Getting started

**Prerequisites:** Python 3.11+, Node.js 22+ with npm, Go 1.22+. No secret or external service is required.

### 1. API

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1
```

```bash
curl http://127.0.0.1:8000/health      # {"status":"ok"}
```

Interactive API docs: <http://127.0.0.1:8000/docs>. The optional `CW_APP_NAME` and `CW_ENVIRONMENT` variables are read from the environment (see `backend.env.example`).

### 2. Frontend

```bash
cd frontend
npm install
npm run dev -- --hostname 127.0.0.1
```

Open <http://127.0.0.1:3000>. Production check: `npm run typecheck && npm run build`.

### 3. Runner

```bash
cd runner
go run . tcp-connect
go run . tls-audit
```

Each recognised command prints `not implemented` and exits with a deliberate failure code. No scan or audit is performed.

## Project structure

```text
backend/app/main.py          API entry point and health check
backend/app/core/config.py   Settings loaded from CW_* variables
backend/app/api/routes/      Endpoint stubs (tools)
frontend/src/app/            Layout, landing page, styles
runner/                      Go command dispatch (no network code)
docs/                        Historical architecture documentation
config/ scripts/ supabase/   Reserved placeholders
```

## Tech stack

Next.js · React · TypeScript · FastAPI · Pydantic Settings · Go

## Design principles

- **Explicit execution contracts** — every tool declares what it accepts and returns.
- **Least privilege** — network access is isolated in a separate runner process.
- **Passive by default** — cloud lookups are read-only and validated against SSRF.
- **Honest scope** — this repository documents what is *not* included as clearly as what is.

---

**Author** — Konaté Adama · [github.com/DaskoStudio](https://github.com/DaskoStudio)
