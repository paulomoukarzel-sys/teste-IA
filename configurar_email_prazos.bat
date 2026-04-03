@echo off
title Configurar E-mail — Controle de Prazos
cd /d "%~dp0prazos"
echo.
echo  ══════════════════════════════════════════════
echo   Configuração do Leitor de E-mail
echo   Gastão da Rosa ^& Moukarzel — Advogados
echo  ══════════════════════════════════════════════
echo.
pip install flask requests --quiet
echo.
python configurar_email.py
pause
