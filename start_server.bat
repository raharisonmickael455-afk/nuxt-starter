@echo off
REM Démarrer le serveur Flask Facebook Backend sur Windows

echo.
echo =====================================
echo   Facebook Login Backend
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Téléchargez Python depuis: https://www.python.org
    pause
    exit /b 1
)

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
pip list | findstr Flask >nul 2>&1
if errorlevel 1 (
    echo Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR: L'installation a échoué
        pause
        exit /b 1
    )
)

echo.
echo ✓ Dépendances vérifiées
echo.
echo Démarrage du serveur...
echo.
echo Le serveur s'exécute sur: http://localhost:5000
echo.
echo Endpoints disponibles:
echo  - POST   /api/signup
echo  - POST   /api/login
echo  - GET    /api/users
echo  - GET    /api/connection-data
echo  - GET    /api/login-logs
echo  - GET    /api/stats
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

python app.py

pause
