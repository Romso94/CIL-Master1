

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