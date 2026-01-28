# Script de configuration pour Windows PowerShell

Write-Host "`n"
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   VerAccessoire - Configuration Automatique (Windows)  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Vérifier si on est à la racine du projet
if (-not (Test-Path "BACKEND")) {
    Write-Host "❌ Erreur: Veuillez exécuter ce script depuis la racine du projet" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel s'il n'existe pas
if (-not (Test-Path ".venv")) {
    Write-Host "🔧 Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Environnement virtuel créé" -ForegroundColor Green
} else {
    Write-Host "✅ Environnement virtuel existant" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host "`n🔌 Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Installer/mettre à jour pip
Write-Host "`n📚 Installation des dépendances..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Installer les dépendances du projet
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'installation des dépendances" -ForegroundColor Red
    exit 1
}

# Exécuter le script de configuration
Write-Host "`n⚙️ Exécution du script de configuration..." -ForegroundColor Yellow
Set-Location BACKEND
python setup.py
Set-Location ..

# Demander si l'utilisateur veut démarrer le serveur
Write-Host "`n" -ForegroundColor Green
$response = Read-Host "🚀 Voulez-vous démarrer le serveur maintenant? (y/n)"

if ($response -eq 'y' -or $response -eq 'yes') {
    Write-Host "`n🚀 Démarrage du serveur Flask..." -ForegroundColor Green
    Set-Location BACKEND
    python app.py
} else {
    Write-Host "`n✅ Configuration terminée!" -ForegroundColor Green
    Write-Host "`nPour démarrer le serveur plus tard, exécutez:" -ForegroundColor Cyan
    Write-Host "  cd BACKEND`n  python app.py" -ForegroundColor White
}
