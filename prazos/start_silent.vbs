' Inicia o Controle de Prazos em segundo plano (sem janela CMD)
' Gastão da Rosa & Moukarzel — Advogados Associados

Dim oShell, oFSO, sDir, sPython, sScript

Set oShell = CreateObject("WScript.Shell")
Set oFSO   = CreateObject("Scripting.FileSystemObject")

' Diretório deste script
sDir = oFSO.GetParentFolderName(WScript.ScriptFullName)

' Localiza o Python no PATH
sPython = "python"
sScript = sDir & "\app.py"

' Inicia sem janela (0 = oculto)
oShell.Run """" & sPython & """ """ & sScript & """", 0, False

Set oShell = Nothing
Set oFSO   = Nothing
