# État actuel — 16 octobre 2026

Cette synthèse décrit le code actuel. Les sections datées plus bas sont l’historique : leurs anciens nombres d’outils et points de reprise ne décrivent plus le catalogue courant.

## Troisième recette Tor et fixtures SSR — 19 octobre 2026

**Validation partielle ; isolation non validée.** 132 tests backend réussis / 6 ignorés,
62 tests frontend réussis et 7 tests Chromium réussis dans la nouvelle configuration
`playwright.tor.config.ts`. Lint sans erreur (un avertissement préexistant),
TypeScript et build de production isolé (`CW_E2E=1 npm run build`) réussis.
Les fixtures passent par le SDK Supabase, ses cookies,
`proxy.ts` et le layout protégés ; aucun contournement produit. Auth et DNS sont
simulés pour ces tests navigateur. Séparément, quatre tests d'intégration passent
ensemble avec un exécuteur local temporaire et Tor réel (`IsTor=true`). Le test de
panne qui modifiait le mauvais processus a été corrigé ; le runbook utilise
désormais un service de test Compose dédié (unittest, montage en lecture seule).

Docker demeure inaccessible : build des conteneurs, isolation effective,
observation des sorties et coupure du daemon restent à vérifier. Deux points de
budgets sont documentés : timeout frontend non composé avec le signal de l'outil,
et verrou Celery 35 s pour une tâche limitée à 50/60 s. L'ancienne suite Playwright
globale n'est pas migrée ni déclarée verte. Détails et limites :
[VALIDATION_TOR_SSR.md](VALIDATION_TOR_SSR.md). Aucun `.env` existant modifié ni commit.

## Seconde recette Tor — 19 octobre 2026

**Non validé pour livraison.** Le composant DNS-Tor fonctionne via Tor réel sur localhost ; le mode async est conservé dans une reproduction simulée. 132 tests backend réussis / 6 ignorés, 62 tests frontend réussis ; deux tests Playwright en échec et contamination d’environnement dans la suite d’intégration du composant. Isolation Docker non exécutée (moteur inaccessible). Cette recette remplace les constats antérieurs sur la perte du mode async et le script absent de l’image. Détails : [VALIDATION_TOR_COMPOSANT.md](VALIDATION_TOR_COMPOSANT.md).

## Validation Tor — 19 octobre 2026

**Livraison non validée.** Transport Tor synchrone testé avec le réseau réel, mais routage perdu dans les tâches asynchrones, exécution applicative non isolée, script de vérification absent de l’image et Playwright DNS en échec. Résultats et reproductions dans [VALIDATION_TOR.md](VALIDATION_TOR.md).

## Correction CORS navigateur local — 17 octobre 2026

Le diagnostic des précontrôles refusés a relevé `Origin: http://127.0.0.1` (sans port), alors que la page Chrome affichait `127.0.0.1:3000`. La liste autorisait seulement `http://127.0.0.1:3000` et `http://localhost:3000`. La cause de cette réécriture côté navigateur/intermédiaire n’est pas établie ; le refus d’origine, lui, est confirmé dans les logs. Le test initial avec le port 3000 ne reproduisait donc pas la requête en erreur.

- **Tentative remplacée** : accepter l’origine sans port supprimait le refus du précontrôle mais Chrome signalait ensuite une origine de réponse différente de celle de la page. Cette exception a été retirée, y compris pour les WebSockets.
- **Présent et testé — relais HTTP local** : en `npm run dev`, le client utilise `/api/...` sur l’origine du frontend. Next.js relaie ces appels vers `NEXT_PUBLIC_API_URL` (par défaut `http://127.0.0.1:8000`). Le navigateur n’effectue plus d’appel HTTP inter-origines à FastAPI. Les tokens Bearer restent vérifiés par FastAPI ; aucun droit n’est déduit du relais. La production conserve l’adresse API absolue et sa configuration CORS explicite. Les WebSockets du runner restent directs et ne sont pas couverts par cette correction.
- **Présent** : logs CORS limités à l’origine, la méthode et le motif du refus, sans token/cookie/corps. L’interface affiche « Accès non vérifié » et une erreur avec bouton Réessayer, au lieu de présenter le repli prudent comme un abonnement Gratuit confirmé.
- **Tests** : cinq tests unittest pour les origines autorisées/refusées et les diagnostics ; deux tests frontend pour les URL de relais et le refus des destinations hors API. Suite backend : 97 tests, 95 réussis et 2 opt-in ignorés. Frontend : 62 tests réussis, TypeScript réussi, lint sans erreur (un avertissement préexistant dans `auth-panel.tsx`). Build de production réussi avec `CW_E2E=1 npm run build` (sortie isolée `.next-e2e` pour préserver le serveur de développement), après mise à l’écart de ses anciens types générés.
- **Recette locale** : via le port 3000, `/api/health` répond 200 et `/api/auth/me` sans token répond 401. Après rechargement de la session réelle du navigateur intégré, l’administration et les accès Elite sont présents ; les appels de profil et d’administration répondent 200. Le Chrome personnel n’est pas accessible à l’automatisation : sa validation reste à confirmer après rechargement. La cause de l’origine sans port n’a pas été identifiée.
- Aucun `.env` modifié. Le token visible dans la capture utilisateur n’a pas été copié ni utilisé. L’avertissement CSP montré dans Chrome est distinct ; aucune règle CSP n’a été assouplie.

## Correction administration — 17 octobre 2026

- **Présent et testé** : les identités authentifiées dont l’email appartient à `ADMIN_EMAILS` reçoivent un accès effectif Elite côté serveur, sans créer ni modifier de commande de paiement. La politique est partagée par `/api/auth/me`, les dépendances Pro/Elite, les workspaces, configurations, tâches, quotas cloud et la revérification du runner. Les métadonnées utilisateur ne donnent aucun droit admin. Le retrait de la liste serveur retire cet accès au prochain contrôle (recharger la configuration/processus si `.env` change).
- **Présent** : rôle admin, offre attribuée et accès effectif distincts dans le panneau ; recherche email/identifiant, filtre d’accès, dates de création/connexion, confirmation d’un changement d’offre, configuration des services et erreurs partielles explicites. Les outils inconnus ne peuvent pas être désactivés par l’endpoint admin.
- **Validations locales** : TypeScript réussi ; lint sans erreur (un avertissement préexistant dans `auth-panel.tsx`) ; 60 tests frontend réussis ; 92 tests unittest backend, dont 90 réussis et 2 opt-in ignorés. Douze nouveaux tests couvrent admin/compte ordinaire/anonyme, métadonnées forgées, retrait du rôle, dépendances payantes, runner, réponse de profil et séparation offre/accès. Les anciennes fonctions pytest de `test_admin.py` ne sont pas découvertes par unittest ; les nouveaux tests sont des TestCase.
- **Recette réelle, lecture seule** : après redémarrage de l’API, le compte connecté affiche Elite, les dix domaines et les onglets Workspaces/Pipelines/Runner/Monitoring. Le panneau affiche le rôle Admin et l’accès effectif Elite avec l’offre attribuée Gratuit. Aucune modification de compte, paiement, fournisseur ou fichier `.env` effectuée.
- **Limites** : les 200 premiers comptes seulement sont chargés. Compteurs et bascules cloud restent en mémoire, propres au processus et perdus au redémarrage ; pas de journal d’audit durable. Les états de configuration ne prouvent pas la disponibilité des services. Le proxy cloud est actuellement indiqué « À configurer » : le routage automatique Elite existant n’est pas contourné et peut refuser les outils qui en dépendent. L’accès Elite n’installe pas le runner et ne configure pas Redis/les workers. La persistance des réglages, une pagination complète et un journal d’actions durable restent à construire.

### Vérification de l’aperçu — 16 octobre 2026

L’erreur « Failed to fetch » de DNS Lookup provenait de l’API locale arrêtée : seul le frontend tournait. Après démarrage de FastAPI sur `127.0.0.1:8000`, une exécution réelle depuis le navigateur sur `127.0.0.1:3000` a renvoyé neuf enregistrements pour le domaine saisi `cloudfare.com`. Ce contrôle ne valide pas les autres services cloud ni l’appairage runner. Le client affiche maintenant une erreur explicite de connexion au service ou de délai dépassé, en conservant les erreurs métier de l’API. Lint, TypeScript et le test Playwright DNS (succès simulé, erreur HTTP et connexion refusée) passent. Aucun fichier d’environnement modifié.

## Extension des dix domaines — code livré

**Présent : 54 manifestes, soit 53 outils et une démonstration.** La salve ajoute 24 outils (20 JavaScript navigateur et 4 via le runner), sans nouvel endpoint cloud. Le catalogue complet et les limites figurent dans [CATALOGUE_OUTILS.md](CATALOGUE_OUTILS.md).

| Domaine | Outils hors démonstration | Nouveaux outils de cette salve |
| --- | ---: | --- |
| OSINT & Recon | 5 | Analyse robots.txt, inventaire CT depuis export |
| Web AppSec | 5 | Analyse HAR |
| Réseau & Infra | 5 | IPv6, ensembles de ports, connectivité TCP locale |
| Crypto & Encoders | 8 | Aucun changement aux outils existants |
| Blue Team & Forensics | 5 | Signatures de fichiers et entropie sur extrait hex |
| Cloud & DevSecOps | 5 | IAM, Dockerfile, inventaire SBOM |
| Threat Intel & GRC | 5 | STIX, registre de risques, tri CVE |
| MailSec | 5 | TXT DKIM, politique MTA-STS, rapport agrégé DMARC |
| Pentest (Local) | 5 | Import/comparaison Nmap, rapports ZAP/Burp, Nmap TCP local, comparaison HTTP entre rôles |
| Red Team (Local) | 5 | Plan ATT&CK, couverture de détection, lecteur BloodHound |

### Statuts et limites

- **Présent et testé — moteur navigateur** : chaque nouveau manifeste est enregistré avec son exécuteur. Les formulaires et sorties ont des exemples et limites explicites ; les imports refusent les DTD/entités XML personnalisées et bornent les volumes. L’analyse est locale, sans requête cloud d’outil. Les 500 premières lignes sont affichées, le JSON contient les données traitées complètes.
- **Présent et testé — contrats runner** : API Pydantic et Go partagent les cinq identifiants autorisés (quatre outils réseau et `local-demo`) et des paramètres propres à chaque outil. Refus des champs supplémentaires, options arbitraires, commandes shell, listes de plus de 32 ports et confirmation absente. Budget réseau de 45 s, concurrence de deux, annulation, chunks XML/JSON concaténés sans séparateur.
- **Présent et testé — périmètre local** : `-allow-network -scope` requis côté CLI. Résolution, vérification de toutes les adresses puis adresse épinglée. Le périmètre ne peut pas être élargi par le navigateur. Noms exacts ou IP/CIDR ; un nom autorise ses adresses résolues. Les outils réseau refusent un proxy configuré ; ils ne disposent pas encore du routage BYOP des sondes.
- **Présent et testé — droits d’interface** : 38 outils navigateur en Gratuit, 45 en Pro/Elite. Les domaines entièrement payants sont masqués en Gratuit ; les nombres du tableau des offres sont calculés à partir des manifestes. Les contrôles serveur du runner restent requis. Les champs Authorization HTTP sont masqués à l’écran ; leur valeur traverse l’API, sans E2EE du relais. Les entrées du formulaire ne sont pas enregistrées dans l’historique des exécutions.
- **Présent, recette incomplète — Nmap** : lancement à arguments fixes sans shell, sortie XML bornée, dépendance absente traitée explicitement. Le binaire Nmap n’est pas installé sur ce poste ; aucun véritable scan Nmap n’a été exécuté. Installation et essai dans un laboratoire autorisé restent nécessaires.
- **Incomplet — TLS et HTTP** : TLS teste seulement 1.2/1.3 avec certificat vérifié, pas toutes les suites ni les versions anciennes. HTTP compare statuts/tailles/empreintes de deux GET sans redirection ; une égalité ne prouve pas une faille d’autorisation. Les corps sont limités au premier Mio et ne sont pas restitués.
- **Incomplet — analyse statique** : IAM ne calcule pas les permissions effectives ; Dockerfile est heuristique ; SBOM n’enrichit pas les CVE. ATT&CK vérifie seulement la syntaxe des identifiants ; BloodHound lit les propriétés/ACL d’un export sans graphe ni chemin d’attaque. Le suivi des détections repose sur les preuves renseignées, pas sur une connexion EDR.
- **Absent de cette salve** : collecte AD, exploitation automatisée, scans actifs cloud, scripts utilisateur arbitraires, sondes actives via proxy, enrichissement CVE/CT externe, connexions de production. Aucun fichier `.env` modifié, aucune migration distante ou publication effectuée.

### Validations exécutées sur ce poste

- Frontend : `npm run lint`, `npx tsc --noEmit`, **59 tests Node réussis**, `npm run build` réussi (Webpack, quatre pages statiques).
- Backend : **80 tests découverts, 78 réussis et 2 tests opt-in ignorés** avec `python -m unittest discover -s tests -v`.
- Runner : **15 tests Go**, `go test -race ./...`, `go vet ./...` et compilation réussis. Les tests réseau utilisent uniquement des serveurs de boucle locale ; vérification du refus des certificats non fiables, de l’absence de redirection et des limites de corps HTTP.
- Intégration supplémentaire : `CW_LIVE_TESTS=1 python -m unittest discover -s tests -p test_live_runner.py -v` réussi. Véritable Go ↔ FastAPI ↔ client WebSocket local, TCP/HTTP locaux, cible hors périmètre refusée ; identité simulée. Le test Redis opt-in n’a pas été rejoué dans cette salve.
- Recette navigateur finale le 16 octobre : **15 tests Playwright réussis** via `npm run test:e2e`. Les vingt nouveaux analyseurs sont exécutés dans Chromium ; XML malveillant refusé, rendu HTML inerte, quatre formulaires runner et concaténation des chunks vérifiés avec WebSocket simulé. Navigation Gratuit/Pro/Elite, retrait de droits, recherche mobile et anciens parcours réussis. Ces tests simulent l’identité et les transports cloud/runner ; l’intégration réelle Go/API locale est vérifiée séparément ci-dessus.

### Point d’arrêt et décisions restantes

Le code de cette extension est préparé. La recette avec un vrai compte Supabase Pro/Elite, WSS distant, les prestataires de proxy et les autres services externes reste à réaliser. Nmap doit être installé et testé sur les OS visés. Le routage BYOP des sondes actives doit être implémenté et testé outil par outil avant d’être annoncé disponible. Les prix/prestataires, la validation des formats d’exports sur des jeux réels volumineux et un catalogue ATT&CK versionné restent des décisions ou travaux distincts ; la présente livraison ne les garantit pas.

---


## Étape 1 — Catalogue d'outils navigateur étendu — 14 octobre 2026

Extension du catalogue d'outils 100 % navigateur (layer `js`, tier gratuit),
sans aucune connexion externe ni modification du backend. Le dépôt a été
initialisé sous git et relié à github.com/DaskoStudio/Cyber_Workbench.

### Nouveaux outils (15 au total ajoutés sur deux salves)

Première salve (crypto, réseau, forensics, threat intel) :
- **Testé — JWT Decoder** : décode header/payload, signale alg:none et expiration ; signature non vérifiée.
- **Testé — Hash Generator** : SHA-1/256/384/512 via Web Crypto (SubtleCrypto), runner asynchrone.
- **Testé — Subnet / CIDR Calculator** : réseau, broadcast, masque, wildcard, plage d'hôtes IPv4.
- **Testé — Password Entropy Analyzer** : entropie, alphabet, estimation de temps de crack ; 100 % local.
- **Testé — IOC Defanger / Refanger** : neutralise/réarme URL, IP, domaines, e-mails (round-trip vérifié).
- **Testé — Timestamp Converter** : epoch (s/ms) ⇄ ISO/UTC/local + relatif.
- **Testé — Secure Token Generator** : UUID v4 et jetons hex/base64url/alphanumériques via CSPRNG.

Seconde salve (remplissage des domaines Web AppSec, MailSec, DevSecOps, Blue Team, OSINT) :
- **Testé — Security Headers Analyzer** (web-appsec) : note CSP, HSTS, anti-clickjacking, cookies, CORS et fuites de version à partir des en-têtes collés. Logique pure exportée (`analyzeSecurityHeaders`) réutilisable côté serveur à l'étape 3.
- **Testé — URL & HTML Encoder/Decoder** (web-appsec) : pourcent-URL, form, URL complète, entités HTML ; détection du double encodage.
- **Testé — Email Header Analyzer** (mailsec) : reconstruit la chaîne Received, lit SPF/DKIM/DMARC, signale Reply-To divergent et nom affiché trompeur.
- **Testé — SPF / DMARC Parser** (mailsec) : mécanismes, compte des requêtes DNS (limite de 10), politique et faiblesses.
- **Testé — Secret Scanner** (cloud-devsecops) : clés AWS/GitHub/OpenAI/Anthropic/Stripe…, clés privées PEM, identifiants d'URL ; extraits masqués, placeholders ignorés.
- **Testé — JWT Signature Verifier** (cloud-devsecops) : vérifie HS256/384/512 avec secret partagé via Web Crypto ; signale secrets triviaux et trop courts.
- **Testé — IOC Extractor** (blue-team-forensics) : extrait URL/domaines/IP/e-mails/hashs/CVE depuis des logs, reconnaît les formes defang, dédoublonne, ressort une liste neutralisée.
- **Testé — URL Inspector** (osint-recon) : décompose une URL reçue, décode le punycode et détecte l'homographe IDN, l'astuce des identifiants avant @, les sous-domaines trompeurs. Aucune requête réseau.

### Résultats locaux

- Frontend : 25 tests Node (7 existants + 18 nouveaux) passent ; lint ESLint et `tsc --noEmit` sans erreur ; build de production Webpack réussi (BUILD_ID généré, 4 pages statiques).
- Aucune règle du schéma n'a été modifiée : tous les nouveaux outils sont en layer `js` et respectent la contrainte d'un unique endpoint cloud approuvé.
- Catalogue : 4 → 19 outils. Domaines encore vides : Red Team (local). Network & Infra, Threat Intel, Web AppSec, MailSec, Cloud & DevSecOps, Blue Team et OSINT ont désormais au moins un outil.

### Suite de la feuille de route

- Étape 2 — **FAIT** : liste blanche exportée et garde anti-SSRF partagé intégrés ; détail et validations ci-dessous.
- Étape 3 : premiers outils cloud passifs (WHOIS/RDAP, SSL/TLS checker, HTTP headers en live réutilisant `analyzeSecurityHeaders`). Nécessite un réseau réel et Supabase de test pour une recette complète.

## Feuille de route et point de reprise — 14 octobre 2026

Le projet est désormais sous git (deux commits) et destiné à github.com/DaskoStudio/Cyber_Workbench.
Développement mené par salves, chaque salve testée (lint + tsc + tests Node + build pour le frontend) et commitée.

**Plan en 4 étapes :**

- **Étape 0 — FAIT.** Dépôt git initialisé, `.gitignore` vérifié (aucun secret indexé), premier commit de l'état existant.
- **Étape 1 — FAIT.** 8 outils navigateur supplémentaires remplissant Web AppSec, MailSec, Cloud & DevSecOps, Blue Team et OSINT (détail ci-dessus). Catalogue 4 → 19 outils. Aucune modification backend, aucune connexion externe.
- **Étape 2 — FAIT.** Couche cloud préparée sans ajout d’outil cloud (réalisation détaillée ci-dessous) :
  1. Dans `frontend/src/plugins/schema.ts`, remplacer la règle « endpoint cloud unique » (`m.execution.endpoint !== "/api/tools/osint/dns-lookup"`) par une liste blanche d'endpoints approuvés (constante partagée, ex. `APPROVED_CLOUD_ENDPOINTS`), pour pouvoir déclarer plusieurs outils cloud tout en gardant le refus des destinations arbitraires. Conserver et faire passer le test existant « arbitrary destination rejected ».
  2. Côté backend, ajouter un garde anti-SSRF partagé (ex. `backend/app/services/net_guard.py`) : résoudre l'hôte fourni par l'utilisateur et refuser les plages privées (RFC 1918), loopback (127/8, ::1), lien-local (169.254/16, fe80::/10), ULA (fc00::/7), CGNAT (100.64/10) et surtout l'adresse de métadonnées cloud 169.254.169.254. Le brancher dans `dns_resolver.py` et en faire le point de passage obligatoire de tout futur outil cloud.
  3. Tests backend (`python -m unittest discover -s tests`) couvrant le refus de chaque plage interdite.
- **Étape 3 — À FAIRE.** Premiers outils cloud passifs : WHOIS/RDAP, SSL/TLS checker, et HTTP Headers en live (ce dernier réutilise `analyzeSecurityHeaders` déjà exporté côté frontend dans `security-headers.ts`). Chaque outil = route FastAPI dans `backend/app/api/routes/` + logique dans `backend/app/services/` passant par le garde anti-SSRF + endpoint ajouté à la liste blanche + manifeste `layer: cloud`. Strictement passif : aucun scan de ports ni requête active. Recette complète nécessite un réseau réel et un Supabase de test.

**Contraintes permanentes :** le cloud reste strictement passif (jamais de scan actif depuis l'IP serveur, cf. PRD §6) ; tout scan actif reste réservé au runner local. Chaque salve doit laisser lint, tsc, tests Node et build du frontend au vert, et la suite unittest du backend au vert.

**Point de reprise : étape 3.** L’étape 2 est terminée et validée localement. Les futurs services cloud doivent utiliser le garde partagé avant toute utilisation d’un hôte fourni par l’utilisateur.


## Étape 2 — FAIT — Préparation de la couche cloud — 14 octobre 2026

- **Présent et testé — Liste blanche frontend** : `APPROVED_CLOUD_ENDPOINTS`, exportée et gelée dans `frontend/src/plugins/schema.ts`, contient uniquement `/api/tools/osint/dns-lookup`. La comparaison porte sur le chemin exact : URL absolue, destination arbitraire, endpoint absent, query string et slash ajouté sont refusés. Le test existant « arbitrary destination rejected » passe toujours.
- **Présent et testé — Garde partagé** : `backend/app/services/net_guard.py` expose `resolve_public_host`. Il accepte un hôte nu ou une IP, effectue uniquement une résolution DNS et renvoie les adresses publiques validées. `ipaddress` refuse RFC 1918, loopback IPv4/IPv6, lien-local, ULA, CGNAT et les métadonnées `169.254.169.254`. Les adresses non globales, multicast, réservées et certains préfixes de transition IPv6 sont aussi refusés. Les IPv4 encapsulées en IPv6 sont contrôlées après extraction de l’IPv4.
- **Présent et testé — Passage obligatoire du service DNS** : `resolve_domain_dns`, utilisé par les routes DNS et le worker, passe par le garde. Une seule IP interdite dans l’ensemble A/AAAA suffit à rejeter le résultat (HTTP 400). Les réponses du chemin direct ou DoH/proxy sont réutilisées, sans seconde résolution ni lookup système en mode proxy. Le refus du fallback direct est conservé.
- **Comportement explicite** : une réponse sans adresse A/AAAA exploitable, même avec des TXT/MX, est refusée (HTTP 502). Une erreur sur une famille A/AAAA ne peut plus être ignorée si l’autre famille répond ; l’absence confirmée d’un type de record (`NoAnswer`) reste permise. Les erreurs et délais de résolution provoquent un refus.
- **Tests** : nouveau `backend/tests/test_net_guard.py`, couvrant chaque plage demandée sous forme littérale et dans une réponse DNS mixte, les IPv4/IPv6 publiques, les formes encapsulées, les entrées mal formées, les erreurs de résolution, les deux chemins DNS et l’absence de fuite directe du mode proxy. Tests sans réseau extérieur : réponses DNS simulées, aucun contact avec les IP de test.

### Validations exécutées

- `cd frontend && npm run lint && npx tsc --noEmit && npm test && npm run build` : réussi ; **26 tests Node réussis**, compilation et TypeScript réussis, 4 pages statiques générées.
- `cd backend && source .venv/bin/activate && python -m unittest discover -s tests -v` : **43 tests recensés, 41 réussis, 2 ignorés**. Les deux tests opt-in Redis/Go nécessitant `CW_LIVE_TESTS=1` n’ont pas été exécutés pour cette étape.
- Aucun outil ni manifeste ajouté, logique des outils JS inchangée, aucun fichier `.env` modifié. Pas de scan de ports ni de connexion à une cible ajoutés. Le DoH via le fournisseur configuré reste le transport DNS existant.

### Contrat pour l’étape 3 et limites

Chaque futur service cloud doit appeler `resolve_public_host` avant d’utiliser l’hôte utilisateur. Avec un proxy, fournir un résolveur utilisant ce proxy et retournant tous les résultats A/AAAA ; il doit lever une erreur si une famille ne peut pas être résolue. Un simple contrôle DNS ne protège pas à lui seul une future connexion HTTP/TLS contre le DNS rebinding : le client devra utiliser les IP validées sans nouvelle résolution implicite, contrôler les éventuelles redirections et conserver la validation TLS. Aucun client de ce type n’est ajouté ici et aucune garantie de protection HTTP complète n’est annoncée.

Le fichier `frontend/PRD.MD` indiqué dans la demande n’existe pas dans ce dépôt : les contraintes ont été vérifiées dans `PRD.MD` à la racine. Les validations avec Supabase, un proxy réel et les services externes restent distinctes de cette étape locale.

## Étape 3 — Premiers outils cloud passifs — 14 octobre 2026

Trois outils cloud ajoutés, chacun passant par le garde anti-SSRF de l'étape 2.
Catalogue porté à 22 outils (19 navigateur + 3 cloud, dont le DNS existant → 4 cloud au total).

### Outils

- **Présent — WHOIS / RDAP** (osint-recon) : interroge le RDAP public (rdap.org, hôte fixe de confiance — l'outil ne se connecte jamais au domaine de l'utilisateur). Renvoie registrar, dates création/expiration/mise à jour, statuts et serveurs de noms. Service `rdap_client.py`, route POST `/api/tools/osint/whois`.
- **Présent — SSL / TLS Certificate Checker** (network-infra) : se connecte UNIQUEMENT à une adresse validée par `resolve_public_host`, en épinglant la connexion TCP sur cette IP tout en envoyant le vrai nom via SNI. Récupère le certificat même invalide/expiré pour le rapporter (jamais pour l'approuver). Parse émetteur, sujet, SAN, validité, jours restants, algo de signature via `cryptography`. Service `tls_inspector.py`, route POST `/api/tools/osint/tls-certificate`.
- **Présent — HTTP Security Headers (live)** (web-appsec) : récupère les en-têtes côté serveur, revalide chaque redirection avec le garde (redirections suivies manuellement, jamais automatiquement), renvoie les en-têtes bruts. La notation est faite côté frontend en RÉUTILISANT `runSecurityHeaders`/`analyzeSecurityHeaders` déjà écrit à l'étape 1 (zéro duplication). Service `http_inspector.py`, route POST `/api/tools/osint/http-headers`.

### Intégration

- `APPROVED_CLOUD_ENDPOINTS` (schema.ts) étendue aux trois nouveaux endpoints ; destinations arbitraires toujours rejetées (test couvert).
- `execute.ts` généralisé : le cloud ne code plus en dur la forme DNS. Cas DNS historique conservé par rétro-compatibilité ; cas général = passage direct des sorties du backend ; cas headers live = post-traitement par l'analyseur client-side.
- `cryptography` déjà présent dans requirements.txt.

### Résultats locaux

- Backend : 13 tests net_guard + 6 tests recon (RDAP parsing + 404, suivi de redirection HTTP + rejet d'hôte privé via le garde, certificat TLS valide + expiré parsés depuis un certificat auto-signé généré dans le test) — tous OK. Suite complète (fastapi/celery/supabase) non relançable dans la VM Linux d'ici (venv macOS).
- Frontend : 27 tests Node OK, lint et tsc sans erreur, build de production réussi.

### Limites (recette réseau réelle requise)

- Aucune vérification réseau RÉELLE n'a été exécutée depuis cette VM : les tests mockent le réseau. WHOIS/TLS/HTTP doivent être testés en direct sur une machine avec accès réseau (et idéalement Supabase de test).
- Protection DNS-rebinding : TLS épingle sur l'IP validée (robuste) ; HTTP revalide l'hôte avant chaque requête mais laisse une petite fenêtre TOCTOU à fermer au déploiement (épinglage socket), documentée en tête de `http_inspector.py`.

**Point de reprise : étape 3 livrée côté code, recette réseau réelle à faire sur machine.** Suite logique : brancher un Supabase de test et faire la recette des outils cloud en conditions réelles (feuille de route d'origine : connexions externes et staging).

## Affichage des 10 domaines + mode dev — 14 octobre 2026

- **Présent — Les 10 domaines sont affichés** dans la sidebar. Les deux domaines locaux (Pentest, Red Team) s'affichent avec un cadenas et le badge « Pro » quand le tier est inférieur à Pro ; leur panneau montre un message d'offre Pro au lieu d'être vide. Avant, ils étaient totalement masqués aux comptes gratuits.
- **Présent — Override de tier côté interface, dev uniquement** : `NEXT_PUBLIC_DEV_TIER` (free|pro|elite) et un sélecteur visible seulement quand `NODE_ENV !== "production"` (`DevTierSwitcher`). `AccessProvider` respecte l'override et saute l'appel `/api/auth/me`. Ne débloque QUE l'affichage ; les contrôles API/RLS restent intacts.
- **Présent — Override d'entitlement côté API, dev uniquement** : réglage `DEV_FORCE_TIER` (pro|elite) honoré seulement si `APP_ENV=development`, court-circuitant `entitlement_for` sans appel Supabase. Ignoré en production (test couvert).
- **Testé** : 3 tests backend (`test_dev_tier`) : octroi en dev, ignoré en prod, valeur invalide ignorée. Frontend : 27 tests, lint, tsc, build OK.
- Sécurité : les trois mécanismes sont strictement dev-only (gardes `NODE_ENV`/`APP_ENV`) et ne modifient rien en production. Pour tester le Local Runner de bout en bout, il faut en plus appairer l'agent Go.

## 8 outils supplémentaires + Red Team rempli — 14 octobre 2026

Catalogue porté à 30 outils. Tous les domaines ont désormais au moins un outil ;
Red Team est rempli avec des outils analytiques **non-offensifs** (choix de sécurité
explicite : aucun générateur d'exploit, de payload, de cassage ou de C2).

### Nouveaux outils navigateur (tier gratuit sauf mention)

- **Testé — CVSS v3.1 Calculator** (threat-intel-grc) : score de base et sévérité depuis un vecteur. Logique partagée `cvss.ts` (vérifiée contre la spec : 10.0, 9.8, Low).
- **Testé — User-Agent Parser** (blue-team) : navigateur, OS, type d'appareil, détection de bot.
- **Testé — Log Parser** (blue-team) : Apache/Nginx combined et syslog → tableau, top IP, comptage de statuts.
- **Testé — Magic Decoder** (crypto) : pèle automatiquement les couches Base64/Base64URL/Hex/URL et s'arrête au texte clair (ROT13 volontairement exclu de la détection auto car sans signature).
- **Testé — Classical Cipher** (crypto) : ROT13, César (+ force brute), Atbash, XOR, Vigenère ; round-trips vérifiés.
- **Présent — CORS & Cookie Analyzer** (web-appsec) : config CORS et attributs de cookies (réutilise `parseRawHeaders`).

### Nouveaux outils Red Team (tier Pro, non-offensifs)

- **Testé — Payload Analyzer** (red-team-local) : décode un payload capturé (PowerShell -enc UTF-16LE, désobfuscation) et met en évidence les indicateurs suspects. Analyse statique, jamais exécuté, rien n'est transmis.
- **Présent — Pentest Report Builder** (red-team-local) : transforme un finding en section de rapport Markdown avec sévérité CVSS (réutilise `cvss.ts`).

### Résultats

- Frontend : 34 tests Node (7 nouveaux), lint et tsc sans erreur, build de production réussi. Catalogue 22 → 30 outils.
- Les deux outils Red Team sont en tier Pro : affichés avec le cadenas, exécutables par un compte Pro (ou via l'override dev). Ils tournent 100 % navigateur, sans runner.
- Choix de sécurité : aucun outil offensif (exploit, payload, cassage, C2) n'est fourni ; le domaine Red Team reste analytique/défensif.

## Quotas par tier + comparatif d'offres — 14 octobre 2026

Première brique du renforcement de la valeur par offre (demande : différencier Free/Pro/Elite au-delà de quelques fonctionnalités).

- **Testé — Quotas de requêtes cloud par offre** : `TIER_RPM` dans `rate_limit.py` (Free 15, Pro 60, Elite 240 req/min) et `limit_for_tier`. Les routes `/api/tools/osint/*` résolvent l'offre effective (`_resolve_tier`, 'free' pour anonyme ou en cas d'échec) et passent le quota au limiteur. Tests : mapping et refus 429 au-delà de la limite free, marge élite.
- **Présent — Comparatif d'offres** dans le panneau Abonnement : tableau Free/Pro/Elite listant outils, OSINT cloud, quota/min, workspaces E2EE, pipelines, export, agent local, BYOP, proxies résidentiels, multi-cible, et (à venir) monitoring programmé et API. Rend la valeur d'Elite lisible.
- Résultats : backend 25 tests, frontend 34 tests, lint/tsc/build OK.

### Suite prévue (demande « je veux le tout »)

Monitoring programmé (watchlist + re-checks périodiques + alertes via Celery Beat) et API publique + clés (Elite). Ces deux briques nécessitent Supabase pour la persistance : code et tests mockés d'abord, branchement DB à l'hébergement.

## Monitoring programmé (Elite) — 14 octobre 2026

La fonctionnalité phare d'Elite : surveillance périodique de cibles et alertes de changement.

- **Testé — Cœur de détection** (`monitoring.py`) : `digest` (SHA-256 de JSON canonique, stable et insensible à l'ordre), `diff_snapshots` (changements lisibles par clé, ignore les champs volatils comme « Jours restants »), `run_check` (dispatch vers DNS/TLS/WHOIS/HTTP, réutilise les inspecteurs existants et leur garde anti-SSRF, snapshot normalisé). 5 tests.
- **Présent — Migration** `202610140001_monitoring.sql` : tables `watchlist_targets` et `watchlist_changes` avec RLS propriétaire ; insertion réservée aux offres payantes (`has_paid_tier()`), `user_id` auto (`default auth.uid()`) ; le worker écrit via service_role.
- **Présent — Tâche Celery** `cw.monitor_watchlist` + beat horaire : `scan_due_targets` parcourt les cibles dues, exécute les contrôles, compare à l'empreinte précédente et journalise les changements. Sans Supabase configuré, ne fait rien (fail-safe).
- **Présent — Routes Elite** `/api/watchlist` (POST réservé Elite via `EliteUser`, GET/DELETE, GET `/changes`). Validation du type et de la cible.
- **Présent — Panneau front Monitoring** (onglet visible uniquement en Elite) : ajout de cible, liste avec date de dernier contrôle, journal des changements récents.
- Résultats : backend 30 tests (5 monitoring), frontend 34 tests, lint/tsc/build OK.
- À faire pour le live : appliquer la migration sur Supabase, démarrer le worker + beat, et (plus tard) l'envoi d'alertes externes (e-mail/webhook) — pour l'instant les changements sont consultables dans l'app.

## Corrections de la revue cloud et monitoring — 14 octobre 2026

Les sept points de la revue sont corrigés dans le code. Cette section remplace les limites HTTP et monitoring décrites dans les sections historiques ci-dessus.

- **Présent et testé — HTTP anti-SSRF** : chaque saut résout et contrôle les adresses avant connexion à une IP validée. Le Host et le SNI restent ceux du domaine d'origine ; la validation du certificat TLS reste activée. Proxies implicites d'environnement et réutilisation des connexions désactivés. Les redirections sont contrôlées une à une, sans transmission de cookies ou d'identifiants. Tests du transport HTTPX/httpcore avec socket simulée, notamment refus d'une erreur de certificat, IPv6, port explicite et redirection privée.
- **Présent et testé — Lecture des seuls en-têtes** : réponse ouverte en streaming puis fermée sans consommation du corps, y compris lors d'une redirection. Six requêtes au maximum et délai total de 30 secondes. Le test fournit un flux qui échoue si le corps est consommé.
- **Présent et testé localement — Droits Elite** : migration additive `20261014190452_harden_monitoring.sql`, générée avec le CLI Supabase. La politique d'insertion exige une commande Elite active et non expirée. Les clients ne peuvent plus renseigner les colonnes de suivi internes. Le worker contrôle l'éligibilité avant l'exécution, et la transaction de sauvegarde la revérifie. Les fonctions du worker sont réservées au rôle `service_role` et utilisent `security invoker`.
- **Présent et testé — Une tâche par cible** : le dispatcher n'effectue plus les contrôles réseau en série dans son budget global de 30 secondes. Il publie des identifiants vers `cw.monitor_target` ; verrou Redis par cible, budget applicatif 80 s et limites Celery 90/100 s. La sélection exclut les comptes non éligibles et ordonne les tentatives par ancienneté. `last_attempt_at` est distinct de `last_checked_at` : un échec ne prétend pas être un contrôle réussi.
- **Présent et testé localement — Persistance atomique** : `record_watchlist_check` insère l'alerte et met à jour le snapshot dans la même transaction. Vérification des statuts HTTP, verrou SQL et comparaison du digest attendu. Un échec ne fait plus avancer le snapshot ; une tâche ayant une ancienne version ne produit pas une deuxième alerte. Test SQL d'un échec après insertion de l'alerte : alerte et snapshot sont annulés ensemble.
- **Présent et testé — Échéances TLS** : un état stable de seuil est inclus dans le snapshot (30 jours ou plus, moins de 30, moins de 15, expiré). Les changements de seuil déclenchent une alerte sans bruit quotidien. Le premier contrôle signale aussi un certificat déjà à risque.
- **Présent et testé — CORS** : wildcard avec credentials décrit comme configuration invalide bloquant la lecture navigateur ; plus de qualification « Critique » ni de reflet d'origine présenté comme démontré.

Validation locale :

- Frontend : `npm run lint`, `npx tsc --noEmit`, `npm test` (**36 tests réussis**) et `npm run build` réussis.
- Backend : `python -m unittest discover -s tests -v` : **75 tests découverts, 73 réussis, 2 ignorés** (intégrations Redis/Go opt-in).
- SQL : les quatre migrations et `supabase/tests/monitoring.sql` passent sur PostgreSQL 14.20 temporaire, avec rôles Supabase et `auth.uid()` simulés. Refus Pro/anonyme/Elite expiré, insertion Elite, restrictions de colonnes et de fonctions, sélection des cibles, digest périmé, atomicité et expiration avant commit vérifiés. Serveur temporaire arrêté après test.
- Aucun fichier `.env` modifié, aucun nouvel outil ajouté et aucune base distante modifiée.

**Reste à connecter et valider :** appliquer la nouvelle migration sur Supabase avant le nouveau worker ; vérifier PostgREST/Auth et le traitement Celery/Redis de bout en bout. Les tests réseau utilisent des transports simulés et ne constituent pas une recette des services externes ou d'un proxy réel. La limite de 100 cibles distribuées par heure reste une limite du scheduler actuel ; aucune garantie de contrôle horaire de toutes les cibles au-delà de ce volume.

## Facilité d'utilisation des outils — 16 octobre 2026

Les formulaires générés depuis les manifestes restaient techniques ; ajout d'aides à l'usage sans toucher aux manifestes.

- **Présent — Bouton « Charger un exemple »** : pré-remplit le formulaire avec un cas réaliste. Exemples + aide centralisés dans `lib/tool-meta.ts` (29 outils couverts), lus par le formulaire via l'id ; les autres outils dégradent proprement (bouton absent).
- **Présent — Import de fichier** sur les champs texte : bouton « Importer un fichier » qui lit un .txt/.log/.json/.eml/.har… (≤ 5 Mo) dans le champ. Utile pour logs, en-têtes d'e-mail, code à scanner.
- **Présent — Aide courte** : bouton « Aide » qui déplie une phrase d'explication par outil ; bouton « Effacer » pour réinitialiser.
- **Présent — Favoris** : étoile par outil dans le catalogue, filtre « Favoris », favoris remontés en tête. Mémorisés dans le navigateur (`stores/favorites.ts`, localStorage avec repli en mémoire).
- La recherche du catalogue (nom/domaine) et le filtre par type d'exécution existaient déjà et sont conservés.
- Résultats : frontend 59 tests, lint/tsc/build OK. Aucune modification backend.

## Workflows prêts à lancer — 16 octobre 2026

Différenciation vs un simple catalogue : des pipelines pré-câblés chargeables en un clic (réutilisent le moteur de pipeline Pro existant).

- **Présent — 3 workflows** (`lib/workflows.ts`), avec exemples d'entrée valides (repris des tests du catalogue, vérifiés en exécution réelle) :
  1. **Audit de ports Nmap → rapport** : nmap-report compare un scan à un scan de référence (port 443 nouvellement ouvert détecté), puis report-builder génère la section de rapport (exportable PDF). La comparaison est native à nmap-report (entrée `baseline`), sans outil runner.
  2. **DMARC → synthèse MailSec** : dmarc-report analyse un rapport agrégé (142 messages, 14 en échec d'alignement) → report-builder en tire une synthèse partageable.
  3. **SBOM → inventaire → priorisation CVE** : sbom-inventory (CycloneDX) + cve-triage (CVE fournies, triées par CVSS) → report-builder consolide.
- **Présent — Sélecteur « Charger un workflow prêt à lancer »** dans le PipelinePanel : injecte les étapes pré-câblées ; l'utilisateur vérifie/remplace les entrées puis exécute.
- Câblage : chaque étape finale reçoit la sortie `summary` de l'étape précédente dans son champ `description` (sortie texte → entrée textarea, conforme au moteur). Aucun workflow n'exige le runner local.
- **Testé** : un test vérifie que chaque workflow s'ordonne (sans cycle), câble des outils existants avec des types compatibles, et a ses entrées requises pré-remplies. Les 4 entrées d'exemple ont été exécutées sur les vrais runners sans erreur. Frontend 60 tests, lint/tsc/build OK.

## Routage Tor (DNS Lookup)

Premier mode de sortie **Tor** pour DNS Lookup (modes `direct`/`proxy`/`tor`, décidés serveur, réservé Elite+admins, zéro repli). Détails, isolation et vérifications : voir [docs/TOR.md](docs/TOR.md). Ne garantit pas l'anonymat global.
