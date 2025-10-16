@echo off
setlocal

REM --- Script para instalar Python y dependencias, y ejecutar la aplicacion ---

echo Verificando la instalacion de Python...

REM Intenta encontrar la ruta de Python
where python >nul 2>nul
if %errorlevel% == 0 (
    echo Python ya esta instalado.
) else (
    echo Python no encontrado. Intentando instalar...
    
    REM Intenta usar winget (metodo moderno en Windows 10/11)
    winget --version >nul 2>nul
    if %errorlevel% == 0 (
        echo Usando winget para instalar la ultima version de Python...
        winget install -e --id Python.Python.3 --silent --source winget --accept-package-agreements --accept-source-agreements
    ) else (
        echo winget no encontrado. Descargando instalador de python.org...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile 'python_installer.exe'"
        echo Instalando Python...
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
        del python_installer.exe
    )

    REM Verificar de nuevo despues de la instalacion
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: La instalacion de Python fallo o no se agrego al PATH.
        echo Por favor, instale Python manualmente desde python.org y asegurese de marcar "Add Python to PATH".
        pause
        exit /b 1
    )
)

echo.
echo Instalando/actualizando dependencias del proyecto...

REM Instala las librerias desde requirements.txt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Iniciando la aplicacion...
python ../main.py

endlocal