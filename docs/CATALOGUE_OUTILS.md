# Catalogue des outils — 15 octobre 2026

**53 outils et une démonstration technique**, dont 24 nouveaux outils dans cette salve. Répartition : 45 JavaScript navigateur, 4 cloud existants, 4 réseau via le runner et `local-demo`. Aucun nouvel outil cloud ajouté. Les comptes gratuits disposent de 38 outils navigateur et 4 cloud ; Pro/Elite ajoutent 7 analyses navigateur et les 4 outils réseau. Le catalogue et la sidebar filtrent les droits de l’offre courante.

« Présent » signifie implémenté ; les limites de validation se trouvent dans [ETAT_PROJET.md](ETAT_PROJET.md). Les outils cloud et l’appairage runner nécessitent les services correspondants ; le nombre d’outils n’est pas une garantie de disponibilité sans connexion.

| Domaine | Outils hors démonstration |
| --- | ---: |
| OSINT & Recon | 5 |
| Web AppSec | 5 |
| Réseau & Infra | 5 |
| Crypto & Encoders | 8 |
| Blue Team & Forensics | 5 |
| Cloud & DevSecOps | 5 |
| Threat Intel & GRC | 5 |
| MailSec | 5 |
| Pentest (Local) | 5 |
| Red Team (Local) | 5 |

## Inventaire

Les fiches « Nouveau » sont celles ajoutées le 15 octobre. Les entrées XML sont décompressées et collées ; les archives ZIP et fichiers binaires ne sont pas acceptés. Pour les vingt nouveaux analyseurs navigateur, limite générale des imports : un million de caractères, avec des plafonds plus bas selon l’outil. Le tableau affiche les 500 premières lignes ; la sortie JSON conserve les données traitées complètes.

### OSINT & Recon

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Inventaire de certificats CT](../frontend/src/plugins/manifests/ct-inventory.json) | Navigateur | Gratuit | Nouveau | Extrait et dédoublonne les noms d’un export JSON crt.sh dans un domaine donné. Aucun appel réseau. |
| [DNS Lookup](../frontend/src/plugins/manifests/dns-lookup.json) | Cloud | Gratuit | Existant | Consultez les enregistrements A, AAAA, MX et TXT d’un domaine via l’API cloud. |
| [Analyseur robots.txt](../frontend/src/plugins/manifests/robots-analyzer.json) | Navigateur | Gratuit | Nouveau | Analyse les groupes, règles et sitemaps d’un robots.txt fourni, sans visiter les chemins. |
| [URL Inspector](../frontend/src/plugins/manifests/url-analyzer.json) | Navigateur | Gratuit | Existant | Décompose une URL reçue et repère les pièges : homographe IDN (punycode), identifiants avant @, sous-domaines trompeurs, TLD à risque. Aucune requête réseau. |
| [WHOIS / RDAP Lookup](../frontend/src/plugins/manifests/whois-lookup.json) | Cloud | Gratuit | Existant | Interroge le RDAP officiel d'un domaine : registrar, dates de création/expiration, statuts et serveurs de noms. Exécution cloud passive. |

### Web AppSec

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [CORS & Cookie Analyzer](../frontend/src/plugins/manifests/cors-cookie-analyzer.json) | Navigateur | Gratuit | Existant | Analyse les en-têtes CORS (Access-Control-*) et les attributs des cookies (Secure, HttpOnly, SameSite). |
| [Analyseur HAR](../frontend/src/plugins/manifests/har-analyzer.json) | Navigateur | Gratuit | Nouveau | Classe les requêtes d’un export HAR par durée et compte les erreurs, sans restituer les secrets des en-têtes ou corps. |
| [HTTP Security Headers (live)](../frontend/src/plugins/manifests/http-headers-live.json) | Cloud | Gratuit | Existant | Récupère les en-têtes de réponse d'une URL côté serveur (anti-SSRF, redirections revalidées) et les note avec le même analyseur que l'outil Security Headers. |
| [Security Headers Analyzer](../frontend/src/plugins/manifests/security-headers.json) | Navigateur | Gratuit | Existant | Collez les en-têtes de réponse HTTP (ex. sortie de curl -sI) : l'outil note CSP, HSTS, anti-clickjacking, cookies et fuites de version. |
| [URL & HTML Encoder / Decoder](../frontend/src/plugins/manifests/url-html-encoder.json) | Navigateur | Gratuit | Existant | Encodez ou décodez en pourcent-URL, application/x-www-form-urlencoded et entités HTML. Détecte le double encodage. |

### Réseau & Infra

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Calculateur IPv6](../frontend/src/plugins/manifests/ipv6-calculator.json) | Navigateur | Gratuit | Nouveau | Calcule le réseau, la dernière adresse, la taille et le nom inverse d’une adresse IPv6/CIDR. |
| [Ensembles de ports](../frontend/src/plugins/manifests/port-set.json) | Navigateur | Gratuit | Nouveau | Normalise les listes de ports et compare deux périmètres, sans scan. |
| [Subnet / CIDR Calculator](../frontend/src/plugins/manifests/subnet-calculator.json) | Navigateur | Gratuit | Existant | Calculez réseau, broadcast, masque, wildcard et plage d'hôtes utilisables à partir d'un préfixe CIDR IPv4. |
| [Connectivité TCP](../frontend/src/plugins/manifests/tcp-connect.json) | Runner | Pro | Nouveau | Teste la connexion à 32 ports maximum d’une cible du périmètre local. Mode direct explicite requis. |
| [SSL / TLS Certificate Checker](../frontend/src/plugins/manifests/tls-certificate.json) | Cloud | Gratuit | Existant | Récupère et analyse le certificat TLS d'un hôte : émetteur, validité, jours restants, SAN et algorithme de signature. Connexion passive validée anti-SSRF. |

### Crypto & Encoders

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Classical Cipher](../frontend/src/plugins/manifests/classical-cipher.json) | Navigateur | Gratuit | Existant | Chiffre/déchiffre avec ROT13, César, Atbash, XOR et Vigenère ; force brute César incluse. |
| [Hash Generator](../frontend/src/plugins/manifests/hash-generator.json) | Navigateur | Gratuit | Existant | Calculez l'empreinte SHA-1/256/384/512 d'un texte, directement dans le navigateur (Web Crypto). |
| [Hash Identifier](../frontend/src/plugins/manifests/hash-identifier.json) | Navigateur | Gratuit | Existant | Identifiez les algorithmes possibles d’une empreinte à partir de sa longueur et de son format. |
| [JWT Decoder](../frontend/src/plugins/manifests/jwt-decoder.json) | Navigateur | Gratuit | Existant | Décodez l'en-tête et la charge utile d'un JSON Web Token et repérez les alertes (alg:none, expiration). La signature n'est pas vérifiée. |
| [Magic Decoder](../frontend/src/plugins/manifests/magic-decoder.json) | Navigateur | Gratuit | Existant | Détecte et décode automatiquement les couches successives : Base64, Base64URL, Hex et URL. |
| [Password Entropy Analyzer](../frontend/src/plugins/manifests/password-analyzer.json) | Navigateur | Gratuit | Existant | Estimez l'entropie, l'alphabet et le temps de crack d'un mot de passe. Analyse 100 % locale : rien n'est transmis. |
| [Secure Token Generator](../frontend/src/plugins/manifests/token-generator.json) | Navigateur | Gratuit | Existant | Générez des UUID v4 et des jetons aléatoires (hex, base64url, alphanumérique) via le CSPRNG du navigateur. |
| [Universal Encoder / Decoder](../frontend/src/plugins/manifests/universal-encoder.json) | Navigateur | Gratuit | Existant | Encodez ou décodez du texte en Base64 et Hex, directement dans votre navigateur. |

### Blue Team & Forensics

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Signatures de fichiers](../frontend/src/plugins/manifests/file-signature.json) | Navigateur | Gratuit | Nouveau | Identifie des signatures et mesure l’entropie d’un extrait hexadécimal. N’exécute jamais le fichier. |
| [IOC Extractor](../frontend/src/plugins/manifests/ioc-extractor.json) | Navigateur | Gratuit | Existant | Extrait URL, domaines, IP, e-mails, hashs et CVE depuis des logs ou un rapport, dédoublonne et ressort une liste neutralisée (defang). |
| [Log Parser](../frontend/src/plugins/manifests/log-parser.json) | Navigateur | Gratuit | Existant | Structure des logs Apache/Nginx (combined) ou syslog en tableau, avec top IP et statuts. |
| [Timestamp Converter](../frontend/src/plugins/manifests/timestamp-converter.json) | Navigateur | Gratuit | Existant | Convertissez entre horodatage Unix (s/ms) et formats ISO 8601 / UTC / local. Utile pour la corrélation de logs. |
| [User-Agent Parser](../frontend/src/plugins/manifests/user-agent-parser.json) | Navigateur | Gratuit | Existant | Décompose une chaîne User-Agent : navigateur, système, type d'appareil et détection de bot. |

### Cloud & DevSecOps

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Audit Dockerfile](../frontend/src/plugins/manifests/dockerfile-audit.json) | Navigateur | Gratuit | Nouveau | Repère des configurations à examiner : image non figée, root, secrets déclarés et téléchargements exécutés. |
| [Analyseur de politique IAM](../frontend/src/plugins/manifests/iam-policy.json) | Navigateur | Gratuit | Nouveau | Relève les wildcards, exclusions et délégations dans un document AWS IAM JSON. Analyse statique, sans compte AWS. |
| [JWT Signature Verifier (HMAC)](../frontend/src/plugins/manifests/jwt-verifier.json) | Navigateur | Gratuit | Existant | Vérifie la signature HMAC (HS256/384/512) d'un JWT avec un secret partagé, et signale les secrets faibles ou trop courts. Vérification locale. |
| [Inventaire SBOM](../frontend/src/plugins/manifests/sbom-inventory.json) | Navigateur | Gratuit | Nouveau | Lit CycloneDX JSON ou SPDX 2.x et restitue composants, versions, licences et présence d’empreintes. |
| [Secret Scanner](../frontend/src/plugins/manifests/secret-scanner.json) | Navigateur | Gratuit | Existant | Repère clés d'API, tokens, clés privées et identifiants dans du code ou une configuration collés. Extraits masqués, analyse 100 % locale. |

### Threat Intel & GRC

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Triage de CVE importées](../frontend/src/plugins/manifests/cve-triage.json) | Navigateur | Gratuit | Nouveau | Dédoublonne et classe un export NVD ou une liste de CVE par score CVSS 3.x fourni. Aucun enrichissement en ligne. |
| [CVSS v3.1 Calculator](../frontend/src/plugins/manifests/cvss-calculator.json) | Navigateur | Gratuit | Existant | Calcule le score de base CVSS 3.1 et la sévérité à partir d'un vecteur. |
| [IOC Defanger / Refanger](../frontend/src/plugins/manifests/ioc-defanger.json) | Navigateur | Gratuit | Existant | Neutralisez (defang) ou réarmez (refang) des indicateurs de compromission : URL, domaines, IP et e-mails. |
| [Registre des risques](../frontend/src/plugins/manifests/risk-register.json) | Navigateur | Gratuit | Nouveau | Priorise les risques fournis par probabilité × impact (1 à 5) et affiche responsables et traitements. |
| [Lecteur STIX 2](../frontend/src/plugins/manifests/stix-reader.json) | Navigateur | Gratuit | Nouveau | Inspecte les objets et relations d’un bundle STIX importé, sans interpréter ni exécuter les patterns. |

### MailSec

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Inspecteur DKIM TXT](../frontend/src/plugins/manifests/dkim-record.json) | Navigateur | Gratuit | Nouveau | Inspecte les tags, le type de clé, la révocation et la taille décodée d’un TXT DKIM fourni. Sans validation de signature. |
| [Rapport agrégé DMARC](../frontend/src/plugins/manifests/dmarc-report.json) | Navigateur | Gratuit | Nouveau | Lit un rapport XML DMARC décompressé et calcule les volumes et échecs d’alignement. |
| [Email Header Analyzer](../frontend/src/plugins/manifests/email-header-analyzer.json) | Navigateur | Gratuit | Existant | Retrace les sauts Received, lit les résultats SPF/DKIM/DMARC et repère les signaux d'usurpation (Reply-To divergent, nom affiché trompeur). |
| [Validateur MTA-STS](../frontend/src/plugins/manifests/mta-sts-policy.json) | Navigateur | Gratuit | Nouveau | Vérifie la syntaxe du fichier de politique MTA-STS fourni. Aucun contact avec les MX. |
| [SPF / DMARC Parser](../frontend/src/plugins/manifests/spf-dmarc-parser.json) | Navigateur | Gratuit | Existant | Décortique un enregistrement SPF ou DMARC collé : mécanismes, compte des requêtes DNS (limite de 10), politique et faiblesses. |

### Pentest (Local)

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Comparateur HTTP entre rôles](../frontend/src/plugins/manifests/http-compare.json) | Runner | Pro | Nouveau | Compare deux GET sur la même URL sans redirection. Restitue statut, taille et empreinte, jamais les corps. Autorisations transmises via le relais API en mémoire ; runner direct et périmètre requis. |
| [Démonstration locale](../frontend/src/plugins/manifests/local-demo.json) | Runner | Pro | Existant | Outil sans accès réseau, avec annulation et limites. |
| [Lecteur et comparateur Nmap](../frontend/src/plugins/manifests/nmap-report.json) | Navigateur | Pro | Nouveau | Importe des rapports XML Nmap et compare états et services. Fonctionne dans le navigateur, sans runner. |
| [Inventaire Nmap TCP](../frontend/src/plugins/manifests/nmap-scan.json) | Runner | Pro | Nouveau | Scan TCP connect d’une seule cible, 32 ports maximum, sans scripts NSE. Nécessite Nmap installé et runner activé en mode direct avec périmètre. |
| [Import de rapports ZAP / Burp](../frontend/src/plugins/manifests/scan-report.json) | Navigateur | Pro | Nouveau | Normalise et dédoublonne les observations de rapports ZAP JSON ou Burp XML, dans le navigateur. |
| [Audit TLS local](../frontend/src/plugins/manifests/tls-audit.json) | Runner | Pro | Nouveau | Teste TLS 1.2 et TLS 1.3 avec vérification du certificat et du nom. Deux connexions au maximum ; runner et périmètre en mode direct requis. |

### Red Team (Local)

| Outil | Exécution | Offre | Ajout | Entrées et limites |
| --- | --- | --- | --- | --- |
| [Planificateur ATT&CK](../frontend/src/plugins/manifests/attack-plan.json) | Navigateur | Pro | Nouveau | Structure un exercice avec objectifs, périmètre, détections attendues et nettoyage. Préparation uniquement. |
| [Lecteur BloodHound](../frontend/src/plugins/manifests/bloodhound-reader.json) | Navigateur | Pro | Nouveau | Examine les ACL sensibles et propriétés HighValue/délégation d’un export JSON BloodHound décompressé. Aucune collecte AD. |
| [Couverture de détection](../frontend/src/plugins/manifests/detection-coverage.json) | Navigateur | Pro | Nouveau | Compare techniques planifiées et observations documentées ; distingue non testé, détecté, mixte et non détecté. |
| [Payload Analyzer](../frontend/src/plugins/manifests/payload-analyzer.json) | Navigateur | Pro | Existant | Décode et analyse un payload capturé (PowerShell -enc, obfuscation) et met en évidence les indicateurs suspects. Analyse statique, jamais exécuté. |
| [Pentest Report Builder](../frontend/src/plugins/manifests/report-builder.json) | Navigateur | Pro | Existant | Transforme un finding en section de rapport Markdown propre, avec sévérité CVSS. Pour vos rapports d'engagement. |

## Limites à connaître

- Les analyseurs IAM/Dockerfile, les signatures de fichiers et les imports de rapports sont des aides au triage. Ils ne certifient ni sécurité ni conformité et ne remplacent pas les outils sources.
- CT, CVE, STIX et BloodHound traitent les données fournies ; aucune collecte ni actualisation externe. Le lecteur BloodHound ne fusionne pas les graphes et ne calcule pas de chemins d’attaque.
- Le plan ATT&CK valide la syntaxe des identifiants ; il ne vérifie pas leur existence dans une version MITRE et n’exécute aucune technique. La couverture de détection reflète les observations et preuves renseignées.
- DKIM inspecte le TXT sans valider une signature de message ou la structure RSA. MTA-STS vérifie la syntaxe du texte, sans vérifier sa publication. Le rapport DMARC utilise les résultats d’alignement déclarés et pondère par le nombre de messages.
- HAR retire query strings, credentials d’URL, headers et corps de ses sorties ; les chemins peuvent toujours contenir des identifiants. Les autres exports peuvent contenir des informations sensibles fournies en entrée.
- Nmap, TCP, TLS et HTTP restent exclusivement sur le poste du runner, en mode direct avec périmètre explicite. BYOP des sondes actives reste à réaliser. Voir les [commandes et dépendances](../README.MD#activer-les-quatre-outils-réseau-locaux).
