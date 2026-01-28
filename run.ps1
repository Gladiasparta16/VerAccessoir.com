# Script de démarrage rapide

Write-Host "🚀 VerAccessoire - Démarrage du serveur" -ForegroundColor Cyan

# Vérifier l'environnement virtuel
if (-not (Test-Path ".venv")) {
    Write-Host "⚠️ Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activer
Write-Host "🔌 Activation..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Installer les dépendances s'il y a un fichier requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "📚 Installation des dépendances..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
}

# Démarrer
Write-Host "🎉 Démarrage du serveur..." -ForegroundColor Green
cd BACKEND
python app.py
