# ---------- "Preparacion del entorno Normal" ----------

import os
import csv
from datetime import datetime
from dotenv import load_dotenv, set_key

import tkinter as tk
import sv_ttk
from tkinter import Tk, Text
from tkinter import ttk, filedialog, PhotoImage
from tkinter import messagebox

# Importar desde archivos
from funciones_base import cimiento
import funciones_datos as datos

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
        
        guardado_exitoso = datos.guardar_cliente(datos_cliente)
        
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
        clientes = datos.cargar_clientes()
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
            exito = datos.actualizar_cotizacion_completa(
                self.nro_cotizacion_editando, self.cliente_seleccionado, self.total_cotizacion, self.detalle_data
            )
            if exito:
                messagebox.showinfo("Éxito", f"Cotización N° {self.nro_cotizacion_editando} actualizada correctamente.")
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la cotización.")
        else:
            # Lógica para guardar una nueva
            nro_cotizacion = datos.guardar_cotizacion_completa(
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
        cotizaciones = datos.cargar_cotizaciones()
        cotizacion_data = next((c for c in cotizaciones if c[0] == str(self.nro_cotizacion_editando)), None)
        if not cotizacion_data:
            messagebox.showerror("Error", f"No se encontró la cotización N° {self.nro_cotizacion_editando}")
            return

        # 2. Cargar cliente
        nombre_cliente = cotizacion_data[3]
        self.cliente_seleccionado = datos.cargar_datos_cliente_por_nombre(nombre_cliente)
        if self.cliente_seleccionado:
            self.seleccionar_cliente(self.cliente_seleccionado)

        # 3. Cargar detalles
        detalles_completos = datos.leer_csv("data_cotizaciones_detalle.csv")
        insumos_cargados = datos.cargar_insumos()

        for detalle_fila in detalles_completos:
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
        acciones_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        btn_editar_estado = ttk.Button(acciones_frame, text="Editar Estado", command=self.editar_estado_cotizacion)
        btn_editar_estado.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        btn_editar_contenido = ttk.Button(acciones_frame, text="Editar Contenido", command=self.editar_contenido_cotizacion)
        btn_editar_contenido.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_borrar = ttk.Button(acciones_frame, text="Borrar Cotización", command=self.borrar_cotizacion)
        btn_borrar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # 3. Frame para el detalle de la cotización seleccionada
        detalle_frame = ttk.LabelFrame(self, text="Detalle de la Cotización Seleccionada")
        detalle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columnas_det = ("Cantidad", "Descripción", "Precio Unit.", "Subtotal")
        self.tree_detalle_cot = ttk.Treeview(detalle_frame, columns=columnas_det, show='headings')
        for col in columnas_det:
            self.tree_detalle_cot.heading(col, text=col)
        self.tree_detalle_cot.pack(fill="both", expand=True)

    def cargar_cotizaciones(self):
        cotizaciones = datos.cargar_cotizaciones()
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

        detalles = datos.cargar_detalle_cotizacion(nro_cotizacion_seleccionada)
        for detalle in detalles:
            self.tree_detalle_cot.insert("", "end", values=detalle)

    def editar_estado_cotizacion(self):
        from tkinter import simpledialog
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para editar su estado.")
            return

        valores_actuales = self.tree_cotizaciones.item(item_seleccionado)['values']
        nro_cotizacion = valores_actuales[0]
        estado_actual = valores_actuales[2]

        nuevo_estado = simpledialog.askstring("Editar Estado", "Ingrese el nuevo estado:", initialvalue=estado_actual)

        if nuevo_estado:
            datos.actualizar_campo_cotizacion(nro_cotizacion, 2, nuevo_estado)
            self.recargar_cotizaciones()

    def editar_contenido_cotizacion(self):
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para editar.")
            return

        nro_cotizacion = self.tree_cotizaciones.item(item_seleccionado)['values'][0]
        
        # Llama a un método en la ventana principal para cambiar de frame
        self.controller.abrir_editor_cotizacion(nro_cotizacion)

    def borrar_cotizacion(self):
        item_seleccionado = self.tree_cotizaciones.focus()
        if not item_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una cotización para borrar.")
            return

        valores = self.tree_cotizaciones.item(item_seleccionado)['values']
        nro_cotizacion = valores[0]

        confirmar = messagebox.askyesno("Confirmar Borrado", f"¿Está seguro de que desea eliminar la cotización N° {nro_cotizacion} y todos sus detalles? Esta acción no se puede deshacer.")

        if confirmar:
            datos.borrar_cotizacion_completa(nro_cotizacion)
            
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

        if datos.guardar_insumo(datos_insumo):
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
        insumos = datos.cargar_insumos()
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