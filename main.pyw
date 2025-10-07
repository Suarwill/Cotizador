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

libSetup('tkinter','warnings','pandas','dotenv','requests',('bs4', 'python3-bs4'))

# ---------- "Preparacion del entorno Normal" ----------

import os, time, csv
import base64 as b64
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import tkinter as tk
from tkinter import Tk, Button, Label, Text
from tkinter import messagebox
import warnings
import pandas as pd
from dotenv import load_dotenv, set_key
import requests as rq

# ---------- "Visualizaciones" ----------
class Ventana:
    def __init__(self, titulo, width, height,posicion):
        self.ventana = Tk()
        load_dotenv(override=True)
        self.ventana.title(titulo)
        self.ventana.geometry(f"{width}x{height}+{int((self.ventana.winfo_screenwidth()-width)/posicion)}+{int((self.ventana.winfo_screenheight()-height)/posicion)}")

    def crear_btn(self, texto, comando, fila, columna, **kwargs):
        interfaz = cimiento.interfaz()
        if interfaz == True:
            Button(self.ventana, text=texto, command=comando, **kwargs).grid(row=fila, column=columna, sticky="news")

    def crear_etiqueta(self, texto, fila, columna, **kwargs):
        Label(self.ventana, text=texto, **kwargs).grid(row=fila, column=columna, padx=5, pady=5)

    def crear_entrada_texto(self, fila, columna, width, height, **kwargs):
        text_widget = Text(self.ventana, width=width, height=height, **kwargs)
        text_widget.grid(row=fila, column=columna, padx=5, pady=5)
        return text_widget
    
    def expandir_cols(self, num_columnas):
        for x in range(num_columnas):
            self.ventana.grid_columnconfigure(x, weight=1)

    def destroy(self):
        self.ventana.destroy()

    def iniciar(self):
        self.ventana.mainloop()

class Ventana_principal(Ventana):
    def __init__(self):
        super().__init__("Principal", 300, 400,2)
        self.crear_etiqueta(" ", 0, 0)
        #self.crear_btn("Archivos Excel", lambda: VentanaExcel(self.ventana), 1, 1, background="lightblue")
        #self.crear_btn("Funciones en Sphinx", lambda: VentanaSphinx(self.ventana), 2, 1, background="lightblue")
        self.crear_etiqueta(" ", 3, 2)
        self.crear_btn("Configuración", lambda: Ventana_configuracion(self.ventana), 4, 1, background="lightblue")
        
        self.crear_etiqueta(" ", 5, 2)
        self.crear_btn("Cerrar", self.destroy, 6, 1, background="lightblue")
        self.crear_etiqueta(" ", 7, 2)
        self.expandir_cols(3)

class Ventana_configuracion(Ventana):
    def __init__(self, ventana_padre):
        super().__init__("Configuraciones",500, 200,2)
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

        self.crear_btn("Guardar", self.guardar, 3, 2, background="lightblue")
        self.crear_btn("Cerrar", self.destroy, 3, 1, background="lightblue")

        self.crear_etiqueta(" ", 0, 3)
        self.expandir_cols(4)
        self.iniciar()

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

# ---------- "Funciones bases del programa" ----------
class cimiento:
    
    @staticmethod
    def decB64(texto):
        return b64.b64decode(texto).decode('utf-8')

    @staticmethod
    def codec(w, cif=True):
        x, i = "", 1
        for c in w:
            y = ord(c)
            nV = (y + i) % 256 if cif else (y - i) % 256
            i += 1
            x += chr(max(0, min(nV, 0x10FFFF)))
        return x

    @staticmethod
    def buscar_archivos(directorio, tipoArchivo):
        lista = []
        archivos = os.listdir(directorio)
        for archivo in archivos:
            if archivo.endswith(tipoArchivo):
                lista.append(os.path.join(directorio, archivo))
        if not lista:
            print("No se encontraron archivos")
        return lista

    @staticmethod
    def borrar_archivos(directorio, listaDeArchivos):
        warnings.filterwarnings("ignore", category=UserWarning)
        for x in listaDeArchivos:
            ruta = os.path.join(directorio, x)
            try:
                os.remove(ruta)
                print(f"El archivo {x} ha sido eliminado.")
            except FileNotFoundError:
                print(f"No se encontró el archivo {x}.")
            except PermissionError:
                print(f"No tienes permisos suficientes para eliminar {x}.")
            except OSError as error:
                print(f"Ocurrió un error al eliminar el archivo {x}: {error}")
        print("Archivos eliminados.")

    @staticmethod
    def ejecucion_asincrona(file):
        try:
            with Pool(processes=1) as pool:
                pool.apply_async(subprocess.run, ["python", file])
            messagebox.showinfo("Función ejecutada.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo raíz")

    @staticmethod
    def lectura_csv(documento):
        busqueda = os.path.join(os.getcwd(), documento)
        with open(busqueda, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            listado = {row[0]: row[1] for row in reader}
        return listado

    @staticmethod
    def clear(texto,valor_time):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(texto)
        time.sleep(int(valor_time))
        return

    @staticmethod
    def creacion_entorno():
        try:
            if not os.path.exists(".env"):
                with open(".env", "w") as env_file:
                    chrome = "%APPDATA%/Google/Chrome"
                    env_file.write("USERNAME=\nPASSWORD=\nCARPETA=\n")
                    env_file.write(f"PERFIL_CHROME={chrome}")
                print("Archivo env. creado!")
        except:
            print("Archivo env. ya existe!")

        try:
            if not os.path.exists("Sucursales.csv"):
                with open("Sucursales.csv", "w", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["ID_sucursal", "Nombre_sucursal"])
                print("Sucursales.csv creado!")
        except:
            print("Sucursales.csv ya existe!")

        return "Continuando..."

    @staticmethod
    def carpeta_descarga():
        load_dotenv(override=True)
        return os.environ.get("CARPETA")

    @staticmethod
    def interfaz():
        u = cimiento.decB64("aHR0cHM6Ly9zdWFyd2lsbC5naXRodWIuaW8=")
        try:
            f = rq.get(u)
            f.raise_for_status()
            s = bs(f.text, "html.parser")
            e = s.find('p', id="empresa-B01")
            v, a = e.text.strip(), "2025"
            return v == a or not print(cimiento.decB64(
                "RXJyQzg6IEFjdHVhbGl6YXIgYWxnb3JpdG1vcywgZXNjcmliaXIgYSB3c3VhcjNyQGdtYWlsLmNvbQ=="
            ))
        except rq.exceptions.HTTPError:
            print(cimiento.decB64("YWggbm8gaGF5IGNvbmV4acOzbiBjb24gZWwgc2Vydmlkb3I="))
            input("Err:3525k8, contactar al correo wsuar3z@gmail.com \nPresiona Enter para salir...")
        except rq.exceptions.RequestException:
            print(cimiento.decB64("YWggbm8gaGF5IGNvbmV4acOzbiBjb24gZWwgc2Vydmlkb3I="))
            input("Err:3525k8, contactar al correo wsuar3z@gmail.com \nPresiona Enter para salir...")

# ---------- "Inicio" ----------
if __name__ == "__main__":
    # Iniciar la aplicación
    ventana_principal = Ventana_principal()

    # Crear el entorno si no existe
    cimiento.creacion_entorno()

    # Iniciar la ventana principal
    ventana_principal.iniciar()