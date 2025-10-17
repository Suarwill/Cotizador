@echo off
setlocal

REM --- Script para crear el entorno, instalar Python y dependencias, y ejecutar la aplicacion ---

echo Creando directorio de la aplicacion...
set "INSTALL_DIR=C:\Katech\Cotizador"
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo Directorio creado en: %INSTALL_DIR%
) else (
    echo El directorio ya existe: %INSTALL_DIR%
)

echo.
echo Copiando archivos de la aplicacion...
REM Asumimos que el script esta en una carpeta 'installer' y los archivos estan un nivel arriba.
copy "..\main.py" "%INSTALL_DIR%\" > nul
copy "..\requirements.txt" "%INSTALL_DIR%\" > nul
xcopy "..\assets" "%INSTALL_DIR%\assets\" /E /I /Y > nul
echo Archivos copiados.

echo.
echo Creando acceso directo en el escritorio...
set "SHORTCUT_NAME=Katech - Cotizador.lnk"
set "TARGET_PATH=%INSTALL_DIR%\main.py"
set "ICON_PATH=%INSTALL_DIR%\assets\logo.ico"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\%SHORTCUT_NAME%'); $s.TargetPath = '%SystemRoot%\py.exe'; $s.Arguments = '-m main'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.IconLocation = '%ICON_PATH%'; $s.Save()"
echo Acceso directo creado.

echo.

echo Verificando la instalacion de Python...

REM Intenta encontrar la ruta de Python
where py >nul 2>nul
if %errorlevel% == 0 (
    echo Python ya esta instalado.
) else (
    echo Python no encontrado. Intentando instalar...
    
    REM Intenta usar winget (metodo moderno en Windows 10/11)
    where winget >nul 2>nul
    if %errorlevel% == 0 (
        echo Usando winget para instalar la ultima version de Python...
        winget install -e --id Python.Python.3.12 --silent --source winget --accept-package-agreements --accept-source-agreements
    ) else (
        echo winget no encontrado. Descargando instalador de python.org...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe' -OutFile 'python_installer.exe'"
        echo Instalando Python...
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
        del python_installer.exe
    )

    REM Verificar de nuevo despues de la instalacion
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: La instalacion de Python fallo o no se agrego al PATH.
        echo Por favor, instale Python 3.12 manualmente desde python.org y asegurese de marcar "Add Python to PATH".
        pause
        exit /b 1
    )
)

echo.
echo Instalando/actualizando dependencias del proyecto en %INSTALL_DIR%...

REM Cambiar al directorio de instalacion para que pip y la app funcionen correctamente
cd /d "%INSTALL_DIR%"

REM Instala las librerias desde requirements.txt
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

echo.
echo Iniciando la aplicacion por primera vez para la configuracion inicial...
py main.py

echo.
echo -----------------------------------------------------------------
echo Proceso de instalacion finalizado.
echo.
echo Puedes iniciar la aplicacion desde el acceso directo:
echo "Katech - Cotizador" en tu escritorio.
echo -----------------------------------------------------------------
echo.
pause

endlocal