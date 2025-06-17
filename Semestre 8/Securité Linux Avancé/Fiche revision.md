

# 📘 Sécurité Linux Avancé

## 🧭 Objectifs du cours
- Comprendre les attaques typiques sur systèmes Linux (ex: élévation de privilège).
- Écrire/utiliser des scripts d’audit.
- Appliquer des politiques de durcissement système.
- Implémenter SELinux, AppArmor, auditd, rsyslog, etc.
- Adopter une architecture de journalisation sécurisée.

---

## 🧱 Architecture Linux

- **Noyau Linux** : monolithique, modulaire, multitâche.
- **Appels système (`syscall`)** : interface entre espace utilisateur et noyau.
- **Processus** : créés avec `fork()`, remplacés avec `exec()`.
- **Commutation de contexte** : bascule entre mode user ↔ kernel.

---

## 🛡️ Durcissement (Hardening)

### Principes
- **Minimisation** : désactiver les composants inutiles.
- **Moindre privilège** : accès minimum requis.
- **Défense en profondeur** : couches de sécurité successives.
- **Conformité** : ANSSI, NIST, PCI-DSS.

### Niveaux ANSSI
- **Minimal** → correctifs, PAM robuste, mots de passe forts.
- **Intermédiaire** → auditd, suppression SUID inutiles.
- **Renforcé** → chroot, AppArmor.
- **Élevé** → SELinux, journalisation exhaustive.

---

## ⚔️ Élévation de Privilège (EoP)

### Types
- **Horizontale** : utilisateur A → utilisateur B.
- **Verticale** : utilisateur → root.

### Techniques d’exploitation
- SUID/SGID
- Variables d’environnement (`PATH`, `LD_PRELOAD`)
- Failles kernel (ex: Dirty COW)
- Race conditions
- Permissions faibles (`/tmp`, `cron`, etc.)

### SUID
- `chmod 4755 fichier` → exécution avec les droits du propriétaire.
- **RUID vs EUID** : le contrôle d’accès se base sur l’EUID.

### Surfaces d’attaque
- **Entrées utilisateur** : buffer overflow, format string.
- **Variables d’environnement** : PATH détourné → exécution arbitraire.
- **Race Conditions** : TOCTTOU (`/tmp/xyz` → `/etc/shadow`).
- **Capability leaking** : privilèges non nettoyés.
- **System()** : ⚠️ commandes injectables.

---

## 🧩 Journalisation et Audit

### Outils
- **rsyslog** : envoi des logs (TCP/UDP, TLS).
- **auditd** : journalisation fine, avec `aureport`.
- **logwatch** : rapports quotidiens.

### Meilleures pratiques
- **Horodatage obligatoire**.
- **Export sur serveur distant** sécurisé (réseau admin dédié).
- **Rotation/Archivage** conforme à la législation.
- **Hiérarchisation des collecteurs** pour résilience.

---

## 🔐 SELinux

### Fonctionnement
- **MAC** (Mandatory Access Control) basé sur **TE** (Type Enforcement).
- Chaque processus et fichier a un **contexte**.
- Exemple de règle :  
  `allow httpd_t httpd_sys_content_t:file read;`

### Concepts clés
- **Domaines** : contraintes d’exécution (ex: `httpd_t`).
- **Transitions** : gérées par `execve()` et les règles de politique.
- **Booleans SELinux** : activent/désactivent dynamiquement certains accès.

---

## 🧠 Règles de bonne pratique

- Ne jamais utiliser `system()` dans des programmes SUID.
- Séparer **code** et **données** (`execve()` ≠ `system()`).
- Ne jamais faire confiance aux variables d’environnement dans les SUID.
- Toujours vérifier les entrées utilisateur.

---



---
## 🔍 Révisions détaillées – Sécurité Linux Avancé

### 🔒 Contrôle d’accès

- **DAC (Discretionary Access Control)** : modèle standard, basé sur le propriétaire.
    
- **MAC (Mandatory Access Control)** : politique définie par le système, comme SELinux.
    
- SELinux fonctionne avec des **types** associés à chaque sujet (processus) et objet (fichier, socket...).
    
- Par défaut, SELinux interdit tout — il faut explicitement définir ce qui est autorisé.
    

---

### 🧪 Exploits et élévation de privilège

- **Set-UID** : exécution d’un binaire avec les droits du propriétaire, très dangereux s’il est mal codé.
- `system("ls")` utilise `/bin/sh` → qui lit **les variables d’environnement** comme `PATH`.
    
- Si un attaquant contrôle `PATH`, il peut rediriger `ls` vers un **script malveillant**, exécuté avec les **droits root** (via Set-UID).
    
- 👉 C’est une **injection de commande** indirecte = **élévation de privilège** assurée.
    

🧠 **Conclusion** :  
Dans un contexte SUID, toujours utiliser `execve()` avec chemins **absolus**, et **jamais** de `system()`.
    
- Exemples classiques d’exploits :
    
    - **Race condition** (`TOCTTOU`) : entre la vérification et l’usage d’une ressource.
        
    - **Injection système via `system()`**.
        
    - **Manipulation de variables d’environnement** (`PATH`, `LD_PRELOAD`, `DYLD_*`).
        
    - **Buffer overflow / format string**.
        

---

### 🛠️ Audit et journalisation

- `rsyslog` : système de journalisation principal sous Linux (fichiers de logs, envoi réseau, chiffré).
    
- `auditd` : journalisation fine des actions système (authentifications, accès fichiers, etc.).
### 🔎 Par défaut, `auditd` trace :

- 🔐 **Évènements d’authentification** : succès et échecs (`pam`, `sudo`, `login`, etc.)
    
- 👤 **Changements de comptes utilisateurs** (ajout/suppression, changement UID/GID)
    
- 📦 **Blocages SELinux**
    
- ⚙️ **Modifications de fichiers système sensibles**
    
- 🧩 **Chargements/déchargements de modules du noyau**
    
- 🔄 **Changements de droits (chmod, chown, setfacl...)**
    
- 📥 **Accès ou tentatives d'accès aux fichiers surveillés**

    
- `aureport` : permet de générer des rapports à partir des logs `auditd`.
    
- Il est recommandé de **centraliser les logs** sur un serveur distant pour éviter la suppression par un attaquant.
    

---

### 🧱 SELinux – Concepts clés

- **Security context** : `user:role:type`
    
- **Domain transitions** : exécution contrôlée d’un processus dans un domaine différent.
    
- Règle SELinux typique :

### ✅ Élévation verticale :

- 👉 Lorsqu’un **utilisateur non privilégié** (ex. `user`) accède à des privilèges **supérieurs**, comme **root**.
    
- Exemples : exploitation de `SUID root`, failles `sudo`, `kernel exploit`, etc.
### ✅ Élévation horizontale :

- 👉 Lorsqu’un utilisateur accède aux **droits d’un autre utilisateur de même niveau**.
    
- Exemple : `user1` accède aux fichiers ou exécute des commandes comme `user2`.
    
- Cela **peut** utiliser une race condition (mais pas uniquement).
    
- Autres techniques : mauvaises permissions sur `~/.ssh`, fuites de tokens, cron jobs mal protégés...

### ✅ `LD_PRELOAD` – définition :

- C’est une **variable d’environnement** utilisée par le **linker dynamique**.
    
- Elle permet de **forcer le chargement** d’une (ou plusieurs) **bibliothèque(s) partagée(s)** avant toute autre.
    
- But : **remplacer ou intercepter** des fonctions système utilisées par un programme (comme `sleep()`, `open()`, etc.).
    

---

### 🧨 Pourquoi c’est dangereux :

- Dans un **programme SUID**, si `LD_PRELOAD` est respectée, un **attaquant** pourrait injecter une bibliothèque **personnalisée** contenant du code malveillant exécuté… avec les **droits root** 😨
    
- Heureusement, pour les programmes SUID :
    
    - Le **linker ignore** `LD_PRELOAD` **si EUID ≠ RUID** (protection de base).
        

Mais si un programme contourne cela (ou un loader custom est utilisé), **danger absolu** ⚠️

### ✅ Définition claire :

- Une **Race Condition** survient quand **plusieurs processus accèdent/modifient une ressource en même temps**, et que **le résultat dépend de l’ordre** d’exécution.
    
- L’attaquant tente d’**intervenir entre deux étapes critiques** : souvent appelé **TOCTTOU** (Time Of Check To Time Of Use).
    

---

### ✅ Exemple classique :

> Un programme SUID root écrit dans `/tmp/monfichier.tmp` sans vérifier s’il s’agit d’un lien symbolique.
> 
> L’attaquant crée un lien symbolique :

### Qu’est-ce qu’une **transition de domaine** dans SELinux ?

Dans SELinux, un **domaine** est une sorte de "contexte de sécurité" associé à un processus. Chaque processus tourne dans un domaine donné, qui détermine ce qu'il a le droit de faire sur le système.

Une **transition de domaine** correspond au changement de ce contexte de sécurité quand un processus lance un autre programme.

#### En gros :

- Quand un processus A (dans un domaine X) exécute un programme B, SELinux peut décider de changer le domaine du nouveau processus (B) pour un autre domaine Y.
    
- Ce changement, c’est la **transition de domaine**.
    
- Elle sert à restreindre les droits du nouveau processus selon la politique SELinux, pour renforcer la sécurité.
    

### Exemple simple :

- Un processus qui tourne dans le domaine **user_t** lance un programme qui doit s’exécuter dans le domaine **httpd_t** (par exemple un serveur web).
    
- SELinux va alors faire une transition de domaine de **user_t** vers **httpd_t** pour ce nouveau processus.
    
- Cela limite ce que le programme lancé peut faire, selon les règles pour **httpd_t**.

### 1. **Enforcing (Application stricte)**

- SELinux est activé et applique toutes les règles de sécurité.
    
- Toute action qui n’est pas autorisée par la politique SELinux est bloquée.
    
- C’est le mode recommandé en production pour protéger le système.
    

### 2. **Permissive (Permissif)**

- SELinux est activé, mais **ne bloque aucune action**.
    
- Il **enregistre seulement les violations** (logs) dans les journaux, ce qui permet d’identifier ce qui serait bloqué si SELinux était en enforcing.
    
- Utile pour tester et déboguer les règles SELinux sans risquer de bloquer des actions légitimes.
    

### 3. **Disabled (Désactivé)**

- SELinux est complètement désactivé.
    
- Aucune politique SELinux n’est appliquée, il n’y a aucune restriction liée à SELinux.
    
- Le système fonctionne comme sans SELinux.

| Mode       | SELinux applique les règles ? | Bloque les actions interdites ? | Enregistre les violations ? |
| ---------- | ----------------------------- | ------------------------------- | --------------------------- |
| Enforcing  | Oui                           | Oui                             | Oui                         |
| Permissive | Oui                           | Non                             | Oui                         |
| Disabled   | Non                           | Non                             | Non                         |
### Qu’est-ce qu’un **Type Enforcement (TE)** dans SELinux ?

Le **Type Enforcement** est le mécanisme principal de contrôle d’accès dans SELinux.

- Dans SELinux, chaque objet (fichier, processus, socket, etc.) est associé à un **type** (aussi appelé **label** ou **contexte**).
    
- De même, chaque processus a un **type** (le domaine).
    
- Le **Type Enforcement** définit les règles qui disent quels types de processus peuvent accéder à quels types d’objets, et comment (lecture, écriture, exécution, etc.).
    

### En résumé :

- Le TE est la **politique qui lie les types** des processus aux types des objets avec des règles d’autorisation.
    
- Par exemple, il va dire que le processus dans le domaine **httpd_t** peut lire des fichiers de type **httpd_sys_content_t** mais pas écrire dessus.
    
- C’est ce qui garantit la séparation stricte et la sécurité sur le système.
    

---

### Pourquoi c’est important ?

- Grâce au TE, SELinux peut empêcher un processus compromis d’accéder à des ressources sensibles.
    
- Le TE est la base des règles SELinux, c’est ce qui fait toute la puissance de ce système.

### PAM — Pluggable Authentication Modules

**PAM** est un système modulaire d’authentification utilisé sur Linux et Unix.

---

### À quoi ça sert ?

- PAM permet de gérer de manière flexible **l’authentification des utilisateurs** (connexion, changement de mot de passe, etc.)
    
- Il fournit une interface unique pour différents services (login, sudo, ssh, su, etc.)
    
- Grâce à PAM, tu peux facilement ajouter, modifier ou enlever des méthodes d’authentification sans toucher au code des applications.
    

---

### Comment ça marche ?

- PAM utilise des **modules** (plugins) qui peuvent être configurés dans des fichiers comme `/etc/pam.d/`
    
- Chaque service utilise un fichier de configuration PAM qui indique quels modules charger et dans quel ordre (ex : vérifier mot de passe, vérifier compte, journaliser, etc.)
    
- Par exemple, tu peux configurer PAM pour utiliser l’authentification par mot de passe, biométrie, carte à puce, ou même LDAP.
    

---

En bref :  
**PAM = un cadre flexible et centralisé pour gérer l’authentification des utilisateurs sur Linux/Unix.**

### MAC = **Mandatory Access Control**

(en français : **Contrôle d’Accès Obligatoire**)

---

### C’est quoi exactement ?

C’est un modèle de sécurité où les règles d’accès sont **imposées par le système** de façon stricte, sans laisser l’utilisateur ou le propriétaire du fichier décider.

- Le système définit qui peut accéder à quoi, et comment.
    
- Les utilisateurs **ne peuvent pas changer ces règles**, même s’ils sont propriétaires des fichiers.
    
- C’est différent du **DAC (Discretionary Access Control)**, où le propriétaire décide des permissions (comme sous Linux avec chmod/chown classique).
    

---

### Exemple de systèmes MAC :

- **SELinux**
    
- **AppArmor**
    
- **TrustedBSD**
    

---

### Pourquoi c’est important ?

- Le MAC renforce la sécurité, car il empêche les utilisateurs ou programmes compromis d’accéder à des ressources sensibles même s’ils ont des droits standards.
    
- Il est souvent utilisé dans des environnements très sensibles (serveurs, systèmes militaires, etc.).

Dans SELinux, chaque **objet** (fichier, socket, processus...) a un **contexte de sécurité** appelé **Security Context**.

Il est structuré en **3 éléments** principaux :

```bash
user:role:type
```
#### 🔹 Détail :

- **user** → identifiant SELinux (≠ login Linux), ex: `system_u`, `user_u`
    
- **role** → rôle attribué au processus (souvent `object_r` pour les fichiers)
    
- **type** → élément central du contrôle d’accès **Type Enforcement**, ex: `httpd_t`, `ssh_exec_t`

```shell
allow user_t bin_t : file { read execute };
```

### Réponse complète : Pourquoi horodater les logs ?

1. **Analyse post-incident (forensique)** :
    
    - Permet de **retracer les événements** : qui a fait quoi, quand.
        
    - Utile pour détecter des attaques, connexions non autorisées, effacements de traces, etc.
        
2. **Corrélation des événements** :
    
    - L’horodatage permet de **croiser les logs** entre plusieurs machines ou services.
        
    - S’il y a des **incohérences de dates**, cela peut indiquer un **dérèglement système** ou une **attaque** (ex: modification de l’horloge pour masquer une intrusion).
        
3. (Bonus) **Détection de comportements anormaux** :
    
    - Fréquence excessive, événements répétitifs, pics d’activité… sont visibles grâce aux horodatages.

## 🕒 Qu’est-ce que **NTP** ?

### ✅ **NTP** = _Network Time Protocol_

> C’est un **protocole réseau** conçu pour **synchroniser l’horloge système** des machines avec une ou plusieurs **sources de temps fiables** (serveurs NTP publics ou internes).

---

### 🔎 Pourquoi c’est **crucial** en sécurité ?

1. ✅ **Précision des horodatages**
    
    - Si les logs ne sont pas **synchronisés**, il est **impossible** de faire une corrélation fiable entre machines (ex: serveur web, pare-feu, SIEM...).
        
2. ✅ **Détection des attaques**
    
    - Si une machine a l’heure déréglée, cela peut cacher une **tentative de masquage** (ex: effacement de trace suivi d’un retour dans le passé).
        
    - Des logs sans cohérence temporelle sont **suspicious**.
        
3. ✅ **Respect des obligations légales**
    
    - Certaines normes (ISO, PCI-DSS, RGPD) exigent des **logs horodatés de manière fiable et traçable**.
        

---

### 🧰 Comment ça marche ?

- Un client (ta machine) interroge des **serveurs NTP** publics ou privés.
    
- Il ajuste son horloge locale en fonction des réponses.
    
- Le service s’appelle souvent `ntpd` ou `chronyd`.
    

---

### 📌 Bonnes pratiques :

- Configurer **plusieurs sources NTP fiables**, internes et/ou publiques (évite le SPOF).
    
- Éviter de se fier à une seule horloge externe non authentifiée.
    
- Sur réseaux critiques : utiliser des serveurs NTP **internes**, synchronisés entre eux.
    

---

🧠 En résumé :  
**"Pas de sécurité sans temps fiable"**. Le NTP est un **fondement invisible mais indispensable**.


### 🧪 Cas d’étude : Durcissement OS

📘 **Contexte** :  
Tu es chargé d’auditer un serveur Linux Debian 12 utilisé comme serveur web interne.

- Services actifs : Apache2, SSH, Cron
    
- Utilisateurs avec accès SSH : admin1, devops, testuser
    
- SELinux n’est pas installé
    
- Pas de système de journalisation avancé
    
- Serveur connecté au réseau interne uniquement (pas exposé à Internet)
    

🎯 **Mission** :  
En tant qu’expert sécurité, propose un plan de durcissement clair et structuré en précisant :

- Ce que tu vas configurer ou désactiver
    
- Pourquoi c’est nécessaire
    
- Quels outils tu utiliseras
    

---

### ❓ Questions à traiter :

1. Quels sont les principes généraux que tu appliquerais pour le durcissement ?
    
2. Quels services ou composants méritent une vérification ou désactivation immédiate ?
    
3. Quelles mesures de journalisation et surveillance mettrais-tu en place ?
    
4. Si SELinux n’est pas utilisable, que peux-tu mettre en place à la place ?
    
5. Donne au moins 5 commandes utiles pour mettre en œuvre ou vérifier ce durcissement.

### Rapport d’audit : Plan de durcissement du serveur Debian 12

#### 1. Principes généraux appliqués pour le durcissement

- Réduction de la surface d’attaque : désactivation des services inutiles.
    
- Mise en place d’un contrôle strict des accès (authentification forte, gestion des permissions).
    
- Surveillance et journalisation centralisées pour détecter les anomalies.
    
- Application du principe du moindre privilège (limiter les droits au minimum nécessaire).
    
- Protection des fichiers sensibles et des configurations système.
    
- Renforcement du noyau et des mécanismes de sécurité (MAC, firewall).
    

#### 2. Services ou composants à vérifier/désactiver immédiatement

- Vérifier les services actifs et désactiver tous ceux non indispensables au fonctionnement (ex: services réseaux inutilisés).
    
- Contrôler la présence et l’usage de fichiers avec le bit SUID/SGID et désactiver ceux non justifiés.
    
- Auditer l’accès SSH : désactivation de la connexion root par mot de passe, changement du port par défaut, activation de l’authentification par clé publique uniquement.
    
- Vérification des tâches cron et des permissions des scripts associés.
    

#### 3. Mesures de journalisation et de surveillance à mettre en place

- Installation d’un HIDS comme **AIDE**, **OSSEC** ou **Wazuh** pour surveiller l’intégrité des fichiers.
    
- Configuration de **rsyslog** pour la collecte et le transfert des logs vers un serveur distant sécurisé, afin d’éviter la perte de logs en cas d’attaque locale.
    
- Mise en place d’**auditd** pour une journalisation fine des événements système.
    
- Contrôle des permissions sur les fichiers de logs pour restreindre leur accès aux administrateurs uniquement.
    

#### 4. Alternatives à SELinux

- Si SELinux ne peut pas être installé, utiliser **AppArmor**, qui est souvent plus simple à déployer sur Debian.
    
- Sinon, renforcer la sécurité via des règles de firewall strictes (iptables, nftables), contrôle des accès SSH, et installation d’outils de monitoring/IDS.
    
- Durcissement du noyau via la configuration sysctl (ex: protection contre les accès non autorisés aux interfaces réseau, désactivation de modules inutiles).
    

#### 5. Commandes utiles pour mettre en œuvre ou vérifier le durcissement

- `lynis audit system` — réaliser un audit complet de sécurité.
    
- `systemctl list-unit-files --state=enabled` — lister les services activés.
    
- `find / -perm -4000` — chercher les fichiers avec bit SUID.
    
- `sshd -T` ou `cat /etc/ssh/sshd_config` — vérifier la configuration SSH.
    
- `auditctl -l` — lister les règles actives d’auditd.
    
- Bonus : `iptables -L -v` ou `firewall-cmd --list-all` — vérifier l’état du firewall.
    

---

### Conclusion

En appliquant ce plan, on réduit significativement les risques d’intrusion, de compromission et de perte de données sur ce serveur. La combinaison d’un contrôle rigoureux des accès, d’une surveillance renforcée et d’un durcissement système adapté assure une posture sécuritaire robuste.


### 1. Explique le fonctionnement de PAM et son rôle dans l’authentification sous Linux

**PAM (Pluggable Authentication Modules)** est un système modulaire qui permet aux applications d’utiliser différentes méthodes d’authentification de manière flexible.

- Au lieu que chaque programme gère l’authentification à sa manière, PAM centralise cette gestion.
    
- Chaque service (login, sudo, ssh, etc.) a un fichier de configuration PAM qui spécifie quels modules doivent être utilisés (mot de passe, biométrie, LDAP, etc.).
    
- Cela facilite l’ajout ou la modification des méthodes d’authentification sans changer le programme.

### 2. Quelle différence entre type enforcement et role-based access control dans SELinux ?

- **Type Enforcement (TE)** est le mécanisme principal de SELinux. Il associe un type (label) aux fichiers, processus, etc., et définit quelles actions sont permises entre les types (ex : le processus httpd_t peut lire les fichiers httpd_sys_content_t).
    
- **Role-Based Access Control (RBAC)** est un système qui attribue des rôles aux utilisateurs/processus, chaque rôle ayant un ensemble de permissions et domaines autorisés.  
    **En résumé :** TE contrôle les interactions entre objets et processus, RBAC contrôle quels rôles un utilisateur peut adopter.

### 3. Que se passe-t-il lorsqu’un processus lance un autre processus dans SELinux ? (transition de domaine)

Quand un processus lance un autre processus (par exemple, un shell qui lance un script), SELinux peut changer automatiquement le **domaine (type)** du nouveau processus selon des règles appelées **transition de domaine**.  
Cela permet de s’assurer que le nouveau processus a les permissions adaptées, souvent plus restreintes, pour limiter les risques.

- Pour voir si SELinux est activé et son mode :

```
sestatus
```

### 5. Qu’est-ce qu’une politique SELinux de type targeted par rapport à une politique strict ?

- **Targeted** est la politique par défaut sur beaucoup de distributions. Elle applique des règles SELinux seulement à certains services critiques (ex : Apache, sshd). Le reste du système est en mode permissif.
    
- **Strict** applique des règles SELinux très strictes à **tous** les processus du système, ce qui offre plus de sécurité mais demande une configuration beaucoup plus complexe.

### 6. Comment écrire une règle simple SELinux pour autoriser un processus à lire un fichier ?

Une règle typique ressemble à ça :
```Selinux
allow process_type file_type:file { read open };
```

- **Enforcing** : SELinux applique strictement les règles et bloque les actions non autorisées.
    
- **Permissive** : SELinux ne bloque rien, mais loggue ce qui aurait été bloqué. Utile pour débogage.
    
- **Disabled** : SELinux est désactivé, aucune règle n’est appliquée.




Permissions SUID/SGID 4750
LD_PRELOAD
Moindre Privilege 
Race conditions 
Service Approach 
PATH variable
ISOLEMENT PAS DE SYSTEM() avec SUID
PAM
Journaux d'evenements 
rsyslog auditd
hordatage des logs HIDS
SELINUX : MAC/DAC - Bell-LaPadula Model -> MLS - Type Enforcement -> Type security context user:role:type - type for object / domain for proces - allow rule (Source Type - Target Type - Object Type - Permissions) - Domain transition -> type transition - Role-based access control - 

Process isolation - Cgroup - Namespaces - kernel capabilities - SECCOMP
