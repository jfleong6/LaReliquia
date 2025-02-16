from tkinter import ttk, filedialog
from tkinter.ttk import *
import tkinter as tk

import subprocess
import sys
import os

def cargar_archivo_py():
    filename = filedialog.askopenfilename(filetypes=[("Archivos Python", "*.py;*.pyw")])
    if filename:
        archivos_cargados['py'] = filename
        actualizar_estado_botones()

def cargar_archivo_ico():
    filename = filedialog.askopenfilename(filetypes=[("Archivos ICO", "*.ico")])
    if filename:
        archivos_cargados['ico'] = filename
        actualizar_estado_botones()

def seleccionar_carpeta_destino():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_destino.set(carpeta)
        actualizar_estado_botones()

def actualizar_estado_botones():
    if archivos_cargados.get('py') and archivos_cargados.get('ico') and carpeta_destino.get():
        boton_crear.config(state=tk.NORMAL)
    else:
        boton_crear.config(state=tk.DISABLED)

def crear_ejecutable(script, icono=None, carpeta_destino=None, archivos_adicionales=None):
    command = ['pyinstaller', '--onefile']

    if icono:
        command.extend(['--icon', icono])

    if carpeta_destino:
        command.extend(['--distpath', carpeta_destino])

    if archivos_adicionales:
        for archivo in archivos_adicionales:
            command.extend(['--add-data', f'{archivo};.'])

    command.append(script)

    try:
        subprocess.run(command, check=True)
        print("¡Archivo ejecutable creado con éxito!")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el ejecutable: {e}")
        sys.exit(1)
def ejecutar_creacion():
    py_file = archivos_cargados.get('py')
    ico_file = archivos_cargados.get('ico')
    destino_folder = carpeta_destino.get()

    if py_file and ico_file and destino_folder:
        crear_ejecutable(py_file, ico_file, destino_folder)

def cargar_archivo_adicional():
    # Método para cargar archivos adicionales
    filename = filedialog.askopenfilename()
    if filename:
        archivos_cargados['adicional'] = filename
# Configuración inicial
# Configuración inicial
archivos_cargados = {'py': None, 'ico': None, 'adicionales': []}

# Crear ventana principal
root = tk.Tk()
root.title("Crear Ejecutable")

# Variable de control para la carpeta de destino
carpeta_destino = tk.StringVar()

# Botón para cargar archivo .py
boton_cargar_py = ttk.Button(root, text="Cargar Archivo .py", command=cargar_archivo_py)
boton_cargar_py.pack(fill = "x")

# Botón para cargar archivo .ico
boton_cargar_ico = ttk.Button(root, text="Cargar Archivo .ico", command=cargar_archivo_ico)
boton_cargar_ico.pack(fill = "x")
# Botón para cargar archivo adicional
boton_cargar_adicional = ttk.Button(root, text="Cargar Archivo Adicional", command=cargar_archivo_adicional)
boton_cargar_adicional.pack(fill="x")
# Botón para seleccionar carpeta de destino
boton_carpeta_destino = ttk.Button(root, text="Seleccionar Carpeta Destino", command=seleccionar_carpeta_destino)
boton_carpeta_destino.pack(fill = "x")

# Etiqueta para mostrar la carpeta de destino seleccionada
label_carpeta_destino = tk.Label(root, textvariable=carpeta_destino)
label_carpeta_destino.pack(fill = "x")

# Botón para crear el ejecutable (inicialmente deshabilitado)
boton_crear = ttk.Button(root, text="Crear Ejecutable", command=ejecutar_creacion, state=tk.DISABLED)
boton_crear.pack(fill = "x")

root.mainloop()
