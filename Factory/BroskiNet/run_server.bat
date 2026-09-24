@echo off
title BroskiNet Factory - Web App Server
cls

echo ===================================================
echo   🚀 AVVIO INTERFACCIA GRAFICA - BROSKINET CORE
echo ===================================================
echo.

cd /d "C:\Users\Slyh\Desktop\Factory\BroskiNet"

echo [INFO] Controllo l'integrità strutturale del server...
if not exist app.py (
    echo [ERRORE] File app.py non trovato!
    goto end
)
if not exist templates\index.html (
    echo [ERRORE] File templates\index.html non trovato!
    goto end
)

echo [INFO] Struttura OK. Avvio il server Flask locale...
echo [INFO] Aprendo l'interfaccia nel browser tra 3 secondi...
echo.

:: Aspetta 3 secondi e lancia il browser predefinito sull'indirizzo locale
timeout /t 3 /nobreak > nul
start http://127.0.0

:: Avvia il server Python
python app.py

:end
echo.
echo ===================================================
echo [INFO] Server arrestato o errore di configurazione.
echo ===================================================
pause
