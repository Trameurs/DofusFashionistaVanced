@echo off
REM Script Docker simple pour DofusFashionista sur Windows
echo.
echo ========================================
echo   DofusFashionista Docker Setup 
echo ========================================
echo.

REM Vérifier si Docker est installé
docker --version >nul 2>&1
if errorlevel 1 (
    echo Erreur: Docker n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Docker Desktop depuis:
    echo https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Vérifier si Docker Compose est disponible
docker compose version >nul 2>&1
if errorlevel 1 (
    echo Erreur: Docker Compose n'est pas disponible
    echo Veuillez installer Docker Desktop avec Compose
    pause
    exit /b 1
)

echo Docker et Docker Compose sont installés
echo.

REM Arrêter et supprimer les conteneurs existants si nécessaire
echo Nettoyage des conteneurs existants...
docker compose down -v 2>nul

echo.
echo Construction et démarrage des conteneurs...
echo Cela peut prendre quelques minutes la première fois...
echo.

REM Construire et démarrer les conteneurs
docker compose up --build -d

if errorlevel 1 (
    echo.
    echo Erreur lors du démarrage des conteneurs
    echo.
    echo Logs des conteneurs:
    docker compose logs
    echo.
    pause
    exit /b 1
)

echo.
echo DofusFashionista est en cours de démarrage !
echo.
echo URLs d'accès:
echo - Application: http://localhost:8000
echo - Base de données MySQL: localhost:3306
echo.
echo Commandes utiles:
echo - Voir les logs: docker compose logs -f
echo - Arrêter: docker compose down
echo - Redémarrer: docker compose restart
echo.

REM Attendre que les services soient prêts
echo Attente que les services soient prêts...
timeout /t 5 /nobreak >nul

REM Vérifier le statut des conteneurs
docker compose ps

echo.
echo Ouverture de l'application dans le navigateur...
start http://localhost:8000

echo.
echo Installation terminée !
echo L'application devrait s'ouvrir dans votre navigateur.
echo Si ce n'est pas le cas, allez sur http://localhost:8000
echo.
pause
