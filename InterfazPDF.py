from pdf2image import convert_from_path
from PIL import Image, ImageTk
import tabla
import os
import tempfile
import tkinter as tk
from tkinter import ttk

ruta_temporal = tempfile.gettempdir()
# Función para crear el PDF y mostrar el visor
def crearPDF_y_mostrar_visor():
    pass

# Crear ventana TopLevel
def crear_interfaz_pdf():
    ventana_pdf = tk.Toplevel(root)
    ventana_pdf.title("Crear PDF")

    # Botón para crear el PDF y mostrar el visor
    btn_crear_pdf = ttk.Button(ventana_pdf, text="Crear PDF y Mostrar", command=crearPDF_y_mostrar_visor)
    btn_crear_pdf.pack(padx=10, pady=10)

# Crear ventana principal
root = tk.Tk()
root.title("Interfaz Principal")

# Botón para abrir la ventana TopLevel
btn_abrir_pdf = ttk.Button(root, text="Abrir PDF", command=crear_interfaz_pdf)
btn_abrir_pdf.pack(padx=20, pady=20)

root.mainloop()
