import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from Cargar_imagenes import CargarImagenes
import CrearBotones
from tkinter import filedialog
import io
from PIL import Image, ImageTk
import time
from datetime import datetime, timedelta
import babel
import babel.numbers
import tkinter as tk
from tkcalendar import Calendar, DateEntry

class interfaz(CargarImagenes):
    def __init__(self, ventana,Hotel):
        style = ttk.Style()
        self.item = 1
        style.configure("Custom.TCheckbutton", font=("times", 10, "bold"))
        style.configure("Custom.TButton", font=("times", 10))
        style.configure("Custom_1.TCombobox", font=("times", 20, "bold"),bg = "red")
        style.configure("Custom.TEntry", font=("times", 10), width = 10)
        style.configure("Custom.TLabel", font=("times", 13))
        style.configure("Fecha.TLabel", font=("times", 10))
        self.Fecha = datetime.now()
        CargarImagenes.__init__(self)
        self.ventana = ventana
        # Hotel
        self.Hotel = Hotel
        self.datos_nuevo_huesped = {}
        self.toplevel_nuevo_huesped = Toplevel(self.ventana)

        self.toplevel_nuevo_huesped.columnconfigure(2, weight=2)



        frame_datos_huesped = LabelFrame(self.toplevel_nuevo_huesped, text = "Datos de Huesped", font= ("times", 20),bd=0)
        frame_datos_huesped.grid(row = 0, column = 0, rowspan = 5, padx=5, pady=3,sticky="wnes")

        separador_horizonal = ttk.Separator(self.toplevel_nuevo_huesped, orient="vertical")
        separador_horizonal.grid(row=0, column=1, rowspan=5, padx=2, pady=10,sticky="ns")

        frame_servicios_huesped = LabelFrame(self.toplevel_nuevo_huesped, text = "", font= ("times", 20))
        frame_servicios_huesped.grid(row = 0, column = 2, columnspan=2, sticky="wnes")

        frame_servicios_huesped_inicio = LabelFrame(self.toplevel_nuevo_huesped, text = "", font= ("times", 20), bd = 0)
        frame_servicios_huesped_inicio.grid(row = 1, column = 2, columnspan=2, sticky="wnes")

        frame_servicios_huesped_fecha = LabelFrame(self.toplevel_nuevo_huesped, text = "", font= ("times", 20), bd = 0)
        frame_servicios_huesped_fecha.grid(row = 2, column = 2, columnspan=2, sticky="wnes")

        frame_tabla_huesped = LabelFrame(self.toplevel_nuevo_huesped, text = "", font= ("times", 20),bd= 0)
        frame_tabla_huesped.grid(row = 3, column = 2, sticky="wnes")

        frame_tabla_huesped_botones = LabelFrame(self.toplevel_nuevo_huesped, text = "", font= ("times", 20))
        frame_tabla_huesped_botones.grid(row = 3, column = 3, sticky="wnse")

        frame_observaciones_huesped = LabelFrame(self.toplevel_nuevo_huesped, text = "Observaciones", font= ("times", 15), bd = 0)
        frame_observaciones_huesped.grid(row = 4, column = 2,  columnspan=2, pady=3, sticky="wnes")

        frame_Total_huesped = LabelFrame(frame_observaciones_huesped, text = "", font= ("times", 20))
        frame_Total_huesped.pack(side="right",padx=5, pady=3)

        self.frame_fecha_perrsonalizada = LabelFrame(frame_servicios_huesped_fecha, text = "", font= ("times", 20), bd= 0)
        

        lista = {"Cédula":self.imgCedula,
                "Nombre":self.imgNombre,
                "Celular":self.imgCelular}
        
        for i, texto in enumerate(lista):
            y = ttk.Label(frame_datos_huesped, text = texto, image=lista[texto], compound="left", style = "Custom.TLabel", justify="left")
            y.grid(row = 0 + 2*i, column=0, padx=2,pady=2, sticky="w")
            y.image = lista[texto]
            x = StringVar()
            self.datos_nuevo_huesped[texto] = x
            CrearBotones.entrada(frame_datos_huesped, x, "", "", style = "Custom.TEntry").grid(row = 1 + 2*i , column=0, padx=2,pady=5)
        ttk.Label(frame_datos_huesped, text = "Habitaciones", image = self.imgHabi, compound="left", style = "Custom.TLabel", justify="left").grid(row = 6, column=0, padx=2,pady=2, sticky="w")
        self.lista_habitaciones = CrearBotones.CheckboxCombobox(frame_datos_huesped, font=("times", 15))
        self.lista_habitaciones.grid(row = 7, column=0, padx=2,pady=2, sticky="w")
        self.lista_habitaciones.valores(self.Hotel.habitaciones)
        
        
        ttk.Label(frame_servicios_huesped, text = "Seleccione servicio", image=self.imgServicio, compound="left",  style = "Custom.TLabel").grid(row = 0, column=0, columnspan=2, padx=2,pady=2)

        self.caja_servicio = ttk.Combobox(frame_servicios_huesped, values = list(self.Hotel.dic_servicios.keys()), font=("times", 15), width=25, state="readonly")
        self.caja_servicio.grid(row = 1, column=0, columnspan=2, padx=2,pady=2)
        self.caja_servicio.bind("<<ComboboxSelected>>", self.select_servicio)

        self.opcion_fecha_personalizada = BooleanVar()
        self.entrada_inicio = StringVar()

        CrearBotones.radiobutton(frame_servicios_huesped_inicio, "Desayuno ", self.entrada_inicio, "Desayuno","","", self.imgDesayuno16).grid(row = 0, column=0, padx=2,pady=2)
        CrearBotones.radiobutton(frame_servicios_huesped_inicio, "Almuerzo", self.entrada_inicio, "Almuerzo","","", self.imgAlmuerzo16).grid(row = 0, column=1, padx=2,pady=2, sticky="w")
        CrearBotones.radiobutton(frame_servicios_huesped_inicio, "Cena", self.entrada_inicio, "Cena","","", self.imgCena16).grid(row = 0, column=2, padx=2,pady=2, sticky="w")

        ttk.Checkbutton(frame_servicios_huesped_fecha, text= "Fecha personalizada",variable=self.opcion_fecha_personalizada, style="Custom_1.TCheckbutton", command=self.check_fecha_personalizada).grid(row = 0, column=0, sticky="w",pady=2)

        ttk.Label(self.frame_fecha_perrsonalizada, text = "Fecha inicio", image=self.imgDias_1, compound="left",  style = "Fecha.TLabel").grid(row = 0, column=0, padx=2,pady=2)
        ttk.Label(self.frame_fecha_perrsonalizada, text = "Fecha fin", image=self.imgDias_1, compound="left",  style = "Fecha.TLabel").grid(row = 0, column=2, padx=2,pady=2)
        self.fecha_inicio_combo = DateEntry(self.frame_fecha_perrsonalizada, locale="es_ES", date_pattern="yyyy-mm-dd", state="readonly", font = ("times",10))
        self.fecha_fin_combo = DateEntry(self.frame_fecha_perrsonalizada, locale="es_ES", date_pattern="yyyy-mm-dd", state="readonly", font = ("times",10))

        self.fecha_inicio_combo.grid(row = 0, column=1, padx=2)
        self.fecha_fin_combo.grid(row = 0, column=3, padx=2)

        ttk.Label(frame_servicios_huesped, text = "Precio", image=self.imgPrecio, compound="left",  style = "Custom.TLabel").grid(row = 0, column=2, padx=2,pady=2)
        ttk.Label(frame_servicios_huesped, text = "días", image=self.imgDias, compound="left",  style = "Custom.TLabel").grid(row = 0, column=3, padx=2,pady=2)
        ttk.Label(frame_servicios_huesped, text = "Personas", image=self.imgPersona, compound="left",  style = "Custom.TLabel").grid(row = 0, column=4, padx=2,pady=2)
        
        self.entrada_precio = StringVar()
        self.entrada_dias = StringVar()
        self.entrada_personas = StringVar()       

        CrearBotones.entrada(frame_servicios_huesped, self.entrada_precio, "", "", style = "Custom.TEntry",width=20).grid(row = 1, column=2, padx=2,pady=2)
        self.entry_dias = CrearBotones.entrada(frame_servicios_huesped, self.entrada_dias, "", "", style = "Custom.TEntry",width=10)
        self.entry_dias.grid(row = 1, column=3, padx=5,pady=2)
        CrearBotones.entrada(frame_servicios_huesped, self.entrada_personas, "", "", style = "Custom.TEntry",width=10).grid(row = 1, column=4, padx=5,pady=2)

        CrearBotones.BotonesImagenes(frame_servicios_huesped,self.imgNuevo,self.imgNuevo1, self.agregar_servicio, "",20).grid(row = 1, column=5, padx=2,pady=2)


        

        self.tabla_servicios_huesped = CrearBotones.TreeView(frame_tabla_huesped, ["","Servicio", "Cant", "Dias", "Fecha Inicio","Fecha fin", "Precio", "Total"], [0, 100, 10, 10, 40, 40, 60, 60])
        self.tabla_servicios_huesped.config(height = 5)

        CrearBotones.Botones(frame_tabla_huesped_botones, "Eleminar", self.eliminar_servicio, self.imgDelete).grid(row = 1, column = 1, padx = 2, pady = 2, sticky = "we")

        self.entrada_observaciones = Text(frame_observaciones_huesped, width=10, height=5, font=("times", 13))
        self.entrada_observaciones.pack(fill="both", side="left", expand=True, padx=2, pady=2)

        self.sub_total_servicio = IntVar()
        self.entrada_efectivo = IntVar()
        self.entrada_trnasferencia = IntVar()
        self.total_servicio = IntVar()

        Label(frame_Total_huesped, text = "Subtotal:", font = ("times", 18),justify="right",anchor="e").grid(row = 0, column = 0, padx=2, pady=2, sticky="we")
        Label(frame_Total_huesped, text = "Efectivo:", font = ("times", 18),justify="right",anchor="e").grid(row = 1, column = 0, padx=2, pady=2, sticky="we")
        Label(frame_Total_huesped, text = "Transferencia:", font = ("times", 18),justify="right",anchor="e").grid(row = 2, column = 0, padx=2, pady=2, sticky="we")
        Label(frame_Total_huesped, text = "Total:", font = ("times", 18),justify="right",anchor="e").grid(row = 3, column = 0, padx=2, pady=2, sticky="we")

        self.label_sub_total = Label(frame_Total_huesped, text = "$ 0", font = ("times", 18),justify="left",anchor="w")
        self.label_sub_total.grid(row = 0, column = 1, padx=2, pady=2)
        entreda_efectivo = CrearBotones.entrada(frame_Total_huesped, self.entrada_efectivo, "", "", justify = "right")
        entreda_transfer = CrearBotones.entrada(frame_Total_huesped, self.entrada_trnasferencia, "", "", justify = "right")
        self.label_total = Label(frame_Total_huesped, text = "$ 0", font = ("times", 18),justify="left",anchor="w")
        self.label_total.grid(row = 3, column = 1, padx=2, pady=2)

        entreda_efectivo.grid(row = 1, column = 1, padx=2, pady=2)
        entreda_transfer.grid(row = 2, column = 1, padx=2, pady=2)

        entreda_efectivo.bind("<KeyRelease>", self.sumar_pagos)
        entreda_transfer.bind("<KeyRelease>", self.sumar_pagos)
        CrearBotones.CenterWindow(self.toplevel_nuevo_huesped)

    def select_servicio (self, event = None):
        servicio = self.caja_servicio.get()
        if servicio in self.Hotel.dic_servicios:
            self.entrada_precio.set(int(self.Hotel.dic_servicios[servicio]))

    def agregar_servicio(self, texto=None):
        if self.opcion_fecha_personalizada.get():
            # Obtener las fechas desde los widgets DateEntry
            fecha_inicio = self.fecha_inicio_combo.get()
            fecha_fin = self.fecha_fin_combo.get()

            # Convertir las fechas de cadena a objetos datetime
            fecha_objeto1 = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_objeto2 = datetime.strptime(fecha_fin, "%Y-%m-%d")

            # Calcular la diferencia en días
            dias = int((fecha_objeto2 - fecha_objeto1).days)
            print(f"Diferencia en días (fecha personalizada): {dias}")
        else:
            # Si no se usa fecha personalizada, obtener la fecha inicial y sumar los días
            fecha_inicio = self.Fecha.strftime("%Y-%m-%d")  # Asegúrate de que self.Fecha es un objeto datetime
            dias = int(self.entrada_dias.get())  # Convertir el valor de entrada en número entero

            # Sumar los días a la fecha inicial
            fecha_objeto_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_objeto_fin = fecha_objeto_inicio + timedelta(days=dias)

            # Convertir la fecha final a string
            fecha_fin = fecha_objeto_fin.strftime("%Y-%m-%d")
            print(f"Fecha final (sin fecha personalizada): {fecha_fin}")

        try:
            # Obtener valores y convertir a enteros
            precio = int(self.entrada_precio.get())
            personas = int(self.entrada_personas.get())
            
            # Calcular total
            total = precio * dias * personas
            print(f"Total: {total}")
        except ValueError:
            print("Error: Asegúrate de que todos los campos contengan números enteros válidos.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        
        self.sub_total_servicio.set(int(self.sub_total_servicio.get()) + int(total))
        self.total_servicio.set(int(self.total_servicio.get()) + int(total))
        self.label_sub_total.config(text = '$ {:,}'.format(self.sub_total_servicio.get()))
        self.sumar_pagos()

        datos = [self.caja_servicio.get(), self.entrada_personas.get(), dias, fecha_inicio, fecha_fin, self.entrada_precio.get(), total]
        self.tabla_servicios_huesped.insertar_elemento_principal("", "", datos)
        
        self.caja_servicio.set("")
        self.entrada_personas.set("")
        self.entrada_dias.set("")
        self.entrada_precio.set("")

        self.opcion_fecha_personalizada.set(False)
        self.select_servicio()

    def edit_servicio(self, texto = None):
        pass

    def eliminar_servicio(self, texto = None):
        try:
            selection = self.tabla_servicios_huesped.selection()[0]
            id = self.tabla_servicios_huesped.item(selection)["text"]
            datos = self.tabla_servicios_huesped.item(selection)["values"]
            self.tabla_servicios_huesped.delete(selection)
            
        except:
            pass
        x = int(self.sub_total_servicio.get()) - int(datos[-1])
        self.sub_total_servicio.set(x)
        self.label_sub_total.config(text = '$ {:,}'.format(self.sub_total_servicio.get()))
        
        self.sumar_pagos()
    
    def sumar_pagos(self, event = None):
        try:
            x1 = int(self.entrada_efectivo.get())
        except ValueError:
            x1 = 0  # Asignar un valor por defecto si ocurre el error

        try:
            x2 = int(self.entrada_trnasferencia.get())
        except ValueError:
            x2 = 0  # Asignar un valor por defecto si ocurre el error

        try:
            x3 = int(self.sub_total_servicio.get())
        except ValueError:
            x3 = 0  # Asignar un valor por defecto si ocurre el error

        suma = x3 - ( x1 + x2)
        self.total_servicio.set(suma)
        self.label_total.config(text = '$ {:,}'.format(self.total_servicio.get()))

    def check_fecha_personalizada(self):
        if self.opcion_fecha_personalizada.get():
            self.frame_fecha_perrsonalizada.grid(row = 0, column = 1,columnspan=3,sticky="we")
            self.entry_dias.config(state="disable")
        else:
            self.frame_fecha_perrsonalizada.grid_forget()
            self.entry_dias.config(state="normal")