@echo off
echo ===============================================
echo Lancement de DofusFashionistaVanced pour Windows 11...
echo Launching DofusFashionistaVanced for Windows 11...
echo ===============================================
echo.

REM Exécute le script PowerShell avec les paramètres adaptés
REM Run the PowerShell script with the appropriate parameters
powershell -NoProfile -ExecutionPolicy RemoteSigned -File "%~dp0run_windows11.ps1" %*

REM Si PowerShell rencontre une erreur, on l'affiche 
REM If PowerShell encounters an error, display it
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ==================================================
    echo Une erreur s'est produite lors du lancement.
    echo An error occurred while starting the application.
    echo.
    echo Code d'erreur : %ERRORLEVEL%
    echo Error code    : %ERRORLEVEL%
    echo.
    echo Vérifiez les logs dans le dossier "logs" pour plus d'informations.
    echo Check the logs in the "logs" folder for more information.
    echo ==================================================
    pause
)