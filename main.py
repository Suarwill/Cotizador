# ---------- "Autoinstalador de librerias" ----------
import sys, time, importlib, os, platform, subprocess
from multiprocessing import Pool
from pathlib import Path

def virtualizado():
    return sys.prefix != sys.base_prefix

def libSetup(*libs, update_status=None):
    """Instala librerías si no están presentes, con soporte para nombres de paquete específicos de pip y apt."""
    for entry in libs:
        if isinstance(entry, tuple) and len(entry) == 3:
            lib, pip_pkg, apt_pkg = entry
        elif isinstance(entry, tuple) and len(entry) == 2:
            lib, apt_pkg = entry
            pip_pkg = lib  # Asumir que el nombre de pip es el mismo que el de importación
        else:
            lib, pip_pkg, apt_pkg = entry, entry, None
        
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
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_pkg])
            else:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_pkg])

            if update_status:
                update_status(f"Librería '{lib}' instalada.", 100)

# Lista a instalar (incluyendo 'tkinter' para asegurar su disponibilidad)
# ---> Sublista (opcion 1, opcion 2)
LIBS_A_INSTALAR = ['tkinter', ('sv_ttk', 'sv-ttk', None), 'warnings','dotenv','requests',('bs4', 'beautifulsoup4', 'python3-bs4'), 'reportlab']

# Ejecutar libSetup para todas las librerías antes de cualquier importación de UI
libSetup(*LIBS_A_INSTALAR)

# --- Importaciones de UI (después de la instalación) ---
from datetime import datetime

import tkinter as tk
from tkinter import (Tk, Text, filedialog, messagebox, simpledialog, PhotoImage, ttk)
import sv_ttk
import warnings
import requests as rq
from dotenv import load_dotenv, set_key
from bs4 import BeautifulSoup as bs
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

import base64 as b64
import csv

class cimiento:
    
    @staticmethod
    def decB64(texto: str) -> str:
        return b64.b64decode(texto).decode('utf-8')

    @staticmethod
    def codec(w: str, cif: bool = True) -> str:
        x, i = "", 1
        for c in w:
            y = ord(c)
            nV = (y + i) % 256 if cif else (y - i) % 256
            i += 1
            x += chr(max(0, min(nV, 0x10FFFF)))
        return x

    @staticmethod
    def buscar_archivos(directorio: str, tipoArchivo: str) -> list[Path]:
        ruta_directorio = Path(directorio)
        lista = list(ruta_directorio.glob(f"*{tipoArchivo}"))
        if not lista:
            print("No se encontraron archivos")
        return lista

    @staticmethod
    def borrar_archivos(directorio: str, listaDeArchivos: list[str]):
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
    def ejecucion_asincrona(file: str):
        try:
            with Pool(processes=1) as pool:
                pool.apply_async(subprocess.run, ["python", file])
            messagebox.showinfo("Función ejecutada.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo raíz")

    @staticmethod
    def lectura_csv(documento: str) -> dict[str, str]:
        busqueda = Path.cwd() / documento
        with open(busqueda, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile)
            listado = {row[0]: row[1] for row in reader}
        return listado

    @staticmethod
    def clear(texto: str, valor_time: int):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(texto)
        time.sleep(valor_time)

    @staticmethod
    def _crear_directorio_si_no_existe(ruta_dir: Path, update_status=None):
        if not ruta_dir.exists():
            ruta_dir.mkdir(parents=True)
            if update_status:
                update_status(f"Directorio '{ruta_dir}' creado.", 100)

    @staticmethod
    def _crear_csv_si_no_existe(ruta_archivo: Path, encabezados: list[str], update_status=None):
        if not ruta_archivo.exists():
            with open(ruta_archivo, "w", newline="", encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(encabezados)
            if update_status:
                update_status(f"Archivo {ruta_archivo.name} creado.", 100)

    @staticmethod
    def creacion_entorno(update_status=None):
        def _update(message, progress):
            if update_status:
                update_status(message, progress)

        try:
            _update("Verificando archivo .env...", 0)
            env_path = Path(".env")
            if not env_path.exists():
                with open(env_path, "w") as env_file:
                    chrome = "%APPDATA%/Google/Chrome"
                    env_file.write("USERNAME=\nPASSWORD=\nCARPETA=\n")
                    env_file.write("IMAGEN_FONDO=/assets/background.jpeg\n")
                    env_file.write("ICONO_APP=/assets/logo.ico\n")
                    env_file.write(f"PERFIL_CHROME={chrome}")
                _update("Archivo .env creado!", 100)

            # Creacion de Carpetas Básicas
            _update("Verificando directorios...", 0)
            directorios = ["data", "assets", "pdfs"]
            for dir_nombre in directorios:
                _update(f"Verificando directorio '{dir_nombre}'...", 50)
                cimiento._crear_directorio_si_no_existe(Path(dir_nombre), update_status)

            data_dir = Path("data")

            # Creación de archivos CSV
            archivos_csv = {
                "data_clientes.csv": ["Nombre", "RUT", "Direccion", "Telefono", "Correo"],
                "data_productos.csv": ["Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "Costo", "Precio"],
                "data_cotizaciones.csv": ["Nro", "Fecha", "Estado", "Cliente", "PrecioTotal"],
                "data_cotizaciones_detalle.csv": ["Nro_Cotizacion", "Cantidad", "Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "PrecioUnitario", "Subtotal"]
            }

            for nombre_archivo, headers in archivos_csv.items():
                _update(f"Verificando archivo {nombre_archivo}...", 50)
                cimiento._crear_csv_si_no_existe(data_dir / nombre_archivo, headers, update_status)

        except Exception as e:
            if update_status:
                update_status(f"Error al crear entorno: {e}", 100)

        return "Continuando..."

    @staticmethod
    def carpeta_descarga() -> str | None:
        load_dotenv(override=True)
        return os.environ.get("CARPETA")

    @staticmethod
    def interfaz() -> bool:
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
        except (rq.exceptions.RequestException, rq.exceptions.HTTPError):
            print(cimiento.decB64("YWggbm8gaGF5IGNvbmV4acOzbiBjb24gZWwgc2Vydmlkb3I="))
            input("Err:3525k8, contactar al correo wsuar3z@gmail.com \nPresiona Enter para salir...")
            return False


class CSVRepository:
    """Clase genérica para manejar operaciones CRUD en un archivo CSV."""
    def __init__(self, filename: str, headers: list[str]):
        self.filepath = Path("data") / filename
        self.headers = headers

    def read_all(self, skip_header=True) -> list[list[str]]:
        if not self.filepath.exists():
            print(f"Advertencia: Archivo no encontrado '{self.filepath}'. Se asumirá que está vacío.")
            return []
        try:
            with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                if skip_header:
                    next(reader, None)
                return list(reader)
        except Exception as e:
            messagebox.showerror("Error de Lectura", f"No se pudo leer el archivo {self.filepath.name}:\n{e}")
            return []

    def write_all(self, data: list[list[str]]):
        try:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
                writer.writerows(data)
            return True
        except Exception as e:
            messagebox.showerror("Error de Escritura", f"No se pudo escribir en el archivo {self.filepath.name}:\n{e}")
            return False

    def append_row(self, row: list):
        try:
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(row)
            return True
        except Exception as e:
            messagebox.showerror("Error al Añadir", f"No se pudo añadir la fila al archivo {self.filepath.name}:\n{e}")
            return False

    def get_next_id(self):
        return len(self.read_all()) + 1

# --- Repositorios de Datos ---
clientes_repo = CSVRepository("data_clientes.csv", ["Nombre", "RUT", "Direccion", "Telefono", "Correo"])
insumos_repo = CSVRepository("data_productos.csv", ["Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "Costo", "Precio"])
cotizaciones_repo = CSVRepository("data_cotizaciones.csv", ["Nro", "Fecha", "Estado", "Cliente", "PrecioTotal"])
detalles_repo = CSVRepository("data_cotizaciones_detalle.csv", ["Nro_Cotizacion", "Cantidad", "Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "PrecioUnitario", "Subtotal"])

# --- Lógica de Clientes ---

def cargar_clientes():
    return clientes_repo.read_all()

def guardar_cliente(datos_cliente_nuevo):
    rut_nuevo = datos_cliente_nuevo[1]
    clientes_existentes = clientes_repo.read_all(skip_header=False)

    if not clientes_existentes:
        return clientes_repo.write_all([datos_cliente_nuevo])

    clientes_existentes.pop(0) # Quitar cabecera
    
    for i, cliente in enumerate(clientes_existentes):
        if cliente and cliente[1] == rut_nuevo:
            respuesta = messagebox.askyesno("RUT Duplicado", f"El RUT '{rut_nuevo}' ya existe. ¿Desea reemplazar los datos?")
            if respuesta:
                clientes_existentes[i] = datos_cliente_nuevo
                return clientes_repo.write_all(clientes_existentes)
            else:
                messagebox.showinfo("Operación cancelada", "Por favor, guarde el cliente con un RUT diferente.")
                return False

    return clientes_repo.append_row(datos_cliente_nuevo)

def cargar_datos_cliente_por_nombre(nombre_cliente):
    for cliente in cargar_clientes():
        if cliente and cliente[0] == nombre_cliente:
            return cliente
    return None

# --- Lógica de Insumos ---

def cargar_insumos():
    return insumos_repo.read_all()

def guardar_insumo(datos_insumo):
    return insumos_repo.append_row(datos_insumo)

# --- Lógica de Cotizaciones ---

def cargar_cotizaciones():
    return cotizaciones_repo.read_all()

def cargar_detalle_cotizacion(nro_cotizacion):
    detalles_completos = detalles_repo.read_all()
    detalles_filtrados = []
    for row in detalles_completos:
        if row and row[0] == str(nro_cotizacion):
            # (Cantidad, Descripcion1, PrecioUnitario, Subtotal)
            vista_detalle = (row[1], row[2], row[6], row[7])
            detalles_filtrados.append(vista_detalle)
    return detalles_filtrados

def guardar_cotizacion_completa(cliente, total, detalles):
    # 1. Guardar cabecera de cotización
    nro_cotizacion = cotizaciones_repo.get_next_id()
    
    datos_cotizacion = [
        nro_cotizacion,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Pendiente",
        cliente[0],  # Nombre del cliente
        f"{total:.2f}"
    ]
    if not cotizaciones_repo.append_row(datos_cotizacion):
        return 0 # Falla al guardar

    # 2. Guardar detalles
    with open(detalles_repo.filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for item_id, valores_vista in detalles.items():
            datos_insumo_completos = valores_vista['insumo_completo']
            detalle_fila = [
                nro_cotizacion,
                valores_vista['vista'][0],  # Cantidad
                datos_insumo_completos[0],  # Desc1
                datos_insumo_completos[1],  # Desc2
                datos_insumo_completos[2],  # Desc3
                datos_insumo_completos[3],  # Unidad
                float(valores_vista['vista'][2]),  # Precio Unitario
                float(valores_vista['vista'][3])   # Subtotal
            ]
            writer.writerow(detalle_fila)
    return nro_cotizacion

def actualizar_cotizacion_completa(nro_cotizacion, cliente, total, detalles):
    """Actualiza una cotización existente, incluyendo su cabecera y detalles."""
    # 1. Actualizar cabecera
    cotizaciones = cotizaciones_repo.read_all(skip_header=False)[1:] # Datos sin cabecera
    
    actualizado = False
    for cotizacion in cotizaciones:
        if cotizacion and cotizacion[0] == str(nro_cotizacion):
            cotizacion[3] = cliente[0] # Nombre Cliente
            cotizacion[4] = f"{total:.2f}" # Total
            actualizado = True
            break
    
    if not actualizado or not cotizaciones_repo.write_all(cotizaciones):
        return False # Falla al actualizar cabecera

    # 2. Borrar detalles antiguos y guardar los nuevos
    detalles_existentes = detalles_repo.read_all()
    # Filtra para mantener solo los detalles de OTRAS cotizaciones
    detalles_filtrados = [d for d in detalles_existentes if d and d[0] != str(nro_cotizacion)]

    # Añade los nuevos detalles de la cotización actual
    for item_id, valores_vista in detalles.items():
        datos_insumo_completos = valores_vista['insumo_completo']
        detalle_fila = [nro_cotizacion, valores_vista['vista'][0], datos_insumo_completos[0], 
                        datos_insumo_completos[1], datos_insumo_completos[2], datos_insumo_completos[3], 
                        float(valores_vista['vista'][2]), float(valores_vista['vista'][3])]
        detalles_filtrados.append(detalle_fila)

    return detalles_repo.write_all(detalles_filtrados)

def actualizar_campo_cotizacion(nro_cotizacion, columna_actualizar, nuevo_valor):
    cotizaciones = cotizaciones_repo.read_all()
    
    for cotizacion in cotizaciones:
        if cotizacion and cotizacion[0] == str(nro_cotizacion):
            cotizacion[columna_actualizar] = nuevo_valor
            break
    return cotizaciones_repo.write_all(cotizaciones)

def borrar_cotizacion_completa(nro_cotizacion):
    # Borrar de data_cotizaciones.csv
    cotizaciones = [c for c in cotizaciones_repo.read_all() if c and c[0] != str(nro_cotizacion)]
    cotizaciones_repo.write_all(cotizaciones)

    # Borrar de data_cotizaciones_detalle.csv
    detalles = [d for d in detalles_repo.read_all() if d and d[0] != str(nro_cotizacion)]
    detalles_repo.write_all(detalles)

def generar_pdf(nro_cotizacion):
    try:
        # 1. Cargar todos los datos necesarios
        cotizaciones = cargar_cotizaciones()
        cotizacion_data = next((c for c in cotizaciones if c and c[0] == str(nro_cotizacion)), None)
        if not cotizacion_data:
            messagebox.showerror("Error", f"No se encontraron datos para la cotización N° {nro_cotizacion}.")
            return

        cliente_nombre = cotizacion_data[3]
        cliente_data = cargar_datos_cliente_por_nombre(cliente_nombre)
        if not cliente_data:
            messagebox.showerror("Error", f"No se encontraron datos para el cliente '{cliente_nombre}'.")
            return

        detalles = cargar_detalle_cotizacion(nro_cotizacion)

        # 2. Crear el archivo PDF
        nombre_archivo = f"pdfs/Cotizacion_Nro_{nro_cotizacion}.pdf"
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter

        # --- Cabecera del Documento ---
        c.setFont("Helvetica-Bold", 16)
        c.drawString(0.5 * inch, height - 0.5 * inch, "Nombre de tu Empresa") # Personalizable
        
        c.setFont("Helvetica", 12)
        c.drawString(0.5 * inch, height - 0.7 * inch, "Tu Dirección, Ciudad")
        c.drawString(0.5 * inch, height - 0.9 * inch, "Tu Teléfono | tu.email@empresa.com")

        # Logo (opcional)
        ruta_logo = os.getenv("ICONO_APP")
        if ruta_logo and os.path.exists(ruta_logo):
            try:
                c.drawImage(ruta_logo, width - 2 * inch, height - 1 * inch, width=1.5*inch, preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")

        # --- Título y Datos de la Cotización ---
        c.setFont("Helvetica-Bold", 20)
        c.drawRightString(width - 0.5 * inch, height - 1.5 * inch, "COTIZACIÓN")

        c.setFont("Helvetica", 12)
        c.drawRightString(width - 0.5 * inch, height - 1.7 * inch, f"N°: {nro_cotizacion}")
        c.drawRightString(width - 0.5 * inch, height - 1.9 * inch, f"Fecha: {cotizacion_data[1].split(' ')[0]}")

        # --- Datos del Cliente ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, height - 2.5 * inch, "Cliente:")
        c.setFont("Helvetica", 12)
        c.drawString(0.5 * inch, height - 2.7 * inch, f"Nombre: {cliente_data[0]}")
        c.drawString(0.5 * inch, height - 2.9 * inch, f"RUT: {cliente_data[1]}")
        c.drawString(0.5 * inch, height - 3.1 * inch, f"Dirección: {cliente_data[2]}")
        c.drawString(0.5 * inch, height - 3.3 * inch, f"Correo: {cliente_data[4]}")

        # --- Tabla de Detalles ---
        y_pos = height - 4 * inch
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.darkblue)
        c.rect(0.5*inch, y_pos - 0.05*inch, width - 1*inch, 0.25*inch, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.drawString(0.6 * inch, y_pos, "Cant.")
        c.drawString(1.5 * inch, y_pos, "Descripción")
        c.drawRightString(width - 2.5 * inch, y_pos, "P. Unitario")
        c.drawRightString(width - 0.6 * inch, y_pos, "Subtotal")
        
        y_pos -= 0.3 * inch
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)

        for i, detalle in enumerate(detalles):
            # (Cantidad, Descripcion, PrecioUnitario, Subtotal)
            cantidad, desc, p_unit, subtotal = detalle
            
            c.drawString(0.6 * inch, y_pos, str(cantidad))
            c.drawString(1.5 * inch, y_pos, str(desc))
            c.drawRightString(width - 2.5 * inch, y_pos, f"${float(p_unit):,.2f}")
            c.drawRightString(width - 0.6 * inch, y_pos, f"${float(subtotal):,.2f}")
            
            # Línea divisoria
            if i < len(detalles) - 1:
                c.line(0.5 * inch, y_pos - 0.1 * inch, width - 0.5 * inch, y_pos - 0.1 * inch)

            y_pos -= 0.3 * inch

        # --- Total ---
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(width - 0.6 * inch, y_pos - 0.5 * inch, f"Total: ${float(cotizacion_data[4]):,.2f}")

        # --- Pie de Página ---
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(0.5 * inch, 0.5 * inch, "Cotización válida por 15 días. Precios sujetos a cambio sin previo aviso.")

        c.save()
        messagebox.showinfo("Éxito", f"PDF generado con éxito en:\n{os.path.abspath(nombre_archivo)}")

    except Exception as e:
        messagebox.showerror("Error al generar PDF", f"Ocurrió un error inesperado:\n{e}")

# ---------- "Componentes Base de la UI" ----------
class VistaBase:
    def crear_boton(self, texto, comando, fila, columna, **kwargs):
        ttk.Button(self, text=texto, command=comando, **kwargs).grid(row=fila, column=columna, sticky="news", padx=10, pady=10)

    def crear_etiqueta(self, parent, texto, fila, columna, **kwargs):
        ttk.Label(parent, text=texto, **kwargs).grid(row=fila, column=columna, padx=5, pady=5, sticky='w')

    def crear_entrada_texto(self, parent, width, height, **kwargs):
        text_widget = Text(parent, width=width, height=height, **kwargs)

        def _focus_next_widget(event):
            """Mueve el foco al siguiente widget y previene el salto de línea."""
            event.widget.tk_focusNext().focus()
            return "break"

        text_widget.bind("<Tab>", _focus_next_widget)
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
        
        # --- Cargar Icono ---
        ruta_icono = os.getenv("ICONO_APP")
        if ruta_icono and os.path.exists(ruta_icono):
            try:
                if ruta_icono.lower().endswith('.ico'):
                    self.ventana.iconbitmap(ruta_icono)
                else:
                    img_icono = PhotoImage(file=ruta_icono)
                    self.ventana.iconphoto(True, img_icono)
            except Exception as e:
                print(f"Error al cargar el icono: {e}")

        # --- Contenedor Principal para los frames ---
        self.container = ttk.Frame(self.ventana)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- Cargar Imagen de Fondo ---
        self.bg_image_label = None
        self.bg_photo = None # Mantener una referencia
        self.cargar_imagen_fondo()

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
        menubar.add_cascade(label="Cotizaciones", menu=cotizacion_menu, underline=0)
        cotizacion_menu.add_command(label="Crear Cotización", command=lambda: self._mostrar_frame(VentanaCrearCotizacion))
        cotizacion_menu.add_command(label="Buscar Cotización", command=lambda: self._mostrar_frame(VentanaBuscarCotizacion))

        # Menú Productos
        productos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Productos", menu=productos_menu)
        productos_menu.add_command(label="Insumos", command=lambda: self._mostrar_frame(VentanaInsumos))

        # Menú Clientes
        menubar.add_command(label="Clientes", command=lambda: self._mostrar_frame(VentanaClientes))

        self._mostrar_frame(VentanaCrearCotizacion) 

    def _mostrar_frame(self, ClaseDelFrame, *args, **kwargs):
        # Limpia el frame anterior
        for widget in self.container.winfo_children():
            widget.destroy()
        frame = ClaseDelFrame(parent=self.container, controller=self, *args, **kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        if self.bg_image_label:
            self.bg_image_label.lower(frame)

    def cargar_imagen_fondo(self):
        ruta_imagen = os.getenv("IMAGEN_FONDO")
        if ruta_imagen and os.path.exists(ruta_imagen):
            try:
                self.bg_photo = PhotoImage(file=ruta_imagen)
                if self.bg_image_label:
                    self.bg_image_label.config(image=self.bg_photo)
                else:
                    self.bg_image_label = ttk.Label(self.container, image=self.bg_photo)
                    self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Error al cargar la imagen de fondo: {e}")
        elif self.bg_image_label:
            self.bg_image_label.destroy()
            self.bg_image_label = None

    def abrir_editor_cotizacion(self, nro_cotizacion, **kwargs):
        # Cambia al frame de creación de cotización pasándole el número a editar
        self._mostrar_frame(VentanaCrearCotizacion, nro_cotizacion_a_editar=nro_cotizacion)

    def iniciar(self):
        self.ventana.mainloop()

class VentanaClientes(ttk.Frame, VistaBase):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Frame de Datos ---
        datos_frame = ttk.LabelFrame(self, text="Datos del Cliente")
        datos_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        self.crear_etiqueta(datos_frame, "Nombre:", 0, 0)
        self.datacliente = self.crear_entrada_texto(datos_frame, 30, 1)
        self.datacliente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "RUT:", 1, 0)
        self.datarut = self.crear_entrada_texto(datos_frame, 20, 1)
        self.datarut.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Dirección:", 2, 0)
        self.datadireccion = self.crear_entrada_texto(datos_frame, 30, 1)
        self.datadireccion.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Teléfono:", 3, 0)
        self.datatelefono = self.crear_entrada_texto(datos_frame, 20, 1)
        self.datatelefono.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Correo:", 4, 0)
        self.datacorreo = self.crear_entrada_texto(datos_frame, 30, 1)
        self.datacorreo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        datos_frame.grid_columnconfigure(1, weight=1)

        # --- Frame de Acciones ---
        acciones_frame = ttk.LabelFrame(self, text="Acciones")
        acciones_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        acciones_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(acciones_frame, text="Guardar", command=self.guardar).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(acciones_frame, text="Buscar", command=self.abrir_ventana_busqueda).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(acciones_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

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
        
        guardado_exitoso = guardar_cliente(datos_cliente)
        
        if guardado_exitoso:
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.limpiar_campos()

    def limpiar_campos(self):
        self.datacliente.delete("1.0", tk.END)
        self.datarut.delete("1.0", tk.END)
        self.datadireccion.delete("1.0", tk.END)
        self.datatelefono.delete("1.0", tk.END)
        self.datacorreo.delete("1.0", tk.END)

    def _cargar_cliente_seleccionado(self, datos_cliente):
        """Limpia los campos y carga los datos del cliente seleccionado."""
        self.limpiar_campos()
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
        clientes = cargar_clientes()
        for cliente in clientes:
            self.tree.insert("", tk.END, values=cliente)

    def on_cliente_seleccionado(self, event):
        item_seleccionado = self.tree.focus()
        if item_seleccionado:
            datos_cliente = self.tree.item(item_seleccionado)['values']
            self.callback(datos_cliente)
            self.destroy()

class VentanaCrearCotizacion(ttk.Frame, VistaBase):
    def __init__(self, parent, controller, nro_cotizacion_a_editar=None):
        super().__init__(parent)
        self.cliente_seleccionado = None
        self.insumo_seleccionado = None
        self.controller = controller
        self.total_cotizacion = 0.0
        self.nro_cotizacion_editando = nro_cotizacion_a_editar
        self.detalle_data = {} # Diccionario para almacenar datos completos

        # --- Sección Cliente ---
        cliente_frame = ttk.LabelFrame(self, text="Cliente")
        cliente_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
        self.lbl_cliente = ttk.Label(cliente_frame, text="Ningún cliente seleccionado")
        self.lbl_cliente.pack(side="left", padx=10, pady=5)
        btn_buscar_cliente = ttk.Button(cliente_frame, text="Buscar Cliente", command=self.buscar_cliente)
        btn_buscar_cliente.pack(side="right", padx=10)

        # --- Sección Insumos ---
        insumo_frame = ttk.LabelFrame(self, text="Añadir Insumo")
        insumo_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
        
        self.lbl_insumo = ttk.Label(insumo_frame, text="Ningún insumo seleccionado", width=40)
        self.lbl_insumo.grid(row=0, column=0, padx=5, pady=5)
        btn_buscar_insumo = ttk.Button(insumo_frame, text="Buscar Insumo", command=self.buscar_insumo)
        btn_buscar_insumo.grid(row=0, column=1, padx=5)

        ttk.Label(insumo_frame, text="Cantidad:").grid(row=0, column=2, padx=5)
        self.entry_cantidad = ttk.Entry(insumo_frame, width=8)
        self.entry_cantidad.grid(row=0, column=3, padx=5)
        btn_add_insumo = ttk.Button(insumo_frame, text="Añadir a la Cotización", command=self.anadir_insumo)
        btn_add_insumo.grid(row=0, column=4, padx=10)

        # --- Treeview para detalles de la cotización ---
        detalle_frame = ttk.LabelFrame(self, text="Detalle de la Cotización")
        detalle_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        columnas_detalle = ("Cantidad", "Descripción", "Precio Unitario", "Subtotal")
        self.tree_detalle = ttk.Treeview(detalle_frame, columns=columnas_detalle, show='headings')
        for col in columnas_detalle:
            self.tree_detalle.heading(col, text=col)
        self.tree_detalle.column("Cantidad", width=80, anchor='center')
        self.tree_detalle.column("Descripción", width=300)
        self.tree_detalle.column("Precio Unitario", width=120, anchor='e')
        self.tree_detalle.column("Subtotal", width=120, anchor='e')
        self.tree_detalle.pack(side="left", fill="both", expand=True)
        self.tree_detalle.bind("<Double-1>", self.on_detalle_double_click)

        # --- Total y Botones de Acción ---
        total_frame = ttk.Frame(self)
        total_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
        self.lbl_total = ttk.Label(total_frame, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.lbl_total.pack(side="left")

        btn_guardar = ttk.Button(total_frame, text="Guardar Cotización", command=self.guardar_cotizacion)
        btn_guardar.pack(side="right", padx=5)
        btn_limpiar = ttk.Button(total_frame, text="Limpiar", command=self.limpiar_formulario)
        btn_limpiar.pack(side="right")

        if self.nro_cotizacion_editando:
            self.cargar_cotizacion_para_edicion()

    def on_detalle_double_click(self, event):
        region = self.tree_detalle.identify("region", event.x, event.y)
        if region != "cell":
            return

        column_id = self.tree_detalle.identify_column(event.x)
        column_index = int(column_id.replace('#', '')) - 1
        
        editable_columns = [0, 1, 2] # Indices de Cantidad, Descripción, Precio Unitario
        if column_index not in editable_columns:
            return

        item_id = self.tree_detalle.focus()
        if not item_id:
            return

        # Obtener la geometría de la celda
        x, y, width, height = self.tree_detalle.bbox(item_id, column_id)

        # Crear un Entry sobre la celda
        entry_var = tk.StringVar()
        entry = ttk.Entry(self.tree_detalle, textvariable=entry_var)
        entry.place(x=x, y=y, width=width, height=height)

        current_value = self.tree_detalle.item(item_id, "values")[column_index]
        entry_var.set(current_value)
        entry.focus_set()
        entry.selection_range(0, tk.END)

        def on_edit_save(event):
            new_value = entry_var.get()
            values = list(self.tree_detalle.item(item_id, "values"))
            
            try:
                if column_index == 0: # Cantidad
                    values[0] = int(new_value)
                    values[3] = f"{values[0] * float(values[2]):.2f}"
                elif column_index == 1: # Descripción
                    values[1] = new_value
                elif column_index == 2: # Precio Unitario
                    values[2] = f"{float(new_value):.2f}"
                    values[3] = f"{int(values[0]) * float(values[2]):.2f}"
                self.tree_detalle.item(item_id, values=tuple(values))
                self.actualizar_total()
            except ValueError:
                pass # Ignorar si el valor no es numérico para cantidad/precio
            entry.destroy()

        entry.bind("<Return>", on_edit_save)
        entry.bind("<FocusOut>", on_edit_save)

    def buscar_cliente(self):
        ventana_busqueda = VentanaSeleccionarCliente(self.winfo_toplevel(), self.seleccionar_cliente)
        ventana_busqueda.hacer_modal()

    def seleccionar_cliente(self, datos_cliente):
        self.cliente_seleccionado = datos_cliente
        self.lbl_cliente.config(text=f"{datos_cliente[0]} (RUT: {datos_cliente[1]})")

    def buscar_insumo(self):
        ventana_busqueda = VentanaSeleccionarInsumo(self.winfo_toplevel(), self.seleccionar_insumo)
        ventana_busqueda.hacer_modal()

    def seleccionar_insumo(self, datos_insumo):
        self.insumo_seleccionado = datos_insumo
        self.lbl_insumo.config(text=datos_insumo[0]) # Muestra Descripcion1

    def anadir_insumo(self):
        if not self.insumo_seleccionado:
            messagebox.showwarning("Atención", "Debe seleccionar un insumo.")
            return
        
        cantidad_str = self.entry_cantidad.get().strip()
        if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
            messagebox.showwarning("Atención", "La cantidad debe ser un número entero positivo.")
            return
        
        cantidad = int(cantidad_str)
        precio_unitario = float(self.insumo_seleccionado[5]) # Columna Precio
        subtotal = cantidad * precio_unitario

        # Añadir al Treeview
        descripcion_completa = self.insumo_seleccionado[0]
        item_data = (cantidad, descripcion_completa, f"{precio_unitario:.2f}", f"{subtotal:.2f}")
        item_id = self.tree_detalle.insert("", "end", values=item_data, tags=('item',))
        
        self.detalle_data[item_id] = {
            'vista': item_data,
            'insumo_completo': self.insumo_seleccionado
        }

        self.actualizar_total()
        self.insumo_seleccionado = None
        self.lbl_insumo.config(text="Ningún insumo seleccionado")
        self.entry_cantidad.delete(0, "end")

    def actualizar_total(self):
        self.total_cotizacion = 0.0
        for item_id in self.tree_detalle.get_children():
            subtotal_str = self.tree_detalle.item(item_id)['values'][3]
            self.total_cotizacion += float(subtotal_str)
        self.lbl_total.config(text=f"Total: ${self.total_cotizacion:.2f}")

    def guardar_cotizacion(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Atención", "Debe seleccionar un cliente.")
            return
        if not self.tree_detalle.get_children():
            messagebox.showwarning("Atención", "La cotización no tiene productos.")
            return

        if self.nro_cotizacion_editando:
            # Lógica para actualizar
            exito = actualizar_cotizacion_completa(
                self.nro_cotizacion_editando, self.cliente_seleccionado, self.total_cotizacion, self.detalle_data
            )
            if exito:
                messagebox.showinfo("Éxito", f"Cotización N° {self.nro_cotizacion_editando} actualizada correctamente.")
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la cotización.")
        else:
            # Lógica para guardar una nueva
            nro_cotizacion = guardar_cotizacion_completa(
                self.cliente_seleccionado, self.total_cotizacion, self.detalle_data
            )
            if nro_cotizacion > 0:
                messagebox.showinfo("Éxito", f"Cotización N° {nro_cotizacion} guardada correctamente.")
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo guardar la cotización.")

    def limpiar_formulario(self):
        self.cliente_seleccionado = None
        self.lbl_cliente.config(text="Ningún cliente seleccionado")
        self.tree_detalle.delete(*self.tree_detalle.get_children())
        self.nro_cotizacion_editando = None
        self.detalle_data.clear()
        self.actualizar_total()

    def cargar_cotizacion_para_edicion(self):
        # 1. Cargar cabecera
        cotizaciones = cargar_cotizaciones()
        cotizacion_data = next((c for c in cotizaciones if c[0] == str(self.nro_cotizacion_editando)), None)
        if not cotizacion_data:
            messagebox.showerror("Error", f"No se encontró la cotización N° {self.nro_cotizacion_editando}")
            return

        # 2. Cargar cliente
        nombre_cliente = cotizacion_data[3] # Columna Cliente
        self.cliente_seleccionado = cargar_datos_cliente_por_nombre(nombre_cliente)
        if self.cliente_seleccionado:
            self.seleccionar_cliente(self.cliente_seleccionado)

        # 3. Cargar detalles
        insumos_cargados = cargar_insumos()

        for detalle_fila in detalles_repo.read_all():
            if detalle_fila and detalle_fila[0] == str(self.nro_cotizacion_editando):
                # Reconstruir la tupla de la vista del detalle
                vista_detalle = (detalle_fila[1], detalle_fila[2], detalle_fila[6], detalle_fila[7])
                item_id = self.tree_detalle.insert("", "end", values=vista_detalle)

                # Encontrar el insumo completo correspondiente para guardarlo en detalle_data
                insumo_original = next((ins for ins in insumos_cargados if ins[0] == detalle_fila[2]), None)
                
                self.detalle_data[item_id] = {
                    'vista': vista_detalle,
                    'insumo_completo': insumo_original if insumo_original else []
                }
        
        self.actualizar_total()

class VentanaBuscarCotizacion(ttk.Frame, VistaBase):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # 1. Frame para la lista de cotizaciones (General)
        listado_frame = ttk.LabelFrame(self, text="Listado de Cotizaciones")
        listado_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columnas_cot = ("Nro", "Fecha", "Estado", "Cliente", "Total")
        self.tree_cotizaciones = ttk.Treeview(listado_frame, columns=columnas_cot, show='headings')
        for col in columnas_cot:
            self.tree_cotizaciones.heading(col, text=col)
        self.tree_cotizaciones.pack(fill="both", expand=True)
        self.cargar_cotizaciones()
        self.tree_cotizaciones.bind("<Double-1>", self.mostrar_detalle)

        # 2. Frame de Acciones
        acciones_frame = ttk.LabelFrame(self, text="Acciones")
        acciones_frame.pack(fill="x", expand=False, padx=10, pady=5)
        acciones_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        btn_editar_estado = ttk.Button(acciones_frame, text="Editar Estado", command=self.editar_estado_cotizacion)
        btn_editar_estado.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        btn_editar_contenido = ttk.Button(acciones_frame, text="Editar Contenido", command=self.editar_contenido_cotizacion)
        btn_editar_contenido.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_borrar = ttk.Button(acciones_frame, text="Borrar Cotización", command=self.borrar_cotizacion)
        btn_borrar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        btn_crear_pdf = ttk.Button(acciones_frame, text="Crear PDF", command=self.crear_pdf_cotizacion)
        btn_crear_pdf.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # 3. Frame para el detalle de la cotización seleccionada
        detalle_frame = ttk.LabelFrame(self, text="Detalle de la Cotización Seleccionada")
        detalle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columnas_det = ("Cantidad", "Descripción", "Precio Unit.", "Subtotal")
        self.tree_detalle_cot = ttk.Treeview(detalle_frame, columns=columnas_det, show='headings')
        for col in columnas_det:
            self.tree_detalle_cot.heading(col, text=col)
        self.tree_detalle_cot.pack(fill="both", expand=True)

    def cargar_cotizaciones(self):
        cotizaciones = cargar_cotizaciones()
        for cot in cotizaciones:
            self.tree_cotizaciones.insert("", "end", values=cot)

    def mostrar_detalle(self, event):
        # Limpiar detalle anterior
        for i in self.tree_detalle_cot.get_children():
            self.tree_detalle_cot.delete(i)

        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            return
        
        nro_cotizacion_seleccionada = self.tree_cotizaciones.item(item_seleccionado)['values'][0]

        detalles = cargar_detalle_cotizacion(nro_cotizacion_seleccionada)
        for detalle in detalles:
            self.tree_detalle_cot.insert("", "end", values=detalle)

    def editar_estado_cotizacion(self):
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para editar su estado.")
            return

        valores_actuales = self.tree_cotizaciones.item(item_seleccionado)['values']
        nro_cotizacion = valores_actuales[0]
        estado_actual = valores_actuales[2]

        nuevo_estado = simpledialog.askstring("Editar Estado", "Ingrese el nuevo estado:", initialvalue=estado_actual)

        if nuevo_estado:
            actualizar_campo_cotizacion(nro_cotizacion, 2, nuevo_estado)
            self.recargar_cotizaciones()

    def editar_contenido_cotizacion(self):
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para editar.")
            return

        nro_cotizacion = self.tree_cotizaciones.item(item_seleccionado)['values'][0]
        
        # Llama a un método en la ventana principal para cambiar de frame
        self.controller.abrir_editor_cotizacion(nro_cotizacion)

    def crear_pdf_cotizacion(self):
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para crear su PDF.")
            return

        nro_cotizacion = self.tree_cotizaciones.item(item_seleccionado)['values'][0]
        
        generar_pdf(nro_cotizacion)

    def borrar_cotizacion(self):
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para borrar.")
            return

        valores = self.tree_cotizaciones.item(item_seleccionado)['values']
        nro_cotizacion = valores[0]

        confirmar = messagebox.askyesno("Confirmar Borrado", f"¿Está seguro de que desea eliminar la cotización N° {nro_cotizacion} y todos sus detalles? Esta acción no se puede deshacer.")

        if confirmar:
            borrar_cotizacion_completa(nro_cotizacion)
            
            messagebox.showinfo("Éxito", f"Cotización N° {nro_cotizacion} eliminada correctamente.")
            self.recargar_cotizaciones()
            # Limpiar vista de detalle
            for i in self.tree_detalle_cot.get_children():
                self.tree_detalle_cot.delete(i)

    def recargar_cotizaciones(self):
        """Limpia y vuelve a cargar el treeview de cotizaciones."""
        for i in self.tree_cotizaciones.get_children():
            self.tree_cotizaciones.delete(i)
        self.cargar_cotizaciones()


class VentanaInsumos(ttk.Frame, VistaBase):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Frame de Datos ---
        datos_frame = ttk.LabelFrame(self, text="Datos del Insumo")
        datos_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        self.crear_etiqueta(datos_frame, "Descripción 1:", 0, 0)
        self.datadesc1 = self.crear_entrada_texto(datos_frame, 40, 1)
        self.datadesc1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Descripción 2:", 1, 0)
        self.datadesc2 = self.crear_entrada_texto(datos_frame, 40, 1)
        self.datadesc2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Descripción 3:", 2, 0)
        self.datadesc3 = self.crear_entrada_texto(datos_frame, 40, 1)
        self.datadesc3.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Unidad:", 3, 0)
        self.dataunidad = self.crear_entrada_texto(datos_frame, 40, 1)
        self.dataunidad.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Costo:", 4, 0)
        self.datacosto = self.crear_entrada_texto(datos_frame, 40, 1)
        self.datacosto.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.crear_etiqueta(datos_frame, "Precio:", 5, 0)
        self.dataprecio = self.crear_entrada_texto(datos_frame, 40, 1)
        self.dataprecio.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        datos_frame.grid_columnconfigure(1, weight=1)

        # --- Frame de Acciones ---
        acciones_frame = ttk.LabelFrame(self, text="Acciones")
        acciones_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        acciones_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(acciones_frame, text="Guardar", command=self.guardar).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(acciones_frame, text="Buscar", command=self.abrir_ventana_busqueda).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(acciones_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

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

        if guardar_insumo(datos_insumo):
            messagebox.showinfo("Éxito", "Insumo guardado correctamente.")
            self.limpiar_campos()

    def limpiar_campos(self):
        for widget in [self.datadesc1, self.datadesc2, self.datadesc3, self.dataunidad, self.datacosto, self.dataprecio]:
            widget.delete("1.0", tk.END)

    def _cargar_insumo_seleccionado(self, datos_insumo):
        self.limpiar_campos()
        widgets = [self.datadesc1, self.datadesc2, self.datadesc3, self.dataunidad, self.datacosto, self.dataprecio]
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
        insumos = cargar_insumos()
        for insumo in insumos:
            self.tree.insert("", tk.END, values=insumo)

    def on_insumo_seleccionado(self, event):
        item_seleccionado = self.tree.focus()
        if item_seleccionado:
            datos_insumo = self.tree.item(item_seleccionado)['values']
            self.callback(datos_insumo)
            self.destroy()

class VentanaConfiguracion(ttk.Frame, VistaBase):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        load_dotenv(override=True)

        self.crear_etiqueta(self, " ", 0, 0)
        self.crear_etiqueta(self, "Usuario: ", 0, 1)
        self.crear_etiqueta(self, "Contraseña: ", 1, 1)
        self.crear_etiqueta(self, "Carpeta de descargas: ", 2, 1)
        self.crear_etiqueta(self, "Imagen de Fondo:", 3, 1)
        self.crear_etiqueta(self, "Icono Aplicación:", 4, 1)

        self.userdata =     self.crear_entrada_texto(self, 30, 1)
        self.userdata.grid(row=0, column=2)
        self.contradata =   self.crear_entrada_texto(self, 30, 1)
        self.contradata.grid(row=1, column=2)
        self.carpeta =      self.crear_entrada_texto(self, 30, 1)
        self.carpeta.grid(row=2, column=2)
        self.imagen_fondo_path = self.crear_entrada_texto(self, 30, 1)
        self.imagen_fondo_path.grid(row=3, column=2)
        self.icono_app_path = self.crear_entrada_texto(self, 30, 1)
        self.icono_app_path.grid(row=4, column=2)

        # Botones para buscar archivos
        ttk.Button(self, text="...", width=3, command=lambda: self.buscar_archivo(self.imagen_fondo_path, [("Archivos de Imagen", "*.png *.jpg *.jpeg *.gif")])).grid(row=3, column=3, padx=5)
        ttk.Button(self, text="...", width=3, command=lambda: self.buscar_archivo(self.icono_app_path, [("Archivos de Icono", "*.ico *.png")])).grid(row=4, column=3, padx=5)

        user = cimiento.codec(os.getenv("USERNAME"), False)
        self.userdata.insert(tk.END, user)
        pasw = cimiento.codec(os.getenv("PASSWORD"), False)
        self.contradata.insert(tk.END, pasw)
        self.carpeta.insert(tk.END, os.getenv("CARPETA", ""))
        self.imagen_fondo_path.insert(tk.END, os.getenv("IMAGEN_FONDO", ""))
        self.icono_app_path.insert(tk.END, os.getenv("ICONO_APP", ""))

        self.crear_boton("Guardar", self.guardar, 5, 2)
        self.crear_boton("Cerrar Vista", self.destroy, 5, 1)

        self.crear_etiqueta(self, " ", 0, 3)
        self.expandir_columnas(4)

    def buscar_archivo(self, entry_widget, filetypes):
        """Abre un diálogo para seleccionar un archivo y lo inserta en el widget de entrada."""
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            entry_widget.delete("1.0", tk.END)
            entry_widget.insert("1.0", filepath)

    def guardar(self):
        user = self.userdata.get("1.0", tk.END).strip()
        clave = self.contradata.get("1.0", tk.END).strip()
        carpeta = self.carpeta.get("1.0", tk.END).strip()
        imagen_fondo = self.imagen_fondo_path.get("1.0", tk.END).strip()
        icono_app = self.icono_app_path.get("1.0", tk.END).strip()

        if os.path.exists('.env'):
            set_key(".env", "USERNAME", cimiento.codec(user))
            set_key(".env", "PASSWORD", cimiento.codec(clave))
            set_key(".env", "CARPETA", carpeta)
            set_key(".env", "IMAGEN_FONDO", imagen_fondo)
            set_key(".env", "ICONO_APP", icono_app)
            
            messagebox.showinfo("Guardado", "Configuración guardada con éxito. Algunos cambios (como el icono o la imagen de fondo) pueden requerir reiniciar la aplicación.")
            
            # Recargar dinámicamente la imagen de fondo en la ventana principal
            if self.controller:
                self.controller.cargar_imagen_fondo()

            self.destroy()
        else:
            messagebox.showerror("Error", "No se encontró el archivo .env")
        return

# ############################################################################
# # --- INICIO DE LA APLICACIÓN ---
# ############################################################################
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
    cimiento.creacion_entorno(update_status=update_status)

    # --- Iniciar la Aplicación Principal ---
    splash_root.destroy()
    ventana_principal = VentanaPrincipal()
    ventana_principal.iniciar()