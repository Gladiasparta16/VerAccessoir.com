@echo off
setlocal enabledelayedexpansion

REM Démarrer le serveur Flask
cd /d "%~dp0"

REM Vérifier si venv existe
if not exist ".venv" (
    echo Création de l'environnement virtuel...
    python -m venv .venv
)

REM Activer venv
call .venv\Scripts\activate.bat

REM Installer/mettre à jour les dépendances
echo Installation des dépendances...
python -m pip install -q -r BACKEND/requirements.txt

REM Lancer le serveur
echo.
echo ====================================
echo Serveur démarré sur http://localhost:5000
echo ====================================
echo.
python BACKEND/app.py
