set str=%~f0
set str=%str:.bat=%.ps1
powershell.exe -ep Bypass %str%