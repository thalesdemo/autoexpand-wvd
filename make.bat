pyinstaller.exe --onefile --noconsole --icon=app.ico autoexpand-wvd-alpha.py
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe" sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a autoexpand-wvd-alpha.exe
pause
