@echo off
REM Script pour exécuter DofusFashionistaVanced avec Docker sous Windows

REM Vérifier si Docker est installé
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker n'est pas installe. Veuillez l'installer d'abord.
    exit /b 1
)

REM Vérifier si Docker Compose est installé
where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker Compose n'est pas installe. Veuillez l'installer d'abord.
    exit /b 1
)

REM Configuration du projet pour Docker
echo Configuration du projet pour Docker...
python configure_docker.py

REM Construction des images Docker
echo Construction des images Docker...
docker-compose build

REM Démarrage des conteneurs
echo Demarrage des conteneurs...
docker-compose up -d

echo.
echo ==================================================
echo DofusFashionistaVanced est maintenant lance!
echo Vous pouvez y acceder a l'adresse: http://localhost:8000
echo Pour voir les logs: docker-compose logs -f
echo Pour arreter: docker-compose down
echo ==================================================

pause
