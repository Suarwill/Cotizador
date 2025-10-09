# Sistema de Cotizaciones

Este es un sistema de escritorio desarrollado en Python con Tkinter para la creación, gestión y seguimiento de cotizaciones comerciales. Permite administrar una base de datos de clientes y productos (insumos) para agilizar el proceso de cotización.

---

## Características Principales

- **Gestión de Clientes**: Permite añadir, buscar y seleccionar clientes para las cotizaciones.
- **Gestión de Productos (Insumos)**: Mantiene un catálogo de productos con descripciones y precios que se pueden añadir a las cotizaciones.
- **Creación de Cotizaciones**: Interfaz intuitiva para construir una cotización añadiendo productos, especificando cantidades y calculando totales automáticamente.
- **Búsqueda y Edición**: Permite buscar cotizaciones guardadas, ver sus detalles, editar su contenido o estado, y eliminarlas.
- **Persistencia de Datos**: Toda la información se guarda localmente en archivos CSV, facilitando su gestión y respaldo.

---

## Requisitos

- Python 3.x

El programa se encarga de instalar automáticamente las librerías necesarias (`sv-ttk`, `python-dotenv`, etc.) durante su primer arranque.

---

## Instalación y Primer Uso

1.  Clona o descarga este repositorio en tu máquina local.
2.  Asegúrate de tener Python instalado.
3.  Ejecuta el archivo `main.pyw`.

    ```bash
    python main.pyw
    ```

4.  En la primera ejecución, el programa:
    - Instalará las dependencias que falten.
    - Creará una carpeta `data/` en el directorio del proyecto.
    - Dentro de `data/`, generará los archivos CSV necesarios para almacenar clientes, productos y cotizaciones.

---

## Manual de Usuario

La aplicación se organiza a través de una barra de menú en la parte superior.

### 1. Gestión de Clientes

- **Ruta**: `Menú -> Clientes`
- **Para añadir un cliente**: Rellena los campos del formulario (Nombre, RUT, etc.) y haz clic en **Guardar**.
- **Para buscar/editar un cliente**: Haz clic en **Buscar**, selecciona un cliente de la lista con doble clic. Sus datos se cargarán en el formulario para que puedas modificarlos y guardarlos de nuevo.

### 2. Gestión de Productos (Insumos)

- **Ruta**: `Menú -> Productos -> Insumos`
- **Para añadir un producto**: Rellena los campos (descripciones, precio, etc.) y haz clic en **Guardar**. La "Descripción 1" es el campo principal que se mostrará en las búsquedas.
- **Para buscar/editar un producto**: Similar a los clientes, usa el botón **Buscar** para cargar un producto existente en el formulario.

### 3. Crear una Cotización

- **Ruta**: `Menú -> Cotizaciones -> Crear Cotización`
1.  **Seleccionar Cliente**: Haz clic en **Buscar Cliente** y selecciona uno de la lista con doble clic.
2.  **Añadir Productos**:
    - Haz clic en **Buscar Insumo** para abrir la lista de productos. Selecciónalo con doble clic.
    - Ingresa la **Cantidad** deseada.
    - Haz clic en **Añadir a la Cotización**. El producto aparecerá en la tabla de detalles.
3.  **Repetir**: Repite el paso 2 para todos los productos que necesites.
4.  **Editar detalles en la tabla**: Si necesitas cambiar la cantidad o el precio de un ítem ya añadido, haz doble clic sobre la celda correspondiente en la tabla, modifica el valor y presiona `Enter`. El subtotal y el total se actualizarán automáticamente.
5.  **Guardar**: Una vez que la cotización esté completa, haz clic en **Guardar Cotización**.

### 4. Buscar y Administrar Cotizaciones

- **Ruta**: `Menú -> Cotizaciones -> Buscar Cotización`
- En esta ventana verás una lista de todas las cotizaciones guardadas.
- **Ver Detalles**: Haz doble clic sobre una cotización para ver sus productos en la tabla inferior.
- **Editar Contenido**: Selecciona una cotización de la lista y haz clic en **Editar Contenido**. Se abrirá la ventana de creación con todos los datos cargados para que puedas modificarlos y volver a guardarlos.
- **Editar Estado**: Selecciona una cotización y haz clic en **Editar Estado** para cambiar su estado (ej: de "Pendiente" a "Aprobada").
- **Borrar Cotización**: Selecciona una cotización y haz clic en **Borrar Cotización** para eliminarla permanentemente.
