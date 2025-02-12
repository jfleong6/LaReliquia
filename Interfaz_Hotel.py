import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from Cargar_imagenes import CargarImagenes
from Hotel import Hotel
import Huesped
import CrearBotones
from tkinter import filedialog
import io
from PIL import Image, ImageTk

class HotelInterface(CargarImagenes):
    
    def __init__(self, ventana, frame, menuBar):
        style = ttk.Style()
        style.configure("Custom.TCheckbutton", font=("times", 13, "bold"))
        style.configure("Custom.TCombobox", font=("times", 13, "bold"))
        CargarImagenes.__init__(self)
        self.ventana = ventana
        self.frame = frame
        self.menuBar = menuBar
        # Hotel
        self.Hotel = Hotel()
        # Sección Principal
        self.framePrincipal = Frame(self.frame)
        self.framePrincipal.pack(fill='both', expand=True)
        
        # Sección de reportes y botón
        self.frame_reportes = Frame(self.framePrincipal, width=300)
        self.frame_reportes.pack(side="right", fill="y")

        # Label de reportes
        self.label_reportes = Label(self.frame_reportes, text="Reportes", font=("Arial", 14))
        self.label_reportes.pack(side="top", pady=10, fill="y")

        # Botón "Más"
        CrearBotones.BotonesImagenes(self.frame_reportes, self.imgMas, self.imgMas1, self.HuespedNuevo).pack(side="bottom")

        # Sección para la visualización de los huéspedes
        self.frame_huespedes = LabelFrame(self.framePrincipal, text="Huespéd")
        self.frame_huespedes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear el menú del hotel
        self.crear_menu_hotel()
        print("hola")

    def crear_menu_hotel(self):
        # Menú archivo
        archivo_menu = tk.Menu(self.menuBar, tearoff=0)
        
        # Submenú Habitaciones
        habitaciones_menu = tk.Menu(archivo_menu, tearoff=0)
        habitaciones_menu.add_command(label="Nueva habitación", command=self.interfaz_nueva_habitacion, image=self.imgNuevo, compound="left")
        habitaciones_menu.add_command(label="Ver habitaciones", command=self.interfaz_ver_habitacion, image=self.imgVer, compound="left")
        archivo_menu.add_cascade(label="Habitaciones", menu=habitaciones_menu, image=self.imgHotel, compound="left")

        # Submenú Servicios
        servicios_menu = tk.Menu(archivo_menu, tearoff=0)
        servicios_menu.add_command(label="Nuevo servicio", command=self.interfaz_nuevo_servicio, image=self.imgNuevo, compound="left")
        servicios_menu.add_command(label="Ver servicios", command=self.interfaz_ver_servicios, image=self.imgVer, compound="left")
        archivo_menu.add_cascade(label="Servicios", menu=servicios_menu, image=self.imgSencillo, compound="left")
        
        # Agregar el menú a la barra de menú
        self.menuBar.add_cascade(label="Hotel", menu=archivo_menu)

    def interfaz_nueva_habitacion(self):
        # Crear ventana toplevel para nueva habitación
        try:
            self.toplevel_nueva_habitacion.destroy()
        except AttributeError:
            pass
        self.toplevel_nueva_habitacion = Toplevel(self.ventana)
        self.toplevel_nueva_habitacion.title("Nueva Habitación")

        self.label_Frame_Nueva_Habi = LabelFrame(self.toplevel_nueva_habitacion, text="Nueva habitación", font = ("Times",25), labelanchor= "n", bd=0)
        self.label_Frame_Nueva_Habi.pack(fill="both", expand=True, padx=5, pady=5)
        self.datos_nueva_habitacion = {}
        lista = ["Habitación","Capacidad","Cama_doble","Cama_sencilla","Camarote","Tv","Arie_acondicionado","Ventilador"]
        images = [self.imgHotel1,self.imgpPersonas,self.imgCamaDoble,self.imgCamaSencilla,self.imgCamarote,self.imgTv,self.imgAireAcondicionado,self.imgVentilador]
        for i, (texto, image) in enumerate(zip(lista, images)):
            Label(self.label_Frame_Nueva_Habi, text=texto.replace("_", " "), font = ("times",13), image=image,justify="left", compound="left", anchor="w", wraplength=110).grid(row = i, column=0, padx=3, pady=3,sticky="ew")
            y = StringVar()
            x = CrearBotones.entrada(self.label_Frame_Nueva_Habi, y,"","")
            x.grid(row = i, column=1, padx=3, pady=3,sticky="ew")
            self.datos_nueva_habitacion[texto] = y

        # Botón para guardar
        self.boton_guardar_nueva_habi = CrearBotones.Botones(self.label_Frame_Nueva_Habi,"Gruardar",self.guardar_habitacion, self.imgGuardar)
        self.boton_guardar_nueva_habi.grid(row=i+1, column=0, columnspan=2, pady=20,sticky="ew")

        CrearBotones.CenterWindow(self.toplevel_nueva_habitacion)

    def guardar_habitacion(self, texto = None):
        # Obtener los valores ingresados
        numero_habitacion = self.datos_nueva_habitacion["Habitación"].get()
        capacidad = self.datos_nueva_habitacion["Capacidad"].get()

        # Validar campos
        if not numero_habitacion or not capacidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            self.toplevel_nueva_habitacion.attributes('-topmost', True)
            self.toplevel_nueva_habitacion.attributes('-topmost', False)
            return
        
        # Guardar habitacion
        try:
            self.Hotel.nueva_habitacion(self.datos_nueva_habitacion)
        except:
            messagebox.showerror("Error", "Habitacion no guardada.")
            self.toplevel_nueva_habitacion.attributes('-topmost', True)
            self.toplevel_nueva_habitacion.attributes('-topmost', False)

    def interfaz_ver_habitacion(self):
        try:
            self.toplevel_ver_habitacion.destroy()
        except AttributeError:
            pass
        self.toplevel_ver_habitacion = Toplevel(self.ventana)
        labelFrame = LabelFrame(self.toplevel_ver_habitacion,text="Ver habitaciones",labelanchor="n", bd=0)
        labelFrame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tabla_ver_habitaciones = CrearBotones.Tabla_filtro(labelFrame, self.Hotel.habitaciones, ["Id", "Habitaciones", "Capacidad"], [10,15,15], self.interfaz_editar_habitaciones, "Habitaciones", self.imgEdita1)
        CrearBotones.CenterWindow(self.toplevel_ver_habitacion)

    def interfaz_editar_habitaciones(self, tabla, ventana):
        try:
            selection = tabla.selection()[0]
            self.id_editar_habitacion = tabla.item(selection)["text"]
            datos = tabla.item(selection)["values"]
        except (IndexError, KeyError):
            return
        self.interfaz_nueva_habitacion()
        self.label_Frame_Nueva_Habi.config(text=f"Edtar Habitacion {self.id_editar_habitacion}")
        for key,inp in zip(self.datos_nueva_habitacion, datos):
            self.datos_nueva_habitacion[key].set(inp)
        self.boton_guardar_nueva_habi.config(command=self.editar_habitacion, text="Editar habitacion")
    
    def editar_habitacion(self):
        try:
            self.Hotel.editar_habitacion(self.id_editar_habitacion,self.datos_nueva_habitacion)
        except:
            return
        self.toplevel_nueva_habitacion.destroy()
        self.interfaz_ver_habitacion()
        
    def interfaz_nuevo_servicio(self):
        try:
            self.toplevel_servicio_nuevo.destroy()
        except AttributeError:
            pass
        self.toplevel_servicio_nuevo = Toplevel(self.ventana)

        self.labelFrame_Nuevo_Servicio = LabelFrame(self.toplevel_servicio_nuevo, text = "Nuevo servicio", labelanchor="n", font = ("times", 25))
        self.labelFrame_Nuevo_Servicio.pack(fill="both", expand=True, padx=5, pady=5)

        Label(self.labelFrame_Nuevo_Servicio, image=self.imgServicio).grid(row=0, column=0, padx=3, pady=3)
        x = StringVar()
        x.set("Nombre servicio")
        entradaNombre = CrearBotones.entrada(self.labelFrame_Nuevo_Servicio, x, "", "Nombre servicio")
        entradaNombre.grid(row=0, column=1, padx=3, pady=3)

        Label(self.labelFrame_Nuevo_Servicio, image=self.imgPrecio).grid(row=1, column=0, padx=3, pady=3)
        x1 = StringVar()
        x1.set("Precio servicio")
        entradaPrecio = CrearBotones.entrada(self.labelFrame_Nuevo_Servicio, x1, "", "Precio servicio")
        entradaPrecio.grid(row=1, column=1, padx=3, pady=3)

        self.boton_nuevo_servivio_img = CrearBotones.Botones(self.labelFrame_Nuevo_Servicio, "Subir Imagen", self.subir_imagen_new_servcio, self.imgSubir)
        self.boton_nuevo_servivio_img.grid(row=2, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        self.opcion_servicio_compuesto = BooleanVar()
        ttk.Checkbutton(self.labelFrame_Nuevo_Servicio, text="Servicio compuesto", variable=self.opcion_servicio_compuesto, command= self.check_servicio_compuesto, style="Custom.TCheckbutton").grid(row=3, column=0, columnspan=2, padx=3, pady=3, sticky="we")


        valores = [descripcion[0] for descripcion in self.Hotel.run_query("SELECT descripcion FROM servicios")]
        valores += [descripcion[0] for descripcion in self.Hotel.run_query_rest("SELECT descripcion FROM Categorias")]
        self.servicios_compuestos = CrearBotones.CheckboxCombobox(self.labelFrame_Nuevo_Servicio)
        self.servicios_compuestos.valores(valores)
        self.servicios_compuestos.config(style="Custom.TCombobox")
        
        self.boton_Guardar_nuevo_servicio = CrearBotones.Botones(self.labelFrame_Nuevo_Servicio, "Guardar servicio", self.guardar_nuevo_servicio, self.imgGuardar)
        self.boton_Guardar_nuevo_servicio.grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        with open("Imagenes/subir.png", "rb") as file:
            self.image_data = file.read()
        self.datos_nuevo_servicio = {"descripcion":x,"precio":x1,"imagen":self.image_data}
        CrearBotones.CenterWindow(self.toplevel_servicio_nuevo)
    
    def check_servicio_compuesto(self):
        if self.opcion_servicio_compuesto.get():
            self.servicios_compuestos.grid(row=4, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        else:
            self.servicios_compuestos.grid_forget()
    
    def guardar_nuevo_servicio(self, texto =None):
        servicio = self.datos_nuevo_servicio["descripcion"].get()
        precio = self.datos_nuevo_servicio["precio"].get()
        if not servicio or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            self.toplevel_nueva_habitacion.lift()
            return
        self.Hotel.nuevo_servicio(self.datos_nuevo_servicio)
        if self.opcion_servicio_compuesto.get():
            id = self.Hotel.run_query("SELECT id FROM servicios ORDER BY id DESC LIMIT 1")[0][0]
            self.Hotel.nuevos_servicios_compuestos(id,(self.servicios_compuestos.check_values))
        messagebox.showinfo("Guardar", f"Servicio guardado")
        self.toplevel_servicio_nuevo.destroy()

    def subir_imagen_new_servcio(self, texto = None):
        # Abrir un cuadro de diálogo para seleccionar una imagen
        ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif")]
        )
        
        # Si se selecciona una imagen, cargarla
        with open(ruta_imagen, "rb") as file:
            self.image_data = file.read()
            img = PhotoImage(file=ruta_imagen)
            self.datos_nuevo_servicio["imagen"] = self.image_data
            self.boton_nuevo_servivio_img.config(image = img)
            self.boton_nuevo_servivio_img.image = img
            self.toplevel_servicio_nuevo.lift()

    def interfaz_ver_servicios(self):
        self.toplevel_ver_servicios = Toplevel(self.ventana)

        labelFrame = LabelFrame(self.toplevel_ver_servicios, text="Servicios", font=("times", 25), bd=0, labelanchor="n")
        labelFrame.pack(fill="both", expand=True, padx=5, pady=5)
        self.tabla_ver_servicios = CrearBotones.Tabla_filtro(labelFrame, self.Hotel.servicios, ["Id", "Servicio", "Precio"],[5,30,20], self.interfaz_editar_servicio, "Servicio", self.imgContinuar)

        CrearBotones.CenterWindow(self.toplevel_ver_servicios)
    
    def interfaz_editar_servicio(self, tabla, ventana):
        try:
            selection = tabla.selection()[0]
            self.id_editar_servicio = tabla.item(selection)["text"]
            datos = tabla.item(selection)["values"]
        except (IndexError, KeyError):
            return
        self.interfaz_nuevo_servicio()
        self.labelFrame_Nuevo_Servicio.config(text="Editar Servicio")
        self.datos_nuevo_servicio["descripcion"].set(datos[0])
        self.datos_nuevo_servicio["precio"].set(datos[1])
        self.boton_Guardar_nuevo_servicio.config(text="Editar habitacion", command= self.editar_servicio)
        imagen = self.Hotel.run_query(f"Select imagen From servicios where id = {self.id_editar_servicio}")[0][0]
        self.datos_nuevo_servicio["imagen"] = imagen
        image = Image.open(io.BytesIO(imagen))
        photo = ImageTk.PhotoImage(image)
        self.boton_nuevo_servivio_img.config(image = photo)
        self.boton_nuevo_servivio_img.image = photo
        lista = [i[0] for i in self.Hotel.run_query(f"Select descripcion From servicios_compuesta Where id_servicio = '{self.id_editar_servicio}'")]

        if len(lista)>0:
            self.opcion_servicio_compuesto.set(True)
            self.check_servicio_compuesto()
            self.servicios_compuestos.set_checked_values(lista)

    def editar_servicio(self):
        servicio = self.datos_nuevo_servicio["descripcion"].get()
        precio = self.datos_nuevo_servicio["precio"].get()
        if not servicio or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            self.toplevel_nueva_habitacion.lift()
            return
        self.Hotel.editar_servicio(self.id_editar_servicio, self.datos_nuevo_servicio)
        self.Hotel.eliminar_servicios_compuestos(self.id_editar_servicio)
        if self.opcion_servicio_compuesto.get():
            self.Hotel.nuevos_servicios_compuestos(self.id_editar_servicio,(self.servicios_compuestos.check_values))
        self.toplevel_servicio_nuevo.destroy()
        self.tabla_ver_servicios.destroy()
        self.interfaz_ver_servicios()

    def HuespedNuevo(self, texto=None):
        Huesped.interfaz(self.ventana, self.Hotel)
    
    def on_mas_click(self):
        messagebox.showinfo("Información", "Aquí puedes agregar más funcionalidad")

if __name__ == '__main__':
    master = tk.Tk()
    frame = Frame(master)
    menu_principal = Menu(master)
    aplicacion1=HotelInterface(master,frame,menu_principal)
    master.mainloop()