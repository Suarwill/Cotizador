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

# Lista a instalar ()
# ---> Sublista (opcion 1, opcion 2)
libSetup('tkinter','warnings','pandas','dotenv','requests',('bs4', 'python3-bs4'), 'sv_ttk')

# ---------- "Preparacion del entorno Normal" ----------

import os
import csv
from dotenv import load_dotenv, set_key

import tkinter as tk
import sv_ttk
from tkinter import Tk, Text
from tkinter import ttk
from tkinter import messagebox

import pandas as pd

# Importar desde archivos
from funciones_base import cimiento

# ---------- "Componentes Base de la UI" ----------
class VistaBase:
    def crear_boton(self, texto, comando, fila, columna, **kwargs):
        ttk.Button(self, text=texto, command=comando, **kwargs).grid(row=fila, column=columna, sticky="news", padx=10, pady=10)

    def crear_etiqueta(self, texto, fila, columna, **kwargs):
        ttk.Label(self, text=texto, **kwargs).grid(row=fila, column=columna, padx=5, pady=5)

    def crear_entrada_texto(self, fila, columna, width, height, **kwargs):
        text_widget = Text(self, width=width, height=height, **kwargs)
        text_widget.grid(row=fila, column=columna, padx=5, pady=5)
        return text_widget

    def expandir_columnas(self, num_columnas):
        for x in range(num_columnas):
            self.grid_columnconfigure(x, weight=1)

# ---------- "Visualizaciones" ----------
class Ventana(VistaBase):
    def __init__(self, titulo, width, height, posicion, ventana_padre=None):
        if ventana_padre:
            self.ventana = tk.Toplevel(ventana_padre)
        else:
            self.ventana = tk.Tk()
            sv_ttk.set_theme("light")

            style = ttk.Style()
            style.configure('TButton', font=('Arial', 12), anchor='center')
            style.configure('TLabel', font=('Arial', 12))

        load_dotenv(override=True)
        self.ventana.title(titulo)
        self.ventana.geometry(f"{width}x{height}+{int((self.ventana.winfo_screenwidth() - width) / posicion)}+{int((self.ventana.winfo_screenheight() - height) / posicion)}")

    def hacer_modal(self):
        self.ventana.transient(self.ventana.master)
        self.ventana.grab_set()
        self.ventana.wait_window(self.ventana)

    def destroy(self):
        self.ventana.destroy()

    def iniciar(self):
        self.ventana.mainloop()

class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        sv_ttk.set_theme("light")
        self.ventana.title("Principal")
        width, height, posicion = 800, 600, 2
        self.ventana.geometry(f"{width}x{height}+{int((self.ventana.winfo_screenwidth() - width) / posicion)}+{int((self.ventana.winfo_screenheight() - height) / posicion)}")

        # --- Barra de Menú ---
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar)

        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Configuración", command=lambda: self._mostrar_frame(VentanaConfiguracion))
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.ventana.quit)

        # Menú Cotizaciones
        cotizacion_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cotizaciones", menu=cotizacion_menu)
        cotizacion_menu.add_command(label="Crear Cotización", command=lambda: self._mostrar_frame(VentanaCrearCotizacion))
        cotizacion_menu.add_command(label="Buscar Cotización", command=lambda: self._mostrar_frame(VentanaBuscarCotizacion))

        # Menú Productos
        productos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Productos", menu=productos_menu)
        productos_menu.add_command(label="Insumos", command=lambda: self._mostrar_frame(VentanaInsumos))

        # Menú Clientes
        menubar.add_command(label="Clientes", command=lambda: self._mostrar_frame(VentanaClientes))

        # --- Contenedor Principal para los frames ---
        self.container = ttk.Frame(self.ventana)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _mostrar_frame(self, ClaseDelFrame):
        # Limpia el frame anterior
        for widget in self.container.winfo_children():
            widget.destroy()
        # Crea y muestra el nuevo frame
        frame = ClaseDelFrame(parent=self.container)
        frame.grid(row=0, column=0, sticky="nsew")

    def iniciar(self):
        self.ventana.mainloop()

class VentanaClientes(ttk.Frame, VistaBase):
    def __init__(self, parent):
        super().__init__(parent)
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
        self.crear_boton("Buscar", self.abrir_ventana_busqueda, 1, 3)
        self.crear_boton("Cerrar", self.destroy, 2, 3)

        self.crear_etiqueta(" ", 7, 2)
        self.expandir_columnas(3)

    def guardar(self):
        nombre = self.datacliente.get("1.0", tk.END).strip()
        rut = self.datarut.get("1.0", tk.END).strip()
        direccion = self.datadireccion.get("1.0", tk.END).strip()
        telefono = self.datatelefono.get("1.0", tk.END).strip()
        correo = self.datacorreo.get("1.0", tk.END).strip()

        if not nombre or not rut:
            messagebox.showwarning("Campos requeridos", "El Nombre y el RUT son obligatorios.")
            return

        datos_cliente = [nombre, rut, direccion, telefono, correo]
        ruta_archivo = os.path.join("data", "data_cliente.csv")

        try:
            with open(ruta_archivo, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(datos_cliente)
            
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            # Limpiar campos después de guardar
            self.datacliente.delete("1.0", tk.END)
            self.datarut.delete("1.0", tk.END)
            self.datadireccion.delete("1.0", tk.END)
            self.datatelefono.delete("1.0", tk.END)
            self.datacorreo.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar el cliente:\n{e}")

    def _cargar_cliente_seleccionado(self, datos_cliente):
        """Limpia los campos y carga los datos del cliente seleccionado."""
        # Limpiar campos
        self.datacliente.delete("1.0", tk.END)
        self.datarut.delete("1.0", tk.END)
        self.datadireccion.delete("1.0", tk.END)
        self.datatelefono.delete("1.0", tk.END)
        self.datacorreo.delete("1.0", tk.END)

        # Cargar nuevos datos
        self.datacliente.insert("1.0", datos_cliente[0])
        self.datarut.insert("1.0", datos_cliente[1])
        self.datadireccion.insert("1.0", datos_cliente[2])
        self.datatelefono.insert("1.0", datos_cliente[3])
        self.datacorreo.insert("1.0", datos_cliente[4])

    def abrir_ventana_busqueda(self):
        # Crea la ventana de selección y la hace modal
        ventana_busqueda = VentanaSeleccionarCliente(self.winfo_toplevel(), self._cargar_cliente_seleccionado)
        ventana_busqueda.hacer_modal()

class VentanaSeleccionarCliente(Ventana):
    def __init__(self, ventana_padre, callback_seleccion):
        super().__init__("Seleccionar Cliente", 700, 400, 2, ventana_padre)
        self.callback = callback_seleccion

        # --- Treeview para mostrar clientes ---
        columnas = ("Nombre", "RUT", "Direccion", "Telefono", "Correo")
        self.tree = ttk.Treeview(self.ventana, columns=columnas, show='headings')

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='w')

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        self.cargar_clientes_csv()

        # --- Evento de selección ---
        self.tree.bind("<Double-1>", self.on_cliente_seleccionado)

    def cargar_clientes_csv(self):
        ruta_archivo = os.path.join("data", "data_cliente.csv")
        try:
            with open(ruta_archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Omitir la cabecera
                for row in reader:
                    self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            messagebox.showwarning("Archivo no encontrado", "No se encontró el archivo 'data/data_cliente.csv'.")
        except Exception as e:
            messagebox.showerror("Error de lectura", f"No se pudo leer el archivo de clientes:\n{e}")

    def on_cliente_seleccionado(self, event):
        item_seleccionado = self.tree.focus()
        if item_seleccionado:
            datos_cliente = self.tree.item(item_seleccionado)['values']
            self.callback(datos_cliente)
            self.destroy()

class VentanaCrearCotizacion(ttk.Frame, VistaBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.crear_etiqueta(" ", 0, 0)

class VentanaBuscarCotizacion(ttk.Frame, VistaBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.crear_etiqueta(" ", 0, 0)

class VentanaInsumos(ttk.Frame, VistaBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.crear_etiqueta(" ", 0, 0)
        self.crear_etiqueta("Descripción 1:", 1, 1)
        self.datadesc1 =      self.crear_entrada_texto(1, 2, 30, 1)
        self.crear_etiqueta("Descripción 2:", 2, 1)
        self.datadesc2 =      self.crear_entrada_texto(2, 2, 30, 1)
        self.crear_etiqueta("Descripción 3:", 3, 1)
        self.datadesc3 =      self.crear_entrada_texto(3, 2, 30, 1)
        self.crear_etiqueta("Unidad:", 4, 1)
        self.dataunidad =     self.crear_entrada_texto(4, 2, 30, 1)
        self.crear_etiqueta("Costo:", 5, 1)
        self.datacosto =      self.crear_entrada_texto(5, 2, 30, 1)
        self.crear_etiqueta("Precio:", 6, 1)
        self.dataprecio =     self.crear_entrada_texto(6, 2, 30, 1)

        self.crear_boton("Guardar", self.guardar, 1, 3)
        self.crear_boton("Buscar", self.abrir_ventana_busqueda, 2, 3)
        self.crear_boton("Cerrar Vista", self.destroy, 3, 3)

        self.expandir_columnas(4)

    def guardar(self):
        desc1 = self.datadesc1.get("1.0", tk.END).strip()
        if not desc1:
            messagebox.showwarning("Campo requerido", "La 'Descripción 1' es obligatoria.")
            return

        datos_insumo = [
            desc1,
            self.datadesc2.get("1.0", tk.END).strip(),
            self.datadesc3.get("1.0", tk.END).strip(),
            self.dataunidad.get("1.0", tk.END).strip(),
            self.datacosto.get("1.0", tk.END).strip(),
            self.dataprecio.get("1.0", tk.END).strip()
        ]

        ruta_archivo = os.path.join("data", "data_productos.csv")
        try:
            with open(ruta_archivo, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(datos_insumo)
            
            messagebox.showinfo("Éxito", "Insumo guardado correctamente.")
            # Limpiar campos
            for widget in [self.datadesc1, self.datadesc2, self.datadesc3, self.dataunidad, self.datacosto, self.dataprecio]:
                widget.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar el insumo:\n{e}")

    def _cargar_insumo_seleccionado(self, datos_insumo):
        widgets = [self.datadesc1, self.datadesc2, self.datadesc3, self.dataunidad, self.datacosto, self.dataprecio]
        for widget in widgets:
            widget.delete("1.0", tk.END)

        for widget, dato in zip(widgets, datos_insumo):
            widget.insert("1.0", dato)

    def abrir_ventana_busqueda(self):
        ventana_busqueda = VentanaSeleccionarInsumo(self.winfo_toplevel(), self._cargar_insumo_seleccionado)
        ventana_busqueda.hacer_modal()

class VentanaSeleccionarInsumo(Ventana):
    def __init__(self, ventana_padre, callback_seleccion):
        super().__init__("Seleccionar Insumo", 800, 400, 2, ventana_padre)
        self.callback = callback_seleccion

        columnas = ("Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "Costo", "Precio")
        self.tree = ttk.Treeview(self.ventana, columns=columnas, show='headings')
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='w')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.cargar_insumos_csv()
        self.tree.bind("<Double-1>", self.on_insumo_seleccionado)

    def cargar_insumos_csv(self):
        ruta_archivo = os.path.join("data", "data_productos.csv")
        try:
            with open(ruta_archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Omitir cabecera
                for row in reader:
                    self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            messagebox.showwarning("Archivo no encontrado", "No se encontró 'data/data_productos.csv'.")
        except Exception as e:
            messagebox.showerror("Error de lectura", f"No se pudo leer el archivo de insumos:\n{e}")

    def on_insumo_seleccionado(self, event):
        item_seleccionado = self.tree.focus()
        if item_seleccionado:
            datos_insumo = self.tree.item(item_seleccionado)['values']
            self.callback(datos_insumo)
            self.destroy()

class VentanaConfiguracion(ttk.Frame, VistaBase):
    def __init__(self, parent):
        super().__init__(parent)
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
        self.crear_boton("Cerrar Vista", self.destroy, 3, 1)

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