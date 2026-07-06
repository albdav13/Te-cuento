@echo off
cd /d "%~dp0"

echo ==========================================
echo  Te cuento la pelicula - Administrador
echo ==========================================
echo.

py -c "import flask, bs4" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias necesarias...
    py -m pip install flask beautifulsoup4
)

echo.
echo Abriendo administrador local...
start http://127.0.0.1:5000

py admin\app.py

pause