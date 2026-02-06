NTL-SysToolbox

Outil CLI d'administration système pour Nord Transit Logistics - Diagnostic, sauvegarde et audit d'obsolescence.

[
[
Description

NTL-SysToolbox est un outil en ligne de commande multi-plateforme qui permet de :

    Diagnostiquer les services critiques (Active Directory, DNS, MySQL)

    Sauvegarder automatiquement la base de données WMS

    Auditer l'obsolescence des systèmes réseau

Prérequis

    Python 3.8 ou supérieur

    Accès réseau aux systèmes à superviser

    Credentials administrateur pour AD et MySQL

Installation
Sur Linux

bash
# 1. Cloner le dépôt
git clone https://github.com/ninochv/MSPR-ES6.1-Nino-Marius-Paul-Arthur.git
cd MSPR-ES6.1-Nino-Marius-Paul-Arthur/NTL-SYSTOOLBOX

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les credentials
cp .env.example .env
nano .env  # Éditer avec vos credentials
chmod 600 .env

Sur Windows

text
REM 1. Cloner le dépôt
git clone https://github.com/ninochv/MSPR-ES6.1-Nino-Marius-Paul-Arthur.git
cd MSPR-ES6.1-Nino-Marius-Paul-Arthur\NTL-SYSTOOLBOX

REM 2. Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate

REM 3. Installer les dépendances
pip install -r requirements.txt

REM 4. Configurer les credentials
copy .env.example .env
notepad .env

Installation via pip (alternative)

bash
# Installation directe depuis le dépôt
pip install -e .

# Avec outils de développement
pip install -e ".[dev]"

Configuration

Éditer le fichier .env avec vos credentials :

text
# Base de données MySQL
NTL_DB_USER=wmsuser
NTL_DB_PASSWORD=VotreMotDePasse
NTL_DB_HOST=192.168.10.21
NTL_DB_NAME=wmsdb

# Active Directory
NTL_AD_USER=administrateur@ntlogistics.local
NTL_AD_PASSWORD=VotreMotDePasseAD

Le fichier config.yaml contient les paramètres généraux (serveurs, seuils, etc.).
Utilisation
Mode interactif

Linux :

bash
python3 ntl-systoolbox.py

Windows :

text
python ntl-systoolbox.py

Un menu interactif s'affiche :

text
╔════════════════════════════════════════════════════╗
║        NTL-SysToolbox - Menu Principal            ║
╚════════════════════════════════════════════════════╝

1. Module Diagnostic
2. Module Sauvegarde WMS
3. Module Audit d'obsolescence
4. Configuration
5. Quitter

Mode ligne de commande
Module Diagnostic

bash
# Diagnostic complet
python ntl-systoolbox.py diagnostic --all

# Vérifier uniquement AD/DNS
python ntl-systoolbox.py diagnostic --check-ad --check-dns

# Vérifier MySQL uniquement
python ntl-systoolbox.py diagnostic --check-mysql

# Vérifier ressources système
python ntl-systoolbox.py diagnostic --check-system

Module Sauvegarde

bash
# Sauvegarde complète de la base
python ntl-systoolbox.py backup --full

# Sauvegarde avec compression
python ntl-systoolbox.py backup --full --compress

# Export de tables spécifiques en CSV
python ntl-systoolbox.py backup --table orders --format csv
python ntl-systoolbox.py backup --table orders,inventory,shipments --format csv

Module Audit

bash
# Scan réseau complet
python ntl-systoolbox.py audit --scan-network

# Scan d'une plage IP spécifique
python ntl-systoolbox.py audit --scan-network --range 192.168.10.0/24

# Analyse CSV et génération rapport
python ntl-systoolbox.py audit --analyze-csv infrastructure.csv

# Rapport d'obsolescence complet
python ntl-systoolbox.py audit --full-report

Format de sortie

Par défaut, l'outil génère deux formats :

    Human : Sortie lisible en console

    JSON : Fichier horodaté pour intégration supervision

bash
# Forcer sortie JSON uniquement
python ntl-systoolbox.py diagnostic --all --format json

# Sortie lisible uniquement
python ntl-systoolbox.py diagnostic --all --format human

Automatisation
Linux (Cron)

Éditer le crontab :

bash
crontab -e

Ajouter :

text
# Diagnostic quotidien à 6h
0 6 * * * cd /opt/ntl-systoolbox && /opt/ntl-systoolbox/venv/bin/python ntl-systoolbox.py diagnostic --all

# Sauvegarde quotidienne à 2h
0 2 * * * cd /opt/ntl-systoolbox && /opt/ntl-systoolbox/venv/bin/python ntl-systoolbox.py backup --full --compress

# Audit hebdomadaire le lundi à 3h
0 3 * * 1 cd /opt/ntl-systoolbox && /opt/ntl-systoolbox/venv/bin/python ntl-systoolbox.py audit --full-report

Windows (Planificateur de tâches)

PowerShell (en tant qu'administrateur) :

powershell
# Créer une tâche pour le diagnostic quotidien
$action = New-ScheduledTaskAction -Execute "C:\ntl-systoolbox\venv\Scripts\python.exe" -Argument "C:\ntl-systoolbox\ntl-systoolbox.py diagnostic --all" -WorkingDirectory "C:\ntl-systoolbox"
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "NTL Diagnostic" -Description "Diagnostic quotidien NTL"

# Créer une tâche pour la sauvegarde quotidienne
$action = New-ScheduledTaskAction -Execute "C:\ntl-systoolbox\venv\Scripts\python.exe" -Argument "C:\ntl-systoolbox\ntl-systoolbox.py backup --full --compress" -WorkingDirectory "C:\ntl-systoolbox"
$trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "NTL Backup" -Description "Sauvegarde quotidienne WMS"

Ou via l'interface graphique :

    Ouvrir le Planificateur de tâches

    Créer une tâche de base

    Programme : C:\ntl-systoolbox\venv\Scripts\python.exe

    Arguments : C:\ntl-systoolbox\ntl-systoolbox.py diagnostic --all

    Répertoire de démarrage : C:\ntl-systoolbox

Codes de retour
Code	Description
0	Succès
1	Avertissement
2	Critique
3	Erreur inconnue
4	Erreur de configuration
5	Erreur de connexion

Exemple d'utilisation dans un script :

bash
python ntl-systoolbox.py diagnostic --all
if [ $? -eq 2 ]; then
    echo "ALERTE: Problème critique détecté!"
fi

Structure des répertoires

text
NTL-SYSTOOLBOX/
├── logs/           # Fichiers de logs
├── backups/        # Sauvegardes générées
├── reports/        # Rapports d'audit
├── config.yaml     # Configuration principale
├── .env            # Variables secrètes (à créer)
└── ntl-systoolbox.py  # Script principal

Dépendances

Les principales dépendances sont :

    pyyaml : Lecture de la configuration

    mysql-connector-python : Connexion MySQL

    psutil : Monitoring système (optionnel)

Résolution des problèmes
Erreur de connexion MySQL

bash
# Vérifier la connectivité
ping 192.168.10.21

# Tester le port MySQL
telnet 192.168.10.21 3306  # Linux
Test-NetConnection -ComputerName 192.168.10.21 -Port 3306  # Windows

Erreur de permissions

Linux :

bash
# Vérifier les permissions du fichier .env
ls -la .env  # Doit être -rw-------

# Corriger si nécessaire
chmod 600 .env

Windows :

powershell
# Vérifier et corriger les permissions
icacls .env /inheritance:r /grant:r "%USERNAME%:F"

Module manquant

bash
# Réinstaller toutes les dépendances
pip install --force-reinstall -r requirements.txt

Documentation

    Dépôt GitHub

    Fichier config.yaml : Configuration complète avec commentaires

    Fichier .env.example : Template des variables d'environnement
