import os, csv
from tkinter import messagebox
from datetime import datetime

# --- Funciones Genéricas de CSV ---

def leer_csv(nombre_archivo, omitir_cabecera=True):
    """Lee todas las filas de un archivo CSV y las devuelve como una lista."""
    ruta_archivo = os.path.join("data", nombre_archivo)
    datos = []
    try:
        with open(ruta_archivo, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            if omitir_cabecera:
                next(reader, None)  # Omitir cabecera de forma segura
            datos = list(reader)
    except FileNotFoundError:
        print(f"Advertencia: Archivo no encontrado '{ruta_archivo}'. Se asumirá que está vacío.")
    except Exception as e:
        messagebox.showerror("Error de Lectura", f"No se pudo leer el archivo {nombre_archivo}:\n{e}")
    return datos

def escribir_csv(nombre_archivo, datos, cabecera):
    """Escribe una lista de datos en un archivo CSV, sobrescribiendo el contenido."""
    ruta_archivo = os.path.join("data", nombre_archivo)
    try:
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cabecera)
            writer.writerows(datos)
        return True
    except Exception as e:
        messagebox.showerror("Error de Escritura", f"No se pudo escribir en el archivo {nombre_archivo}:\n{e}")
        return False

def anadir_fila_csv(nombre_archivo, fila):
    """Añade una única fila al final de un archivo CSV."""
    ruta_archivo = os.path.join("data", nombre_archivo)
    try:
        with open(ruta_archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(fila)
        return True
    except Exception as e:
        messagebox.showerror("Error al Añadir", f"No se pudo añadir la fila al archivo {nombre_archivo}:\n{e}")
        return False

# --- Lógica de Clientes ---

def cargar_clientes():
    return leer_csv("data_clientes.csv")

def guardar_cliente(datos_cliente_nuevo):
    nombre_archivo = "data_clientes.csv"
    cabecera = ["Nombre", "RUT", "Direccion", "Telefono", "Correo"]
    rut_nuevo = datos_cliente_nuevo[1]
    
    clientes_existentes = leer_csv(nombre_archivo, omitir_cabecera=False)
    if not clientes_existentes: # Si el archivo no existe o está vacío
        return escribir_csv(nombre_archivo, [datos_cliente_nuevo], cabecera)

    header = clientes_existentes.pop(0)
    
    for i, cliente in enumerate(clientes_existentes):
        if cliente and cliente[1] == rut_nuevo:
            respuesta = messagebox.askyesno("RUT Duplicado", f"El RUT '{rut_nuevo}' ya existe. ¿Desea reemplazar los datos?")
            if respuesta:
                clientes_existentes[i] = datos_cliente_nuevo
                return escribir_csv(nombre_archivo, clientes_existentes, header)
            else:
                messagebox.showinfo("Operación cancelada", "Por favor, guarde el cliente con un RUT diferente.")
                return False # Indica que no se guardó

    # Si no se encontró, añadirlo al final
    return anadir_fila_csv(nombre_archivo, datos_cliente_nuevo)

def cargar_datos_cliente_por_nombre(nombre_cliente):
    """Busca un cliente por su nombre y devuelve todos sus datos."""
    clientes = cargar_clientes()
    for cliente in clientes:
        if cliente and cliente[0] == nombre_cliente:
            return cliente
    return None

# --- Lógica de Insumos ---

def cargar_insumos():
    return leer_csv("data_productos.csv")

def guardar_insumo(datos_insumo):
    return anadir_fila_csv("data_productos.csv", datos_insumo)

# --- Lógica de Cotizaciones ---

def cargar_cotizaciones():
    return leer_csv("data_cotizaciones.csv")

def cargar_detalle_cotizacion(nro_cotizacion):
    detalles_completos = leer_csv("data_cotizaciones_detalle.csv")
    detalles_filtrados = []
    for row in detalles_completos:
        if row and row[0] == str(nro_cotizacion):
            # (Cantidad, Descripcion1, PrecioUnitario, Subtotal)
            vista_detalle = (row[1], row[2], row[6], row[7])
            detalles_filtrados.append(vista_detalle)
    return detalles_filtrados

def guardar_cotizacion_completa(cliente, total, detalles):
    # 1. Guardar cabecera de cotización
    cotizaciones = leer_csv("data_cotizaciones.csv")
    nro_cotizacion = len(cotizaciones) + 1
    
    datos_cotizacion = [
        nro_cotizacion,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Pendiente",
        cliente[0],  # Nombre del cliente
        f"{total:.2f}"
    ]
    if not anadir_fila_csv("data_cotizaciones.csv", datos_cotizacion):
        return 0 # Falla al guardar

    # 2. Guardar detalles
    ruta_detalle = os.path.join("data", "data_cotizaciones_detalle.csv")
    with open(ruta_detalle, 'a', newline='', encoding='utf-8') as f:
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
    nombre_archivo_cot = "data_cotizaciones.csv"
    cotizaciones = leer_csv(nombre_archivo_cot, omitir_cabecera=False)
    header_cot = cotizaciones.pop(0)
    
    actualizado = False
    for cotizacion in cotizaciones:
        if cotizacion and cotizacion[0] == str(nro_cotizacion):
            cotizacion[3] = cliente[0] # Nombre Cliente
            cotizacion[4] = f"{total:.2f}" # Total
            actualizado = True
            break
    
    if not actualizado or not escribir_csv(nombre_archivo_cot, cotizaciones, header_cot):
        return False # Falla al actualizar cabecera

    # 2. Borrar detalles antiguos y guardar los nuevos
    nombre_archivo_det = "data_cotizaciones_detalle.csv"
    detalles_existentes = leer_csv(nombre_archivo_det, omitir_cabecera=False)
    header_det = detalles_existentes.pop(0)

    # Filtra para mantener solo los detalles de OTRAS cotizaciones
    detalles_filtrados = [d for d in detalles_existentes if d and d[0] != str(nro_cotizacion)]

    # Añade los nuevos detalles de la cotización actual
    for item_id, valores_vista in detalles.items():
        datos_insumo_completos = valores_vista['insumo_completo']
        detalle_fila = [nro_cotizacion, valores_vista['vista'][0], datos_insumo_completos[0], 
                        datos_insumo_completos[1], datos_insumo_completos[2], datos_insumo_completos[3], 
                        float(valores_vista['vista'][2]), float(valores_vista['vista'][3])]
        detalles_filtrados.append(detalle_fila)

    escribir_csv(nombre_archivo_det, detalles_filtrados, header_det)
    return True

def actualizar_campo_cotizacion(nro_cotizacion, columna_actualizar, nuevo_valor):
    nombre_archivo = "data_cotizaciones.csv"
    cotizaciones = leer_csv(nombre_archivo, omitir_cabecera=False)
    header = cotizaciones.pop(0)
    
    for cotizacion in cotizaciones:
        if cotizacion and cotizacion[0] == str(nro_cotizacion):
            cotizacion[columna_actualizar] = nuevo_valor
            break
    return escribir_csv(nombre_archivo, cotizaciones, header)

def borrar_cotizacion_completa(nro_cotizacion):
    # Borrar de data_cotizaciones.csv
    cotizaciones = [c for c in leer_csv("data_cotizaciones.csv") if c and c[0] != str(nro_cotizacion)]
    escribir_csv("data_cotizaciones.csv", cotizaciones, ["Nro", "Fecha", "Estado", "Cliente", "Total"])

    # Borrar de data_cotizaciones_detalle.csv
    detalles = [d for d in leer_csv("data_cotizaciones_detalle.csv") if d and d[0] != str(nro_cotizacion)]
    escribir_csv("data_cotizaciones_detalle.csv", detalles, ["Nro_Cotizacion", "Cantidad", "Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "PrecioUnitario", "Subtotal"])