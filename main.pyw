# ---------- "Autoinstalador de librerias" ----------
import importlib, subprocess, sys, platform

def virtualizado():
    return sys.prefix != sys.base_prefix

def libSetup(*libs, update_status=None):
    for entry in libs:
        if isinstance(entry, tuple):
            lib, apt_pkg = entry
        else:
            lib, apt_pkg = entry, None

        try:
            importlib.import_module(lib)
            if update_status:
                update_status(f"Librería '{lib}' ya está instalada.", 100)
        except ImportError:
            if update_status:
                update_status(f"Instalando librería '{lib}'...", 0)
            
            # Usar APT solo si no estamos en un venv y el sistema es Linux
            if platform.system() == 'Linux' and apt_pkg and not virtualizado():
                try:
                    subprocess.check_call(['sudo', 'apt', 'install', '-y', apt_pkg])
                except subprocess.CalledProcessError:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            else:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            
            if update_status:
                update_status(f"Librería '{lib}' instalada.", 100)

# Lista a instalar ()
# ---> Sublista (opcion 1, opcion 2)
LIBS_A_INSTALAR = ['warnings','pandas','dotenv','requests',('bs4', 'python3-bs4'), 'sv_ttk', 'reportlab']

# Importar desde archivos
from funciones_base import cimiento
from funciones_ventanas import VentanaPrincipal

# Importacion inicial
libSetup('tkinter')
import tkinter as tk
from tkinter import ttk

# ---------- "Inicio" ----------
if __name__ == "__main__":
    
    # --- Ventana de Carga (Splash Screen) ---
    splash_root = tk.Tk()
    splash_root.title("Cargando...")
    
    window_width, window_height = 450, 120
    center_x = int(splash_root.winfo_screenwidth()/2 - window_width / 2)
    center_y = int(splash_root.winfo_screenheight()/2 - window_height / 2)
    splash_root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    splash_root.resizable(False, False)
    splash_root.config(padx=20, pady=10)

    status_label = ttk.Label(splash_root, text="Iniciando aplicación...", anchor="w", width=50)
    status_label.pack(pady=5, fill="x")
    progress_bar = ttk.Progressbar(splash_root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=5)

    def update_status(message, progress):
        status_label.config(text=message)
        progress_bar['value'] = progress
        splash_root.update_idletasks()

    splash_root.update()

    # --- Instalación y Configuración ---
    libSetup(*LIBS_A_INSTALAR, update_status=update_status)
    cimiento.creacion_entorno(update_status=update_status)

    # --- Iniciar la Aplicación Principal ---
    splash_root.destroy()
    ventana_principal = VentanaPrincipal()
    ventana_principal.iniciar()