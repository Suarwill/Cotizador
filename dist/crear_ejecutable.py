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

def crear_exe():
    """Crea el ejecutable usando PyInstaller con las opciones adecuadas."""
    archivo_script = "main.pyw"
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

    # Forzar la inclusión del módulo sv_ttk que PyInstaller podría no detectar
    comando.extend(["--hidden-import", "sv_ttk"])

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
    # Ahora el script de compilación es más simple y directo.
    crear_exe()