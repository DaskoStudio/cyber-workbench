> ℹ️ Dépôt vitrine — code de base / architecture ; fonctionnalités clés privées.

# Cyber Workbench

Socle public d’un workbench de cybersécurité : interface Next.js, API FastAPI et runner Go.

## ✨ Fonctionnalités

- Landing de présentation en français.
- `GET /health` répond `{"status":"ok"}`.
- `POST /api/tools/tcp-connect`, `POST /api/tools/tls-audit` et `GET /api/tools/catalog` répondent HTTP 501 `not implemented`.
- Runner avec dispatch `tcp-connect` / `tls-audit` : stubs uniquement, sans connexion réseau.

Les anciens documents décrivent une architecture cible privée ; ils ne constituent pas des fonctionnalités livrées ici. Supabase, orchestration et outils avancés ne sont pas implémentés. Le fichier `compose.yaml` historique ne s’applique pas à ce socle ; utiliser les commandes ci-dessous.

## 🧱 Structure

```text
backend/app/main.py         API et santé
backend/app/core/config.py Settings via variables CW_*
backend/app/api/routes/    Endpoints stubs
frontend/src/app/          Layout, landing et styles
runner/                   Dispatch Go sans réseau
docs/                     Documentation d’architecture historique
```

## 🚀 Lancer

Prérequis : Python 3.11+, Node.js 22+ avec npm, Go 1.22+.

Depuis la racine, dans des terminaux séparés :

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1
```

Santé : `curl http://127.0.0.1:8000/health`. Documentation API : `http://127.0.0.1:8000/docs`.
Les paramètres facultatifs `CW_APP_NAME` et `CW_ENVIRONMENT` sont lus depuis l’environnement ; aucun service externe ni secret n’est requis.

```bash
cd frontend
npm install
npm run dev -- --hostname 127.0.0.1
```

Ouvrir `http://127.0.0.1:3000`. Compilation : `npm run typecheck && npm run build`.

```bash
cd runner
go run . tcp-connect
go run . tls-audit
```

Chaque commande reconnue affiche `not implemented` et termine en échec volontaire. Aucun scan ni audit réel n’est effectué.

## 🛠️ Stack

Next.js · React · TypeScript · Tailwind CSS (dépendance disponible, styles CSS simples) · FastAPI · Pydantic Settings · Go.

## 👤 Auteur

Konaté Adama (@DaskoStudio) — Ynov Campus
