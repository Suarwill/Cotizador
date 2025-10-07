# ---------- "Autoinstalador de librerias" ----------
import importlib, subprocess, sys, platform

def virtualizado():
    return sys.prefix != sys.base_prefix

def libSetup(*libs):
    for entry in libs:
        if isinstance(entry, tuple):
            lib, apt_pkg = entry
        else:
            lib, apt_pkg = entry, None

        try:
            importlib.import_module(lib)
        except ImportError:
            # Usar APT solo si no estamos en un venv y el sistema es Linux
            if platform.system() == 'Linux' and apt_pkg and not virtualizado():
                print(f"[+] Instalando {lib} con APT...")
                try:
                    subprocess.check_call(['sudo', 'apt', 'install', '-y', apt_pkg])
                except subprocess.CalledProcessError:
                    print(f"[!] Falló la instalación con APT. Intentando con pip...")
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            else:
                print(f"[+] Instalando {lib} con pip...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])

libSetup('tkinter','warnings','pandas','dotenv','requests',('bs4', 'python3-bs4'), 'sv_ttk')

# ---------- "Preparacion del entorno Normal" ----------

import os
import tkinter as tk
from tkinter import Tk, Text
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from dotenv import load_dotenv, set_key
import sv_ttk

# Importar desde archivos
from funciones_base import cimiento

# ---------- "Visualizaciones" ----------
class Ventana:
    def __init__(self, titulo, width, height, posicion, ventana_padre=None):
        if ventana_padre:
            self.ventana = tk.Toplevel(ventana_padre)
        else:
            self.ventana = tk.Tk()
            sv_ttk.set_theme("light")

            style = ttk.Style()
            style.configure('TButton', font=('Arial', 12), anchor='center')
            style.configure('TLabel', font=('Arial', 14))
            style.configure('TEntry', font=('Arial', 12), anchor='center')


        load_dotenv(override=True)
        self.ventana.title(titulo)
        self.ventana.geometry(f"{width}x{height}+{int((self.ventana.winfo_screenwidth() - width) / posicion)}+{int((self.ventana.winfo_screenheight() - height) / posicion)}")

    def crear_boton(self, texto, comando, fila, columna, **kwargs):
        interfaz = cimiento.interfaz()
        if interfaz == True:
            ttk.Button(self.ventana, text=texto, command=comando, **kwargs).grid(row=fila, column=columna, sticky="news", padx=10, pady=10)

    def crear_etiqueta(self, texto, fila, columna, **kwargs):
        ttk.Label(self.ventana, text=texto, **kwargs).grid(row=fila, column=columna, padx=5, pady=5)

    def crear_entrada_texto(self, fila, columna, width, height, **kwargs):
        text_widget = Text(self.ventana, width=width, height=height, **kwargs)
        text_widget.grid(row=fila, column=columna, padx=5, pady=5)
        return text_widget
    
    def expandir_columnas(self, num_columnas):
        for x in range(num_columnas):
            self.ventana.grid_columnconfigure(x, weight=1)

    def destroy(self):
        self.ventana.destroy()

    def iniciar(self):
        self.ventana.mainloop()

class VentanaPrincipal(Ventana):
    def __init__(self):
        super().__init__("Principal", 500, 400, 2)
        self.crear_etiqueta(" ", 0, 0)
        self.crear_boton("Clientes", lambda: VentanaClientes(self.ventana), 1, 1)
        self.crear_boton("Insumos", lambda: VentanaInsumos(self.ventana), 1, 3)
        self.crear_etiqueta(" ", 3, 0)
        self.crear_boton("Configuración", lambda: VentanaConfiguracion(self.ventana), 4, 2)
        
        self.crear_etiqueta(" ", 5, 0)
        self.crear_boton("Cerrar", self.destroy, 6, 2)
        self.crear_etiqueta(" ", 7, 4)
        self.expandir_columnas(5)

class VentanaClientes(Ventana):
    def __init__(self, ventana_padre):
        super().__init__("Clientes", 500, 400, 2, ventana_padre)
        self.crear_etiqueta(" ", 0, 0)
        self.crear_etiqueta("Cliente: ", 0, 1)
        self.datacliente =      self.crear_entrada_texto(0, 2, 30, 2)
        self.crear_etiqueta("RUT: ", 1, 1)
        self.datarut =          self.crear_entrada_texto(1, 2, 30, 2)
        self.crear_etiqueta("Dirección: ", 2, 1)
        self.datadireccion =    self.crear_entrada_texto(2, 2, 30, 2)
        self.crear_etiqueta("Teléfono: ", 3, 1)
        self.datatelefono =     self.crear_entrada_texto(3, 2, 30, 2)
        self.crear_etiqueta("Correo: ", 4, 1)
        self.datacorreo =       self.crear_entrada_texto(4, 2, 30, 2)
        self.crear_etiqueta(" ", 5, 3)

        self.crear_boton("Guardar", self.guardar, 0, 3)
        self.crear_boton("Buscar", self.buscar, 1, 3)
        self.crear_boton("Cerrar", self.destroy, 2, 3)


        self.crear_etiqueta(" ", 7, 2)
        self.expandir_columnas(3)

    def guardar(self):
        pass

    def buscar(self):
        pass


class VentanaInsumos(Ventana):
    def __init__(self, ventana_padre):
        super().__init__("Insumos", 500, 400, 2, ventana_padre)
        self.crear_etiqueta(" ", 0, 0)
        self.crear_etiqueta("Descripcion: ", 0, 1)
        self.crear_boton("Cerrar", self.destroy, 6, 1)
        self.crear_etiqueta(" ", 7, 2)
        self.expandir_columnas(3)

class VentanaConfiguracion(Ventana):
    def __init__(self, ventana_padre):
        super().__init__("Configuraciones", 500, 200, 2, ventana_padre)
        load_dotenv(override=True)

        self.crear_etiqueta(" ", 0, 0)
        self.crear_etiqueta("Usuario: ", 0, 1)
        self.crear_etiqueta("Contraseña: ", 1, 1)
        self.crear_etiqueta("Carpeta de descargas: ", 2, 1)

        self.userdata =     self.crear_entrada_texto(0, 2, 30, 1)
        self.contradata =   self.crear_entrada_texto(1, 2, 30, 1)
        self.carpeta =      self.crear_entrada_texto(2, 2, 30, 1)

        user = cimiento.codec(os.getenv("USERNAME"), False)
        self.userdata.insert(tk.END, user)
        pasw = cimiento.codec(os.getenv("PASSWORD"), False)
        self.contradata.insert(tk.END, pasw)
        carpeta = os.getenv("CARPETA")
        self.carpeta.insert(tk.END, carpeta)

        self.crear_boton("Guardar", self.guardar, 3, 2)
        self.crear_boton("Cerrar", self.destroy, 3, 1)

        self.crear_etiqueta(" ", 0, 3)
        self.expandir_columnas(4)

    def guardar(self):
        user = self.userdata.get("1.0", tk.END).strip()
        clave = self.contradata.get("1.0", tk.END).strip()
        carpeta = self.carpeta.get("1.0", tk.END).strip()

        if os.path.exists('.env'):
            set_key(".env", "USERNAME", cimiento.codec(user))
            set_key(".env", "PASSWORD", cimiento.codec(clave))
            set_key(".env", "CARPETA", carpeta)
            print("Archivos actualizados con éxito.")
            self.destroy()
        else:
            print("No se encontró el archivo .env")
        return

# ---------- "Inicio" ----------
if __name__ == "__main__":
    # Iniciar la aplicación
    ventana_principal = VentanaPrincipal()

    # Crear el entorno
    cimiento.creacion_entorno()

    # Iniciar la ventana principal
    ventana_principal.iniciar()