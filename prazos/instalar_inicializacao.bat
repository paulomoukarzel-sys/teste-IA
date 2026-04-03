@echo off
title Instalar Inicialização Automática — Controle de Prazos
echo.
echo  ══════════════════════════════════════════════
echo   Controle de Prazos — Inicialização Automática
echo   Gastão da Rosa ^& Moukarzel — Advogados
echo  ══════════════════════════════════════════════
echo.

set "VBS=%~dp0start_silent.vbs"
set "TASK=PrazosMoukarzel"

:: Remove tarefa anterior se existir
schtasks /delete /tn "%TASK%" /f >nul 2>&1

:: Cria nova tarefa no Task Scheduler
schtasks /create ^
  /tn "%TASK%" ^
  /tr "wscript.exe \"%VBS%\"" ^
  /sc ONLOGON ^
  /rl HIGHEST ^
  /delay 0000:30 ^
  /f >nul

if %ERRORLEVEL% == 0 (
  echo  [OK] Tarefa registrada com sucesso.
  echo.
  echo  O Controle de Prazos iniciara automaticamente
  echo  30 segundos apos o login no Windows.
  echo.
  echo  URL: http://localhost:5001
) else (
  echo  [ERRO] Falha ao registrar a tarefa.
  echo  Tente executar este arquivo como Administrador.
)

echo.
echo  Para remover a inicializacao automatica:
echo    schtasks /delete /tn "%TASK%" /f
echo.
pause
