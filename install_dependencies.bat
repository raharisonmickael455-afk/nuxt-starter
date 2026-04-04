@echo off
REM Script d'installation des dépendances Python

echo.
echo =====================================
echo   Installation des dépendances
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé
    echo Téléchargez Python depuis: https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python trouvé
echo.
echo Mise à jour de pip...
python -m pip install --upgrade pip

echo.
echo Installation des dépendances depuis requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERREUR: L'installation a échoué
    pause
    exit /b 1
)

echo.
echo ✓ Toutes les dépendances ont été installées avec succès!
echo.
echo Vous pouvez maintenant lancer le serveur:
echo   python app.py
echo.

pause
