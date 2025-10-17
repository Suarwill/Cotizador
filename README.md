# Sistema de Cotizaciones

Este es un sistema de escritorio desarrollado en Python con Tkinter para la creación, gestión y seguimiento de cotizaciones comerciales. Permite administrar una base de datos de clientes y productos (insumos), generar cotizaciones y exportarlas a formato PDF.

---

## Características Principales

- **Gestión de Clientes**: Permite añadir, buscar, editar y eliminar clientes. Los datos se almacenan de forma segura.
- **Gestión de Productos (Insumos)**: Mantiene un catálogo de productos con código, descripciones, unidad y precios.
- **Creación y Edición de Cotizaciones**: Interfaz intuitiva para construir una cotización, añadir productos, especificar cantidades y editar detalles directamente en la tabla.
- **Generación de PDF**: Exporta las cotizaciones a un archivo PDF con un formato profesional, incluyendo los datos de tu empresa y el cliente.
- **Búsqueda y Administración**: Permite buscar cotizaciones guardadas, ver sus detalles, editar su contenido o estado, y eliminarlas.
- **Configuración Personalizable**: Permite configurar los datos de la empresa, el icono de la aplicación y la imagen de fondo.
- **Seguridad**: Los datos sensibles (como la información de clientes) se encriptan antes de guardarse.
- **Instalador Sencillo**: Incluye un script `install_and_run.bat` que automatiza la creación de carpetas, la instalación de Python (si es necesario) y las dependencias del proyecto.

---

## Requisitos Técnicos

- Python 3.x

El script de instalación se encarga de instalar automáticamente las librerías necesarias (`sv-ttk`, `python-dotenv`, `reportlab`, etc.) durante su primer arranque.

---

## Instalación y Primer Uso

1.  Descarga el contenido del repositorio en una carpeta en tu computadora.
2.  Navega a la carpeta `installer`.
3.  Ejecuta el archivo `install_and_run.bat` haciendo doble clic sobre él.

4.  El instalador realizará los siguientes pasos automáticamente:
    - Creará la carpeta `C:\Katech\Cotizador`.
    - Copiará los archivos de la aplicación a esa carpeta.
    - Creará un acceso directo en tu escritorio llamado **"Katech - Cotizador"**.
    - Verificará si Python está instalado. Si no lo está, lo descargará e instalará.
    - Instalará todas las librerías necesarias para la aplicación.
    - Ejecutará la aplicación por primera vez.

5.  **Configuración Inicial**: En la primera ejecución, la aplicación te pedirá que ingreses los datos de tu empresa y una clave maestra. Esta información se usará para generar los PDF y para proteger tus datos.

Una vez finalizado, podrás iniciar el programa desde el acceso directo del escritorio.

---

## Manual de Usuario

La aplicación se organiza a través de una barra de menú en la parte superior con las siguientes secciones: `Archivo`, `Cotizaciones`, `Productos` y `Clientes`.

### 1. Gestión de Clientes

- **Ruta**: `Menú -> Clientes`
- **Añadir un cliente**: Rellena los campos del formulario (Nombre, RUT, etc.) y haz clic en **Guardar**.
- **Buscar/Editar un cliente**: Haz clic en **Buscar**, y en la ventana que aparece, haz doble clic sobre el cliente deseado. Sus datos se cargarán en el formulario para que puedas modificarlos y guardarlos de nuevo.
- **Borrar un cliente**: Carga un cliente usando el botón **Buscar** y luego haz clic en **Borrar**.

### 2. Gestión de Productos (Insumos)

- **Ruta**: `Menú -> Productos -> Insumos`
- **Añadir un producto**: Rellena los campos (Código, descripciones, precio, etc.) y haz clic en **Guardar**. El **Código** debe ser único para cada producto.
- **Buscar/Editar un producto**: Usa el botón **Buscar** para cargar un producto existente en el formulario, modificarlo y guardarlo.

### 3. Crear una Cotización

- **Ruta**: `Menú -> Cotizaciones -> Crear Cotización`
1.  **Seleccionar Cliente**: Haz clic en **Buscar Cliente** y elige uno de la lista con doble clic.
2.  **Añadir Productos**:
    - Ingresa la **Cantidad** deseada en el campo correspondiente.
    - Haz clic en **Buscar Insumo** para abrir la lista de productos y selecciónalo con doble clic.
    - Haz clic en **Añadir**. El producto aparecerá en la tabla de detalles.
3.  **Repetir**: Repite el paso 2 para todos los productos que necesites.
4.  **Editar detalles en la tabla**: Si necesitas cambiar la cantidad o el precio de un ítem ya añadido, haz doble clic sobre la celda correspondiente en la tabla, modifica el valor y presiona `Enter`. El subtotal y el total se actualizarán automáticamente.
5.  **Guardar**: Una vez que la cotización esté completa, haz clic en **Guardar Cotización**.

### 4. Buscar y Administrar Cotizaciones

- **Ruta**: `Menú -> Cotizaciones -> Buscar Cotización`
- En esta ventana verás una lista de todas las cotizaciones guardadas.
- **Ver Detalles**: Haz doble clic sobre una cotización para ver sus productos en la tabla inferior.
- **Editar Contenido**: Selecciona una cotización y haz clic en **Editar Contenido**. Se abrirá la ventana de creación con todos los datos cargados para que puedas modificarlos y guardarlos de nuevo.
- **Editar Estado**: Selecciona una cotización y haz clic en **Editar Estado** para cambiar su estado (ej: de "Pendiente" a "Aprobada").
- **Crear PDF**: Selecciona una cotización y haz clic en **Crear PDF**. El archivo se guardará en la carpeta `pdfs` dentro del directorio de instalación.
- **Borrar Cotización**: Selecciona una cotización y haz clic en **Borrar Cotización** para eliminarla permanentemente.

### 5. Configuración

- **Datos de Empresa** (`Menú -> Archivo -> Datos de Empresa`): Aquí puedes modificar el nombre, dirección y contacto de tu empresa que aparecerán en los PDF de las cotizaciones.
- **Configuración General** (`Menú -> Archivo -> Configuración`): Permite cambiar la ruta del icono de la aplicación, la imagen de fondo y la clave maestra para la encriptación de datos. **¡Cuidado!** Cambiar la clave maestra requerirá re-encriptar los datos existentes.
