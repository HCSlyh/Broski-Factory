@echo off
title BroskiNet Factory - Piattaforma di Input
cls

echo ===================================================
echo   🚀 BUNDLE DI BASE IN ASCOLTO - BROSKINET SAAS
echo ===================================================
echo.
cd /d "C:\Users\Slyh\Desktop\Factory\BroskiNet"

echo Scegli il tipo di attività che sta effettuando l'accesso:
echo [1] PARRUCCHIERE / MACELLAIO (Categoria: COMMERCE)
echo [2] BROKER / BANCA (Categoria: FINANCE)
echo [3] NOLEGGIO AUTO / AGENZIA (Categoria: SERVICES)
echo.
set /p scelta="Digita il numero (1, 2 o 3) e premi Invio: "

if "%scelta%"=="1" set CAT=COMMERCE
if "%scelta%"=="2" set CAT=FINANCE
if "%scelta%"=="3" set CAT=SERVICES

cls
echo ===================================================
echo   STEP 1: RICHIESTA OPZIONI DALLA MATRICE
echo ===================================================
echo [PIATTAFORMA] Invio richiesta per categoria: %CAT%
echo [MATRICE] Ecco la lista di agenti che la piattaforma deve mostrare a schermo:
echo.

python orchestrator.py --get-options %CAT%

echo.
echo ===================================================
echo [FINE TEST] La factory ha estratto solo i nodi corretti.
echo Il cliente vedrà SOLO questa lista tra cui scegliere.
echo ===================================================
pause
