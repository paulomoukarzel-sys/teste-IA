@echo off
title Controle de Prazos — Gastão da Rosa ^& Moukarzel
cd /d "%~dp0prazos"
echo.
echo  ══════════════════════════════════════════════
echo   Controle de Prazos e Compromissos
echo   Gastão da Rosa ^& Moukarzel — Advogados
echo  ══════════════════════════════════════════════
echo.
echo  Verificando dependencias...
pip install flask --quiet
echo.
echo  Iniciando servidor em http://localhost:5001
echo  Pressione CTRL+C para encerrar.
echo.
start "" http://localhost:5001
python app.py
pause
