import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from tkinter import messagebox
import funciones_datos as datos

def generar_pdf(nro_cotizacion):
    try:
        # 1. Cargar todos los datos necesarios
        cotizaciones = datos.cargar_cotizaciones()
        cotizacion_data = next((c for c in cotizaciones if c and c[0] == str(nro_cotizacion)), None)
        if not cotizacion_data:
            messagebox.showerror("Error", f"No se encontraron datos para la cotización N° {nro_cotizacion}.")
            return

        cliente_nombre = cotizacion_data[3]
        cliente_data = datos.cargar_datos_cliente_por_nombre(cliente_nombre)
        if not cliente_data:
            messagebox.showerror("Error", f"No se encontraron datos para el cliente '{cliente_nombre}'.")
            return

        detalles = datos.cargar_detalle_cotizacion(nro_cotizacion)

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