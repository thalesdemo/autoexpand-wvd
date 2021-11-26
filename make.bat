@echo off
if [%1] == [] goto :default
if /I %1==install goto :install
if /I %1==clean goto :clean

:default
pipenv run pyinstaller --noconsole --icon=source\app.ico source\autoexpand-wvd-beta.py --onefile --dist .
echo End of compilation. Copying .EXE
copy autoexpand-wvd-beta.exe autoexpand-wvd-beta-unsigned.exe 
echo Applying digital signature to .exe executable ...
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe" sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a autoexpand-wvd-beta.exe
goto :eof

:install
pipenv install
echo Don't forget to run 'make' to compile the executable.
goto :eof

:clean
pipenv --rm 2>NUL
rmdir build /S /Q 2>NUL
del *.spec  *.exe /Q 2>NUL
goto :eof