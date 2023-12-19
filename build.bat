@echo off
setlocal enabledelayedexpansion
setlocal enableextensions
set "root=%cd%"

echo.
echo Compiling for .exe
pyinstaller --clean -y --noconsole --add-data "func.py;." --add-data "php-logo.png;." --onefile gui.py
ren dist\gui.exe pwis.exe

echo.
echo Done^^! .exe should now be at .\dist\pwis.exe
pause
exit