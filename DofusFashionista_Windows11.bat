@echo off
echo Lancement de DofusFashionistaVanced pour Windows 11...
echo.

REM Exécute le script PowerShell avec les paramètres adaptés
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_windows11.ps1"

REM Si PowerShell rencontre une erreur, on l'affiche
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Une erreur s'est produite lors du lancement. Code d'erreur: %ERRORLEVEL%
    echo Vérifiez les logs dans le dossier "logs" pour plus d'informations.
    pause
)