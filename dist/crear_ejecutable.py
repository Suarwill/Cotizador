import subprocess
import os
from pathlib import Path
import sys

def obtener_ruta_sv_ttk() -> str | None:
    """Encuentra la ruta del paquete sv_ttk para incluir sus archivos de tema."""
    try:
        import sv_ttk
        # La ruta a la carpeta que contiene los archivos del tema
        return str(Path(sv_ttk.__file__).parent)
    except ImportError:
        print("Advertencia: El paquete 'sv-ttk' no está instalado en este entorno.")
        return None

def encontrar_icono(assets_dir: Path) -> str | None:
    """Busca un archivo .ico en el directorio de assets."""
    try:
        iconos = list(assets_dir.glob('*.ico'))
        if iconos:
            print(f"Icono encontrado: {iconos[0]}")
            return str(iconos[0])
    except Exception as e:
        print(f"No se pudo buscar el icono: {e}")
    return None

def listar_scripts() -> list[str]:
    """Lista los archivos .py y .pyw en el directorio actual, excluyendo este script."""
    scripts = [
        f for f in os.listdir() 
        if f.endswith(('.py', '.pyw')) and f != os.path.basename(__file__)
    ]
    return scripts

def elegir_script(scripts: list[str]) -> str:
    """Permite al usuario seleccionar un script de una lista."""
    print("Seleccione el archivo principal que desea convertir a ejecutable:\n")
    for idx, script in enumerate(scripts, 1):
        print(f"{idx}: {script}")

    while True:
        try:
            seleccion = int(input("\nIngrese el número del archivo: "))
            if 1 <= seleccion <= len(scripts):
                return scripts[seleccion - 1]
            else:
                print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Ingrese un número.")

def crear_exe(archivo_script: str):
    """Crea el ejecutable usando PyInstaller con las opciones adecuadas."""
    print("\n--- Iniciando la creación del ejecutable ---")
    
    # Opciones base de PyInstaller
    comando = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Cotizador"
    ]

    # Añadir icono si se encuentra
    icono = encontrar_icono(Path("assets"))
    if icono:
        comando.extend(["--icon", icono])

    # Añadir carpetas de datos y assets
    comando.extend(["--add-data", f"data{os.pathsep}data"])
    comando.extend(["--add-data", f"assets{os.pathsep}assets"])

    # Añadir los archivos del tema sv_ttk
    ruta_sv_ttk = obtener_ruta_sv_ttk()
    if ruta_sv_ttk:
        # El nombre del destino debe ser 'sv_ttk' para que el paquete lo encuentre
        comando.extend(["--add-data", f"{ruta_sv_ttk}{os.pathsep}sv_ttk"])

    # Añadir el script principal
    comando.append(archivo_script)

    print(f"\nEjecutando comando:\n{' '.join(comando)}\n")

    try:
        subprocess.run(comando, check=True)
        print(f"\n✅ ¡Éxito! El ejecutable 'Cotizador.exe' se ha creado en la carpeta 'dist'.")
    except FileNotFoundError:
        print("\n❌ Error: PyInstaller no está instalado. Por favor, instálalo con: pip install pyinstaller")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la compilación con PyInstaller: {e}")
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    scripts_disponibles = listar_scripts()
    if not scripts_disponibles:
        print("No se encontraron archivos .py o .pyw para compilar en esta carpeta.")
    else:
        script_elegido = elegir_script(scripts_disponibles)
        crear_exe(script_elegido)