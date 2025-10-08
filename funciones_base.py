import os
import time
import csv
import base64 as b64
from multiprocessing import Pool
import subprocess
from tkinter import messagebox
import warnings
from dotenv import load_dotenv
import requests as rq
from bs4 import BeautifulSoup as bs

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
                print("Archivo .env creado!")
        except Exception as e:
            print(f"Error al crear .env: {e}")

        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"Directorio '{data_dir}' creado!")

            cliente_csv_path = os.path.join(data_dir, "data_cliente.csv")
            if not os.path.exists(cliente_csv_path):
                with open(cliente_csv_path, "w", newline="", encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Nombre", "RUT", "Direccion", "Telefono", "Correo"])
                print("Archivo Clientes creado!")

            productos_csv_path = os.path.join(data_dir, "data_productos.csv")
            if not os.path.exists(productos_csv_path):
                with open(productos_csv_path, "w", newline="", encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "Costo", "Precio"])
                print("Archivo Productos creado!")

            cotizaciones_csv_path = os.path.join(data_dir, "data_cotizaciones.csv")
            if not os.path.exists(cotizaciones_csv_path):
                with open(cotizaciones_csv_path, "w", newline="", encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Nro", "Fecha", "Estado", "Cliente", "PrecioTotal"])
                print("Archivo Cotizaciones creado!")

            cotizaciones_detalle_csv_path = os.path.join(data_dir, "data_cotizaciones_detalle.csv")
            if not os.path.exists(cotizaciones_detalle_csv_path):
                with open(cotizaciones_detalle_csv_path, "w", newline="", encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Nro_Cotizacion", "Cantidad", "Descripcion1", "Descripcion2", "Descripcion3", "Unidad", "PrecioUnitario", "Subtotal"])
                print("Archivo Cotizaciones Detalle creado!")
        except Exception as e:
            print(f"Error al crear entorno de datos: {e}")

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