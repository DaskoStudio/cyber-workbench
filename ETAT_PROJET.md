# État du projet — 13 octobre 2026

État après développement des principales phases du guide, en reportant les connexions externes comme demandé. L’inventaire initial est conservé dans ETAT_PROJET.initial.md. Aucune mise en production, connexion à des comptes marchands ou migration sur Supabase distant n’a été effectuée. Les fichiers .env existants n’ont pas été consultés ni remplacés.

## Statuts

- **Présent** : code disponible, sans validation suffisante du parcours concerné.
- **Testé** : vérification locale exécutée, avec portée et simulations précisées.
- **Incomplet** : code partiel ou garanties demandées non démontrées.
- **Absent** : fonctionnalité non implémentée ; report explicite.

## Exigences et preuves

### Interface et moteur

- **Testé — Next.js, TypeScript, Tailwind, shadcn/ui** : App Router, composants locaux, sidebar rétractable, thème sombre et dix domaines. Build Webpack et lint passent ; contrôles navigateur pour changement de catégorie.
- **Testé — État Zustand** : sélection, historique borné à 100 exécutions, statuts et résultats. Changement d’identité efface l’historique et déconnecte le runner ; aucun stockage local automatique du contenu.
- **Testé — Manifestes JSON/formulaires dynamiques** : quatre manifestes, schéma Zod versionné, validation des destinations et couche d’exécution, tests de rejet d’un endpoint arbitraire.
- **Testé — Base64/Hex** : JS navigateur, roundtrip UTF-8 et erreurs d’encodage. Limite d’entrée pour borner les ressources.
- **Testé — Hash Identifier** : candidats de format, ambiguïtés de longueur explicites et limite d’entrée. Aucun résultat ne prouve l’algorithme ou l’authenticité d’un hash.
- **Absent — Module WASM réel** : l’exécution navigateur est JS ; le type wasm reste réservé à une évolution éventuelle.
- **Testé — Connexion cloud frontend** : adaptateur centralisé, Bearer de session quand disponible, annulation et erreurs. DNS testé dans Chromium avec réponses API simulées ; pas de requête DNS réelle depuis cette recette.
- **Testé — Connexion runner dans l’UI** : appairage, ticket privé, état, streaming et annulation codés. Parcours navigateur avec WebSocket simulé ; parcours Go/API réel testé séparément.

### Authentification et base

- **Incomplet — Auth Supabase réelle** : inscription, connexion, restauration de session, déconnexion, suppression de compte et API utilisateur codées. Les exécutions runner revérifient l’identité et les droits ; token HTTP gardé uniquement en mémoire, jamais dans Redis ou les messages de l’agent. Tests avec identité simulée ; vrai JWT, emails, révocation externe et suppression distante non validés.
- **Testé — Middleware HTTP** : token absent/invalidité refusés et panne du service distinguée (401/503). get_user exécuté hors de la boucle async. Démarrage/lifespan, santé et refus du token absent également vérifiés sur la vraie factory avec configuration sans service externe. CORS local vérifié.
- **Testé — Schéma profils/workspaces/plugins_custom** : migrations appliquées sur PostgreSQL temporaire ; auth.users et auth.uid simulés. La table profils remplace users pour éviter la duplication d’Auth.
- **Testé — RLS** : propriétaire, refus CRUD inter-utilisateurs, auto-promotion interdite, expiration des droits et conflits de version sur PostgreSQL local. Application et validation sur Supabase de test encore nécessaires.
- **Testé — Droits serveur** : tirés de billing_orders actives non expirées, jamais de user_metadata. Tests priorité Pro/Elite et expiration. La durée de session runner est bornée par le droit payé. Écritures Pro ; données déjà possédées lisibles/supprimables après downgrade.
- **Testé — API workspace** : payload ciphertext/context, refus de contexte ou identité forgés, écriture gratuite refusée et conflit de version. REST utilisateur avec anon+Bearer, pas de service_role pour ce contenu.
- **Présent — Suppression de compte** : confirmation explicite, révocation des sessions, appel admin pour son propre compte et cascade SQL. Essai Supabase distant restant.

### Runner et OPSEC

- **Testé — Appairage/tickets WebSocket** : owner, rôle, expiration, rejeu, Origin, révocation et exigence WSS hors développement ; secrets absents des URL. Tickets 30 s navigateur / 120 s agent, sessions d’une heure.
- **Testé — Exécution locale bornée** : uniquement local-demo, pas de shell/os.exec arbitraire. Deux tâches simultanées, timeout dix secondes, sortie bornée, 1000 IDs/session, refus des doublons. Le relais valide les messages et impose 64 Ko/message et 1 Mo/sortie.
- **Testé — Go/API en réseau local** : vrai binaire et vrai WebSocket, mais identité simulée ; démonstration, streaming, annulation, refus du rejeu et révocation.
- **Testé — Helpers proxy, stdin et concurrence Go** : go test -race et go vet passent. Aucun fournisseur proxy réel ni mesure de fuite réseau effectués.
- **Incomplet — BYOP réseau** : dialer WebSocket SOCKS5/HTTP et modes direct/optional/required ; aucune protection universelle de futurs exécutables. La démonstration n’émet aucun trafic réseau.
- **Incomplet — TLS/appairage multiplateforme** : cinq binaires cross-compilés avec checksums ; installations Linux/Windows, ACL Windows et reverse proxy WSS non testés. Pas de mise à jour automatique.
- **Présent — Relais mono-processus** : sessions en mémoire, perte au redémarrage et nouvel appairage obligatoire. Aucune architecture API multi-instance revendiquée.

### Cloud et tâches

- **Présent — DNS A/AAAA/MX/TXT** : async dnspython ou DoH, validation du domaine, erreurs et délai. Tests proxy avec simulations ; résolution réelle à confirmer avec un réseau configuré.
- **Testé — Refus du fallback proxy** : panne ou absence de proxy demandé → 503, aucun appel direct dans les tests. Droits Elite contrôlés côté serveur.
- **Présent — Quotas** : limiteur borné par utilisateur/IP et création de sessions/tâches ; scope mono-processus, pas de protection distribuée.
- **Testé — Redis/Celery** : publication et consommation via Redis temporaire et worker Celery local, DNS simulé. Propriété, statuts, idempotence de publication, annulation coopérative, retries bornés et refus de republier un résultat terminal codés.
- **Testé — TTL de tâches de 72 h** : Redis conserve l’expiration lors des mises à jour, expiration et refus de ressusciter une tâche annulée testés. Broker limité aux IDs, sans token/entrée DNS.
- **Incomplet — Rétention globale des logs** : compose sans conservation de logs API/worker et Redis non persisté. Rétention des systèmes externes, sauvegardes et observabilité réelle à configurer ; aucune purge de prestataire promise.
- **Présent — Cloud passif** : seul DNS dans les workers de sécurité. Aucun scan actif cloud. Les appels de facturation concernent uniquement les fournisseurs configurés.
- **Absent — WHOIS/scraping et scans locaux actifs** : catalogue initial limité, aucune commande réseau active livrée.
- **Absent — Multi-targeting/scans de masse** : reportés hors du MVP ; tout futur scan actif doit rester local.
- **Incomplet — Fournisseur résidentiel rotatif/illimité** : URL proxy préparée, pas de rotation/fournisseur/quota commercial connectés.

### Workspaces et fonctions Pro

- **Testé — E2EE navigateur** : AES-256-GCM, clé de données aléatoire, enveloppes phrase/récupération, PBKDF2 et contexte compte/workspace authentifié. Roundtrip, mauvaise phrase, ciphertext altéré et échange de contexte refusés dans les tests.
- **Présent — Persistance chiffrée** : CRUD/version RLS/API et UI ; parcours Supabase distant et second appareil non validés. Phrase et clé de récupération jamais envoyées ; nom et métadonnées restent visibles.
- **Présent — Récupération** : clé privée exportable par sauvegarde, modèle décrit dans docs/E2EE.md. Sans clé ni phrase, pas de récupération serveur. Revue cryptographique indépendante encore nécessaire.
- **Testé — Pipelines visuels** : éditeur d’étapes, liaisons simples, cycles/IDs dupliqués refusés, confirmation locale, annulation et arrêt sur erreur. Parcours Chromium avec droits Pro simulés.
- **Testé — Exports PDF/Markdown** : génération navigateur, vérification utilisateur et sélection des résultats, masquage de champs courants sensibles et contenu Markdown isolé dans des blocs de code. Téléchargement PDF réel vérifié dans Chromium ; mise en page multi-pages non inspectée ; un secret non reconnaissable peut subsister, revue utilisateur requise.
- **Présent — Configurations personnalisées Pro** : uniquement adaptateurs navigateur approuvés ; pas de scripts, eval ou code serveur téléchargé. Validation backend interdit les tool_id/scripts non autorisés.
- **Absent — Scripts/plugins libres isolés** : choix de sécurité explicite ; pas de sandbox de scripts revendiquée.

### Facturation et livraison

- **Testé — Signatures et droits de facturation** : HMAC Lemon/BTCPay/NowPayments, contrôle d’expiration, remboursement Lemon et refus de sous-paiement NowPayments avec fixtures. RPC SQL atomique, rejouée sans double effet ; application ordonnée par observation serveur.
- **Présent — Checkout Lemon, BTCPay et NowPayments** : prix/produits/configuration externes ; BILLING_ENABLED=false. Pas d’achat réel ni de compte marchand connecté.
- **Présent — Rapprochement périodique** : Celery Beat toutes les 15 min, lot borné à 100 commandes connues. Tests du mode désactivé et des appels simulés. Le premier webhook doit associer l’objet Lemon/NowPayments ; s’il manque, réémission fournisseur nécessaire.
- **Incomplet — SaaS commercial réel** : renouvellements, refunds/expirations externes, coûts, prix et comptes marchands non validés. Crypto : accès 30 jours, pas de renouvellement automatique ni garantie d’anonymat.
- **Présent — CI et environnement Docker** : workflow lint/type/build/tests/browser, lockfiles et compose API/Redis/worker/beat. CI GitHub et construction Docker non exécutées.
- **Testé — Packaging Go** : cinq cibles compilées avec SHA256SUMS. Distribution signée et installation sur chaque OS encore nécessaires.
- **Incomplet — Staging/production** : procédures de connexion, sauvegarde et rollback documentées ; aucun déploiement ni restauration de staging effectués.

## Résultats locaux observés

- Frontend : lint et TypeScript passent ; sept tests Node passent ; onze tests Chromium passent (JS réel, API/WS/droits simulés). Build Webpack réussi après suppression du loader Turbopack problématique et des polices distantes.
- Backend : suite standard 30 tests, 28 réussis et deux opt-in ignorés. Ces deux tests ont été exécutés avec CW_LIVE_TESTS=1 : Go/API réel et Redis/Celery réel, avec Auth/DNS simulés. Aucun token Supabase réel.
- PostgreSQL temporaire : migrations, isolation RLS, protection des tiers, expiration, versions et rejeu facturation validés. Auth est une simulation locale.
- Go : tests/race detector et vet réussis ; macOS amd64/arm64, Linux amd64/arm64 et Windows amd64 compilés. Aucun de ces builds n’a été publié.
- Dépendances : pip check passe. Dernier audit npm : zéro alerte runtime ; cinq alertes élevées de développement dans la chaîne ESLint/glob/braces. Pas de downgrade majeur automatique. Audit de vulnérabilités Python et revue indépendante non effectués.

Le contrôle de fichier Unix est conservé ; Windows peut utiliser -pairing-stdin avec un ticket source protégé par ACL. Les installations sur ces OS restent à valider.

Les tests ne prouvent ni la sécurité complète ni la conformité production. La CI est préparée, pas observée sur GitHub. Les fichiers .env réels et les services externes sont restés hors de cette validation.

## Écarts et choix actés

1. JS remplace WASM pour les premiers outils ; pas de fausse étiquette WASM dans leurs manifestes.
2. Backend relaie navigateur/agent et peut lire ses messages ; E2EE protège seulement le stockage de workspace.
3. Profils liés à auth.users et droits via commandes serveur actives remplacent la table users autonome et les tiers déclaratifs.
4. Agent limité à une démonstration approuvée plutôt qu’à des commandes arbitraires.
5. Aucun fallback direct en mode proxy demandé ; pas de promesse de routage universel.
6. Catalogue de quatre outils, pas dix outils parce qu’il existe dix catégories.
7. Configurations approuvées remplacent les scripts personnalisés libres ; extension future à isoler.
8. API mono-instance pour le MVP ; multi-instance et proxys illimités non annoncés.
9. Phrase distincte + récupération exportable, conformément au choix laissé à l’assistant ; les deux prestataires crypto sont préparés comme demandé.
10. Downgrade autorise récupération/suppression de ses données précédentes ; nouvelles écritures payantes refusées.

## Point de reprise

**Arrêt à la Phase 8.3 : recette locale terminée pour le socle livré, connexions et recette externe à effectuer ensuite.** Les phases ne sont pas déclarées intégralement validées en production.

Prochaine étape : docs/CONNEXIONS.md, commencer par Supabase de test et ses migrations, puis compte Pro temporaire, runner, proxy, paiements de test et staging. Aucune clé ne doit être transmise dans le chat. Les fonctionnalités absentes ci-dessus sont des reports explicites, pas du code supposé existant.
arrete toi la pour l'instant 


## Interface et visibilité par offre — 13 octobre 2026

- **Présent** : accueil avec recherche et cartes d’outils, palette sombre ardoise/menthe, navigation dédiée aux outils, workspaces, pipelines, runner, tâches, configurations et compte. Navigation compacte sur mobile, focus clavier et lien d’accès au contenu.
- **Testé** : niveau d’offre lu depuis `/api/auth/me`, sans sélecteur de droits côté utilisateur ni persistance locale du niveau. Valeur gratuite initiale et en cas d’échec ; actualisation au changement d’identité, au retour sur la fenêtre et toutes les 60 secondes. Réponses obsolètes ignorées.
- **Testé** : comptes gratuits sans commandes de sauvegarde/export, pipeline, runner et configuration Pro ; domaines locaux et manifestes payants filtrés. Pro et Elite accèdent aux fonctions Pro. Les présentations commerciales restent dans Mon compte.
- **Présent** : récupération et suppression des anciennes sauvegardes depuis Mon compte pour les utilisateurs revenus à l’offre gratuite, sans nouvelle sauvegarde ni export payant. Ce parcours réel reste à valider avec Supabase.
- **Testé** : disparition des panneaux payants après baisse d’offre ou erreur de vérification. Tests navigateur avec identités et API simulées, pas de validation Supabase réelle. Les contrôles serveur existants restent indispensables ; le filtrage visuel ne remplace pas l’autorisation API/RLS.
- **Testé** : runner appairé utilisable après navigation vers un outil local ; encodeur, hash, DNS simulé, pipeline et export PDF toujours opérationnels dans les tests.
- **Testé** : 11 tests Chromium, 7 tests Node, lint et build de production avec contrôle TypeScript réussis. Captures ordinateur/mobile inspectées ; contrôle de largeur mobile à 390 px.
- **Incomplet** : le catalogue reste limité aux quatre outils déjà livrés. Aucune nouvelle capacité Elite, aucun service externe ni paiement réel activé par cette refonte.

Point de reprise : poursuivre les exigences et outils manquants du PRD avant les connexions, conformément à la demande utilisateur. La Phase 8.3 désigne uniquement la recette du socle précédent, pas l’achèvement de tout le PRD.

### Révision visuelle — console métier

Le catalogue en cartes et les slogans sont remplacés par une liste structurée (outil, domaine, exécution), une recherche combinée à un filtre d’exécution et un journal des cinq dernières opérations de la session. Palette graphite neutre, accent bleu discret, navigation compacte à onglets soulignés. Entrées et résultats disposés côte à côte sur grand écran, empilés sur mobile. L’indicateur de développement Next.js est masqué dans l’aperçu.

Les contrôles d’offre précédents sont conservés. Les 11 parcours Chromium existants ont passé ; après correction d’une compression de la barre d’outils, les parcours encodeur/changement d’outil et mobile ont été rejoués avec succès, ainsi qu’un nouveau test combinant filtre, recherche, réinitialisation et historique (12 scénarios au total). Captures ordinateur/mobile inspectées. Aucun changement backend ou connexion externe dans cette révision.

Validation finale du 14 octobre 2026 : build de production isolé réussi, contrôle TypeScript réussi ; aperçu Next.js relancé sur http://127.0.0.1:3000. Refonte de l’interface terminée ; le catalogue et les exigences produit manquants restent à développer.
