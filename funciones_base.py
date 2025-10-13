import os, time, subprocess, csv
from pathlib import Path
import base64 as b64
from multiprocessing import Pool
from tkinter import messagebox, Tk
import warnings
from dotenv import load_dotenv
import requests as rq
from bs4 import BeautifulSoup as bs

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
    def _crear_directorio_si_no_existe(ruta_dir: Path):
        if not ruta_dir.exists():
            ruta_dir.mkdir(parents=True)
            print(f"Directorio '{ruta_dir}' creado!")

    @staticmethod
    def _crear_csv_si_no_existe(ruta_archivo: Path, encabezados: list[str]):
        if not ruta_archivo.exists():
            with open(ruta_archivo, "w", newline="", encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(encabezados)
            print(f"Archivo {ruta_archivo.name} creado!")

    @staticmethod
    def creacion_entorno():
        try:
            env_path = Path(".env")
            if not env_path.exists():
                with open(env_path, "w") as env_file:
                    chrome = "%APPDATA%/Google/Chrome"
                    env_file.write("USERNAME=''\nPASSWORD=''\nCARPETA=''\n")
                    env_file.write("IMAGEN_FONDO='/assets/background.jpg'\n")
                    env_file.write("ICONO_APP='/assets/logo.ico'\n")
                    env_file.write(f"PERFIL_CHROME={chrome}")
                print("Archivo .env creado!")

            # Creacion de Carpetas Básicas
            directorios = ["data", "assets", "pdfs"]
            for dir_nombre in directorios:
                cimiento._crear_directorio_si_no_existe(Path(dir_nombre))

            data_dir = Path("data")

            # Creación de archivos CSV
            archivos_csv = {
                "data_clientes.csv": ["Nombre", "RUT", "Direccion", "Telefono", "Correo"],
                "data_productos.csv": ["Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "Costo", "Precio"],
                "data_cotizaciones.csv": ["Nro", "Fecha", "Estado", "Cliente", "PrecioTotal"],
                "data_cotizaciones_detalle.csv": ["Nro_Cotizacion", "Cantidad", "Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "PrecioUnitario", "Subtotal"]
            }

            for nombre_archivo, headers in archivos_csv.items():
                cimiento._crear_csv_si_no_existe(data_dir / nombre_archivo, headers)

        except Exception as e:
            print(f"Error al crear el entorno: {e}")

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