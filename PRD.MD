# Product Requirements Document (PRD) : Cyber Workbench

## 1. Vision du Projet
Cyber Workbench est un "Système d'Exploitation Web" modulaire pour les professionnels de la cybersécurité (Pentesteurs, SOC, OSINT, Bug Bounty). Il unifie 10 domaines de la sécurité dans une seule interface de type "Command Center".
La plateforme se base sur un système de **Plugins** (WASM, Cloud, Agent Local) permettant d'enchaîner les outils sans quitter le navigateur, tout en garantissant l'OPSEC via une gestion avancée de proxys.

## 2. Architecture Technique Détaillée

Le système repose sur un modèle "Zero Trust" à 3 niveaux d'exécution :

### A. Frontend (Niveau 1 : Navigateur / WASM)
*   **Stack :** Next.js (React), TypeScript, Tailwind CSS, shadcn/ui.
*   **State Management :** Zustand (pour l'état du Workspace et des résultats en cours).
*   **Exécution Client-Side :** Utilisation de WebAssembly (WASM) pour les outils de traitement de texte, encodage (Base64/Hex), cryptographie et manipulation de regex.
*   **Avantage :** Vitesse instantanée, zéro coût serveur, confidentialité totale.

### B. Backend API & Workers (Niveau 2 : Cloud OSINT)
*   **Stack :** Python (FastAPI), Celery, Redis.
*   **Base de Données :** Supabase (PostgreSQL) avec Row Level Security (RLS).
*   **Exécution Cloud :** Pour les outils OSINT passifs (DNS, WHOIS, scraping léger).
*   **OPSEC & Routing :** Intégration d'API de proxys résidentiels rotatifs (ex: BrightData) pour éviter le rate-limiting des requêtes backend.

### C. Le "Local Runner" (Niveau 3 : Agent Local & OffSec)
*   **Stack :** Golang. Binaire compilé autonome (Windows, macOS, Linux).
*   **Communication :** Connexion au frontend via WebSockets (`gorilla/websocket`).
*   **Exécution :** Exécute les commandes shell lourdes (Nmap, requêtes web mutées, scripts Python locaux) depuis la machine de l'utilisateur.
*   **OPSEC :** Support BYOP (Bring Your Own Proxy). L'agent peut wrapper son trafic sortant via SOCKS5/HTTP configuré par l'utilisateur.

## 3. Schéma de la Base de Données (Supabase)
*   **`users` :** id, email, tier (free, pro, elite), created_at.
*   **`workspaces` :** id, user_id, name, encrypted_data (JSON chiffré contenant l'historique des requêtes et résultats de la session).
*   **`plugins_custom` :** id, user_id, manifest_json (pour les utilisateurs Pro qui ajoutent leurs propres scripts).

## 4. Modèle de Plugin (Manifest Standard)
Chaque outil est un module JSON. Le frontend lit ce JSON pour générer l'interface dynamiquement.

```json
{
  "id": "osint-dns-lookup",
  "name": "Advanced DNS & Subdomain Lookup",
  "category": "osint",
  "tier": "free",
  "execution": {
    "layer": "cloud",
    "endpoint": "/api/tools/dns",
    "requires_proxy": true
  },
  "inputs": [{"name": "domain", "type": "string", "regex": "^[a-z0-9.-]+\\.[a-z]{2,}$"}],
  "outputs": [{"name": "records", "type": "json_table"}]
}
```

## 5. Monétisation (SaaS)
*   **Tier 1 (Gratuit) :** Outils WASM + OSINT Cloud basique (IP standard). Pas de sauvegarde.
*   **Tier 2 (Pro) :** Workspaces persistants (E2EE), pipelines visuels, export PDF, Agent Local Go, BYOP proxy.
*   **Tier 3 (Elite) :** Réseau de proxys résidentiels illimité (intégré au Cloud API), automatisation des scans de masse, Multi-Targeting.
*   **Paiement :** Lemon Squeezy (FIAT/TVA) + BTCPay Server / NowPayments (Crypto pour l'anonymat).

## 6. Légal & Contraintes
*   **Strictement Passif sur le Cloud :** Le serveur ne lance JAMAIS de scans de ports ou d'attaques.
*   **Déport de Responsabilité :** Tout scan actif (Bruteforce, Fuzzing) exige l'activation du Local Runner (la requête part de l'IP du client).
*   **Purge des logs :** Conservation maximale des logs Cloud pour les tâches asynchrones : 72 heures.