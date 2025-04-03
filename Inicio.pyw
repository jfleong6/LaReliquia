from tkinter import simpledialog
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3
from functools import partial
import CrearBotones,PDF,Interfaz_Hotel,CrearTablas
from Cargar_imagenes import CargarImagenes
from agregarScroll import AgregarScrollVerticar
import time
from functools import partial
import babel
import babel.numbers
import tkinter as tk
from tkcalendar import DateEntry
from server import PedidoAPI
from tkinter import  ttk , filedialog
from tkinter import *
import win32print
import io
from PIL import Image, ImageTk
import traceback
from datetime import datetime
from tienda import InterfazPrincipal
import tempfile
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import socket
import locale
import asyncio
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Interfaz(CargarImagenes):
    def __init__(self):
        #self.loop = asyncio.new_event_loop()  # Crea un loop para tareas async
        #asyncio.set_event_loop(self.loop)
        ruta_temporal = tempfile.gettempdir()
        self.ruta_temporal = os.path.join(ruta_temporal, 'GrupoJJ\\Base de datos.s3db')

        self.CaracPepidos = ["Comanda", "Fecha", "Mesero", "Mesa", "Hora", "TipoCliente", "cliente", "cantidad",
                            "categoria", "SubCant", "descripcion", "pagos", "Total", "TipoPago", "observaciones",
                             "Activo"]
        self.CaracteristicaPepidos = ["Comanda", "Fecha", "Mesero", "Mesa", "Hora", "TipoCliente", "cliente",
                             "Total", "TipoPago", "observaciones","Activo"]
        self.Todos_Pedidos = {}
        self.Fecha = time.strftime("%Y-%m-%d") 
        self.ventana1 = Tk()
        self.ancho = self.ventana1.winfo_screenwidth()
        self.alto = self.ventana1.winfo_screenheight()
        self.ventana1.geometry(f"{self.ancho}x{self.alto}+0+0")
        # Vincular función al evento de cierre de la ventana
        self.ventana1.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        #self.ventana1.resizable(0,0)
        #SELF.ventana1.reside()
        self.ventana1.state('zoomed')
        rutaIcono = Image.open("Imagenes/Logo.ico")
        self.imgIcono = ImageTk.PhotoImage(rutaIcono)
        CargarImagenes.__init__(self)
        self.ventana1.iconphoto(True,self.imgIcono)
        
        self.baseDatos = "Base de datos.s3db"
        CrearTablas.Restaurante()
        self.actulizarDatos()
        
        self.ventana1.configure(bg=self.Datos["Fondo"])
        self.ventana1.title(self.Datos["Empresa"])
        #self.ventana1.bind("<Key>", self.mouse_scroll)
        #self.ventana1.bind("<Key>", self.mouse_scroll01)
        self.Etiqueta = {}
        self.cuaderno1 = Notebook(self.ventana1)
        
        self.menu_principal = Menu(self.ventana1)
        self.ventana1.config(menu=self.menu_principal)
        
        
        self.style = ttk.Style()
        self.style.configure('custom.TRadiobutton', font=(self.Datos["Tipo de letra"],13))
        self.style.configure('principal.TButton', font=('Helvetica', 12), anchor='w', cursor="hand2")
        self.style.configure('sub.TButton', font=('Helvetica', 10), anchor='w')
        self.style.configure('iconos.TButton', font=('Times New Roman', 20), anchor='w')
        self.style.configure("Custom.TLabelframe", font=('Times New Roman', 20), anchor='w',bd = 0)
        #self.style.configure('entrada.TEntry',font =  tkfont(self.Datos["Tipo de letra"],  30))
        self.tamañoLabelFrame = (self.Datos["Tipo de letra"],15)
        
        self.InterfazLogin()
        
    def obtener_ip_servidor(self):
        return socket.gethostbyname(socket.gethostname())
    def cerrar_ventana(self):
        if messagebox.askyesno(title="Cerrar Ventana",message="¿Estás seguro de que deseas cerrar la ventana?"):
            self.ventana1.destroy()
    
    def menuArchivo(self):
        self.menu_Archivo = Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Archivo", menu=self.menu_Archivo)
        self.menu_Archivo.add_command(label="Empresa", command=self.ventanaInterfazConfigEmpresa, image=self.imgconfiguracionGeneral,compound="left")
        self.menu_Archivo.add_separator()
        self.menu_Archivo.add_command(label="Salir", command=self.salir, image=self.imgSalir,compound="left")
    def subMenuArchivoCerrarSesion(self):
        self.menu_Archivo.add_command(label="Cerrar sesion", command=self.cerrarSesion, image=self.imgCerrarSesion,compound="left")
    def cerrarSesion(self):
        pass
    def salir(self):
        pass
    def actulizarDatos(self):
        query = f"SELECT *FROM Datos"
        self.Datos = {}

        for dato,descripcion in self.run_query(query):
            if "," in descripcion:
                self.Datos[dato] = descripcion.split(',')
            else:
                self.Datos[dato] = descripcion
        query = f"SELECT *FROM DatosTemp"
        for dato,descripcion in self.run_query_temp(query):
            if "," in descripcion:
                self.Datos[dato] = descripcion.split(',')
            else:
                self.Datos[dato] = descripcion
        self.config_impresoras = {
            "cierre de dia": self.Datos["cierre de dia"],
            "reportes": self.Datos["reportes"],
            "cocina": self.Datos["cocina"],
            "recepcion": self.Datos["recepcion"],
            "recibo-caja": self.Datos["recibo-caja"]
        }
        self.Datos["Empresa"] = self.agregar_salto_linea_frase(self.Datos["Empresa"],17)
        #lectura_barra.DEFAULT_SERIAL_PORT = self.Datos["Lector barra"]

    def configImpresoras(self):
        try: 
            self.ventanaConfigueracionImpresoras.destroy()
        except:
            pass
        self.ventanaConfigueracionImpresoras = Toplevel(self.ventana1)
        frame = LabelFrame(self.ventanaConfigueracionImpresoras, text = "Configuración ", labelanchor="n",font=20)
        frame.pack(padx=5, pady=5)
        self.combobox_impresoras = {}
        self.cargar_impresoras()
        x = 0
        for i in self.config_impresoras:
            Label(frame, text = i.capitalize()).grid(row=x, column=0, padx=5,pady=5)
            self.combobox_impresoras[i] = ttk.Combobox(frame, state="readonly",values=self.listaImpresoras)
            self.combobox_impresoras[i].grid(row =x, column=1, padx=5,pady=5)
            if self.config_impresoras[i] != "":
                self.combobox_impresoras[i].set(self.config_impresoras[i])
            x = x+1          
        CrearBotones.Botones(frame,"Guardar",self.guardar_impresora,self.imgGuardar).grid(row=x,column=0,columnspan=2,sticky="we")
        CrearBotones.CenterWindow(self.ventanaConfigueracionImpresoras)
    def guardar_impresora(self, texto):
        for i in self.combobox_impresoras:
            if self.combobox_impresoras[i].get() != "":
                query = f"UPDATE DatosTemp Set descripcion = '{self.combobox_impresoras[i].get()}' where nombre = '{i}'"
                try:
                    self.run_query_temp(query)
                except Exception as e:
                    self.ventanaConfigueracionImpresoras.lift()
                    messagebox.showerror(title="Error de configuracion de impresora",message=f"Configuracion NO Guardad de {i.capitalize()}")
                    break
        
        self.ActualizarInterfazPedido()
        self.ventanaConfigueracionImpresoras.destroy()
    def crear_menu_config_impresoras(self):
        menu_impresoras = Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Configuracion", menu=menu_impresoras)
        menu_impresoras.add_command(label="Impresoras", command=self.configImpresoras, image=self.imgConfifImpresoras,compound="left")
    def cargar_impresoras(self):
        impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL + win32print.PRINTER_ENUM_CONNECTIONS, None, 1)
        self.listaImpresoras = [impresora[2] for impresora in impresoras] 
    def finalizarPedidosCXC(self):
        query = f"""UPDATE Pedido SET Activo  = '4' WHERE TipoPago = 'CXC'"""
        self.run_query(query)
        self.ActualizarInterfazPedido()   
    
        self.datosPorfectoTabla()
    
    def InterfazLogin(self):
        
        self.usuario = StringVar()
        self.contra = StringVar()
        self.usuario.set("Ingrese Usuario")
        self.contra.set("Ingrese Contraseña")
        self.tipoUsuario = IntVar()

        self.login = Frame(self.ventana1,
                           bd = 1,
                           bg = self.Datos["Fondo"],
                           relief="groove")
        self.login.pack(expand = 1,
                        pady=5)
        Label(self.login,
              text = "LOGIN",
              bg = self.Datos["Color de letra"],
              fg = self.Datos["Fondo"],
              font = (self.Datos["Tipo de letra"],25)).pack(
                                                fill = X,
                                                padx = 5,
                                                pady = 5)
        x = 1
        self.loginUsuarios = Frame(self.login)
        self.loginUsuarios.pack()
        for usu in self.Datos["Tipos Usuario"]:
            y = CrearBotones.radiobutton(self.loginUsuarios,usu,self.tipoUsuario,x,self.Datos, self.selec)
            x = x + 1
            y.pack(side = LEFT)
        self.tipoUsuario.set(1)
        self.loginEntradas = Frame(self.login)
        self.loginEntradas.pack(fill = X,padx=5)
        self.loginEntradasImagen = Frame(self.loginEntradas)
        self.loginEntradasImagen.pack(side = LEFT)

        Label(self.loginEntradasImagen,
              image = self.imgUsu).pack(pady=6,padx=5)
        Label(self.loginEntradasImagen,
              image = self.imgCon).pack(pady=6,padx=5)
        self.loginEntradasEntry = Frame(self.loginEntradas)
        self.loginEntradasEntry.pack(fill = X)
        self.IngresoUsuario = CrearBotones.entrada(self.loginEntradasEntry,self.usuario,self.Datos,"Ingrese Usuario")
        self.IngresoUsuario.select_range(0,"end")
        self.IngresoUsuario.focus()
        self.IngresoUsuario.pack(expand  =1,fill = X,pady=5,padx=5)
        self.IngresoContra = CrearBotones.entrada(self.loginEntradasEntry,self.contra,self.Datos,"Ingrese Contraseña",1)
        self.IngresoContra.pack(fill = X,pady=5,padx=5)
        self.continuar = CrearBotones.Botones(self.login,"Continuar",self.logiarse,self.imgContinuar)
        self.continuar.pack(fill=X, padx=5, pady=5)
        self.continuar.bind('<Return>', lambda e:self.logiarse("hola"))
        #tk.Button(self.login,text = "CONTINUAR",command = self.logiarse).grid(row = 4,column =0,columnspan=4,sticky=E+W)
        #self.ventana1.mainloop()
    def selec(self):
        if self.tipoUsuario.get()==3:
            self.loginEntradas.pack_forget()
            self.continuar.focus()
        else:
            self.loginEntradas.pack(after =self.loginUsuarios,fill = X,padx=5 )
    def logiarse(self,texto=""):
        if self.tipoUsuario.get()==2:
            
            query = f"""SELECT *FROM Usuarios WHERE usuario == '{self.usuario.get()}' and pass == '{self.contra.get()}' and tipoUsuario == {self.tipoUsuario.get()}"""
            try:
                if 1 == True:
                #if bool(self.run_query(query)) == True:
                    #messagebox.showinfo(message="bienvenido", title="Login")
                    self.permisos = False
                    self.login.destroy()
                    self.Hotel()
                else:
                    messagebox.showinfo(message="Usuario o Contraseña es incorrecta", title="Login")
            except Exception as e:
                print(e)
                messagebox.showinfo(message="Usuario o Contraseña es incorrecta", title="Login")
        elif self.tipoUsuario.get()==1:
            self.permisos = True
            self.login.destroy()
            self.menuArchivo()
            self.Hotel()
            self.Restaurante()
        else:
            self.permisos = False
            self.login.destroy()
            self.Restaurante()
            self.interzaTienda()
    def Centrar_Ventanas(self, ancho_ventana, alto_ventana, ventana):
        x_ventana = self.ancho // 2 - ancho_ventana // 2
        y_ventana = self.alto // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        ventana.geometry(posicion)
    def run_query(self,query,parameters = ()):
        base = self.baseDatos
        with sqlite3.connect(base) as conect:
            cursor = conect.cursor()
            cursor.execute(query,parameters)
            result = cursor.fetchall()
            conect.commit()
            return result
        
    def run_query_temp(self,query,parameters = ()):
        base = self.ruta_temporal
        with sqlite3.connect(base) as conect:
            cursor = conect.cursor()
            cursor.execute(query,parameters)
            result = cursor.fetchall()
            conect.commit()
            return result
    def run_queryColumnas(self,query):
        with sqlite3.connect(self.baseDatos) as conect:
            cursor = conect.cursor()
            cursor.execute(query)
            nombres_columnas = [columna[0].capitalize() for columna in cursor.description]
            conect.commit()
            return nombres_columnas
    def run_query_many(self,query,parameters = ()):
        with sqlite3.connect(self.baseDatos) as conect:
            cursor = conect.cursor()
            cursor.executemany(query,parameters)
            result = cursor.fetchall()
            conect.commit()
            return result
    def run_query_many_temp(self,query,parameters = ()):
        base = self.ruta_temporal
        with sqlite3.connect(base) as conect:
            cursor = conect.cursor()
            cursor.executemany(query,parameters)
            result = cursor.fetchall()
            conect.commit()
            return result
    def subirIcono(self,boton):
        ruta = filedialog.askopenfilename(title="Selecciona una imagen",filetypes=(("Archivos de imagen", "*.jpg *.jpeg *.png"),))
        self.subirIconoNuevoServicio(ruta,boton)
    def subirIconoNuevoServicio(self,ruta,boton):
        with open(ruta, "rb") as file:
            self.image_data = file.read()
            boton.cambiarIcono(PhotoImage(file=ruta))
    #################################  Configuracione de la Empresa  #############################################################
    def ventanaInterfazConfigEmpresa(self):
        try:
            self.ventanConfigEmpresa.destroy()
        except:
            pass
        self.ventanaConfigEmpresa = Toplevel(self.ventana1)
        # Sección de menú de botones
        self.frame_menu = ttk.Frame(self.ventanaConfigEmpresa)
        self.frame_menu.pack(side="left", padx=5, pady=10,fill="y")
        separador_horizonal = Separator(self.ventanaConfigEmpresa, orient="vertical")
        separador_horizonal.pack(fill="y",expand=True,side="left", padx=2, pady=10)
        
        btn_empresa = CrearBotones.Botones(self.frame_menu,"Empresa",self.cargar_datos_empresa,self.imgEmpresa)
        btn_empresa.pack(padx=5, pady=5, anchor="ne",fill="x")
        self.framesMenuConfig = {}
        self.menuConfigActivo = "Empresa"
        self.interfazBotonMenuConfigEmpresa()
    def interfazBotonMenuConfigEmpresa(self):
        # Sección para ingresar información
        frame_info = Frame(self.ventanaConfigEmpresa,bg="white")
        self.framesMenuConfig["Empresa"] = frame_info
        frame_info.pack(side="left", fill="both", expand=True, padx=2, pady=10)

        
        # Crear etiquetas y entradas
        self.datosEmpresa = {"Empresa": {"Icono":self.imgEmpresa,"entrada":StringVar()},
                        "Correo": {"Icono":self.imgCorreo,"entrada":StringVar()},
                        "Celular": {"Icono":self.imgCelular_24,"entrada":StringVar()},
                        "Nit": {"Icono":self.imgNit,"entrada":StringVar()},
                        "Direccion": {"Icono":self.imgDireccion,"entrada":StringVar()},}
        
        for i,texto in enumerate(self.datosEmpresa):
            self.datosEmpresa[texto]["entrada"].set(self.Datos[texto])
            etiqueta = Label(frame_info, text=f"{texto}", image=self.datosEmpresa[texto]["Icono"],compound="left",justify="left",anchor="w",bg="white")
            etiqueta.image =  self.datosEmpresa[texto]["Icono"]
            entrada = ttk.Entry(frame_info,textvariable=self.datosEmpresa[texto]["entrada"],width=35)
            etiqueta.grid(row=i,column=0,padx=2,pady=2,sticky="we")
            entrada.grid(row=i,column=1,padx=2,pady=2)
            
        # Botón para cargar base de datos
        self.btn_cargar_bd = ttk.Button(frame_info, text="Cargar base de datos*", command=self.cargar_base_datos, image=self.imgBaseDatos,compound="left")
        self.btn_cargar_bd.grid(row=i+1,column=0,columnspan=2, sticky="ew",padx=2,pady=2)
        
        # Botón para guardar
        self.btn_guardar = ttk.Button(frame_info, text="Guardar", command=self.guardar_datos_empresa,image=self.imgGuardar,compound="left")
        self.btn_guardar.grid(row=i+2,column=0,columnspan=2, sticky="ew",padx=2,pady=2)
        CrearBotones.CenterWindow(self.ventanaConfigEmpresa)
    def cargar_datos_empresa(self,texto):
        self.framesMenuConfig[self.menuConfigActivo].pack_forget()
        self.framesMenuConfig[texto].pack(side="left", fill="both", expand=True, padx=2, pady=10)
    def cargar_base_datos(self):
        pass
    def guardar_datos_empresa(self):
        if self.datosEmpresa["Empresa"]["entrada"].get() != "":        
            for i in self.datosEmpresa:
                self.Datos[i] = self.datosEmpresa[i]["entrada"].get()
                query = "UPDATE Datos SET descripcion = ? WHERE nombre = ?"
                self.run_query(query, (self.datosEmpresa[i]["entrada"].get(),i),0)
            
            messagebox.showinfo("Guardar Datos", "Datos de la empresa guardados correctamente.")
            self.ventanaConfigEmpresa.destroy()
        else:messagebox.showwarning("Campos obligatorios", "Por favor complete el nombre de la EMPRESA.")

    #################################  hotel  #############################################################
    def Hotel(self):
        self.cuaderno1.pack(fill='both',expand = 1)
        self.paginaHotel = Frame(self.cuaderno1,bg=self.Datos["Fondo"])
        self.paginaHotel.pack(fill='both',expand = 1)
        
        Interfaz_Hotel.HotelInterface(self.ventana1, self.paginaHotel, self.menu_principal)
        self.cuaderno1.add(self.paginaHotel, text="Hotel")
    ########################################   pedido   ######################################################
    def Restaurante(self):
        self.cuaderno1.pack(fill='both',expand = 1)
        self.crear_menu_config_impresoras()
        
        self.pagina2 = Frame(self.cuaderno1,bg=self.Datos["Fondo"])
        self.pagina2.pack(fill='both',expand = 1)
        #self.pagina2.bind_all('<Key>',self.NuevoMesero)
        self.cuaderno1.add(self.pagina2, text="Restaurante")
        self.funcionesRes = LabelFrame(self.pagina2,width = self.ancho)
        self.funcionesRes.pack(fill = Y,side = LEFT)
        
        self.funcionRestauranteActiva = "REPORTES"
        self.funcionesRestaurante()
        self.funcionPedidos()
        self.cargarpedidos()
        self.funcionReportes()
        self.ejecutarFunRes("PEDIDOS")
        
        
        #self.ventana1.bind("<F2>", self.verPedidosCXC)
    def verPedidosCXC(self):
        
        query = f"""UPDATE Pedido SET Activo  = '2' WHERE TipoPago = 'CXC' AND Fecha = '{self.Fecha}'"""
        self.run_query(query)
        self.ActualizarInterfazPedido()

    def OrganizarPedido(self,Ped):
        Orden = {}
        for des, i, item in zip(Ped, self.CaracPepidos, enumerate(Ped)):
            if item[0] > 6 and item[0] < 12:
                x = des.split('//')
                if i == "descripcion" or i == "SubCant":
                    y = []
                    for t in x:
                        y.append(t.split('/'))
                    Orden[i] = y
                else:
                    Orden[i] = x
            else:
                Orden[i] = des
        return Orden
    def OrganizarPedido1(self, Ped):
        Orden = {}
        for descripcion in self.CaracPepidos:
            Orden[descripcion] = []
        for descripcion,item in zip(self.CaracteristicaPepidos,Ped):
            Orden[descripcion] = item

        query = f"Select *from RegistroPedidos where Comanda = {Orden['Comanda']}"
        try:
            Articulos = self.run_query(query)
        except Exception as e:
            print(e)
        cantidad = []
        categoria = []
        pagos = []
        SubCant = []
        descripcion = []
        tempSubCant = []
        tempDescripcion = []
        Orden["Sumar"] = []
        for Articulo in Articulos:
            if Articulo[3] == "--":
                pagos.append(Articulo[8])
                cantidad.append(Articulo[6])
                categoria.append(Articulo[5])
                SubCant.append(tempSubCant)
                descripcion.append(tempDescripcion)
                tempSubCant = []
                tempDescripcion = []
            else:
                Sumar =[Articulo[6],Articulo[2],Articulo[5],Articulo[3]]
                tempSubCant.append(Articulo[6])
                tempDescripcion.append(Articulo[3])
                Orden["Sumar"].append(Sumar)
        Orden["descripcion"] = descripcion
        Orden["cantidad"] = cantidad
        Orden["SubCant"] = SubCant
        Orden["categoria"] = categoria
        Orden["pagos"] = pagos
        return Orden
    def cargarpedidos(self):
        query = "SELECT *FROM Pedido WHERE Activo =='1' or Activo =='2' or Activo =='0'"
        Pedidos = self.run_query(query)
        self.TotalOrdenes_1 = {}
        EnMesa =[]
        EnEspera =[]
        PorFinish =[]
        self.EtiquetaBalance ={}
        for Ped1 in Pedidos:
            #Orden = self.OrganizarPedido(Ped1)
            Orden = self.OrganizarPedido1(Ped1)
            if Orden["Activo"]==2:
                EnMesa.append(Orden["Comanda"])
            elif Orden["Activo"]==1:
                EnEspera.append(Orden["Comanda"])
            else:PorFinish.append(Orden["Comanda"])
            Orden["Pedido"]=Ped1
            self.TotalOrdenes_1[Ped1[0]]=Orden
            self.EtiBalance(Orden)

        self.PedOrganizados =[sorted(EnMesa,reverse = True),sorted(EnEspera,reverse = True),sorted(PorFinish,reverse = True)]

        self.TotalOrdenes = {}
        for Estados in self.PedOrganizados:
            for key in Estados:
                x = self.TotalOrdenes_1[key]
                self.TotalOrdenes[key] = PEDIDOS(self.EnMesa,x,self.Datos)
                #self.Organizar(self.TotalOrdenes[key].NuevoPedido,x)
        self.Organizar1()
        self.VerEtiBalance()
    def EtiBalance (self,orden):
        if orden["Activo"] in self.EtiquetaBalance:
            tempCat = self.EtiquetaBalance[orden["Activo"]]
        else:
            tempCat = {}
        for cat,i in zip(orden["categoria"],enumerate(orden["categoria"])):
            if cat in tempCat:
                tempArt = tempCat[cat]
            else:
                tempArt = {}
            descripcion = orden["descripcion"]
            SubCant = orden["SubCant"]
            for art,cant in zip(descripcion[i[0]],SubCant [i[0]]):
                if art in tempArt:
                    tempCant = int(tempArt[art])
                else:
                    tempCant = 0
                try:
                    tempArt[art] = tempCant+int(cant)
                except:
                    tempArt[art] = tempCant+0
                tempCat[cat] = tempArt
                self.EtiquetaBalance[orden["Activo"]] = tempCat
    def VerEtiBalance(self):
        Label(self.BalancePedidos,text = "BALANCE",bg=self.Datos["Color categoria"],fg = self.Datos["Fondo"],font =(self.Datos["Tipo de letra"],17)).pack(fill = "x",pady=5)
        try:
            self.Estado.destroy()
        except:
            pass
        self.Estado = Frame(self.BalancePedidos)
        self.Estado.pack(fill="both")
        ListEstado = [2,1,0]
        Fondos = [self.Datos["En mesa"],self.Datos["En espera"],self.Datos["Por finish"]]
        for keyEst,fondo in zip(ListEstado,Fondos):

            if keyEst in self.EtiquetaBalance:
                tempCat = self.EtiquetaBalance[keyEst]
                for keyCat in tempCat:
                    tempArt = tempCat[keyCat]

                    Label(self.Estado,text = f"►{keyCat}",bg=fondo,font =(self.Datos["Tipo de letra"],14),justify="left").pack(fill="x",anchor="w")
                    for keyArt in tempArt:
                        Articulos = Frame(self.Estado)
                        Articulos.pack(fill="x")
                        Label(Articulos,text = f"{keyArt}",font =(self.Datos["Tipo de letra"],12),justify="left").pack(side="left")
                        Label(Articulos,text = tempArt[keyArt],font =(self.Datos["Tipo de letra"],12),justify="left").pack(side="right")

    def Organizar1 (self):
        fila = 0
        X = int(self.ancho/250*0.8)
        for estados in self.PedOrganizados:
            x = 0
            for key in estados:
                pedido = self.TotalOrdenes[key].NuevoPedido
                pedido.grid(row = fila,column = x,padx=5,pady=5,sticky=N)
                if x+1 == X:
                    fila = fila + 1
                    x = 0
                else:
                    x = x+1
            fila = fila + 1
    def funcionesRestaurante(self):
        
        CrearBotones.Botones(self.funcionesRes,"PEDIDOS",self.ejecutarFunRes,self.imgPedidos).pack(padx=5,pady =5,fill = X)
        self.subMenu = Frame(self.funcionesRes)
        self.subMenu.pack(fill = X) 
        CrearBotones.Botones(self.subMenu,"MENU",self.ejecutarFunRes,self.imgMenu).pack(padx=5,fill = X)
        self.contenedorSubMenu = Frame(self.subMenu,bg="white")
        self.activarMenu= False
        CrearBotones.SubBotones(self.contenedorSubMenu,"Inventario",self.inventarioArticulos,self.imgInventario,11).pack(padx=10,pady=2,fill = X)

        CrearBotones.SubBotones(self.contenedorSubMenu,"Nuevo Articulo",self.nuevoArticulo,self.imgNew,11).pack(padx=10,pady=2,fill = X)

        CrearBotones.SubBotones(self.contenedorSubMenu,"Nueva Categoria",self.NuevaCategoria,self.imgCategoria,11).pack(padx=10,pady=2,fill = X)
        CrearBotones.SubBotones(self.contenedorSubMenu,"Editar Categoria",self.editarCategoriaInterfaz,self.imgRegistrar,11).pack(padx=10,pady=2,fill = X)

        CrearBotones.Botones(self.funcionesRes,"REPORTES",self.ejecutarFunRes,self.imgReporte).pack(padx=5,pady =5,fill = X)
        CrearBotones.Botones(self.funcionesRes,"PERSONAL",self.ejecutarFunRes,self.imgPersonal).pack(padx=5,pady =5,fill = X)
        if self.permisos:
            CrearBotones.Botones(self.funcionesRes,"CUENTAS",self.ejecutarFunRes,self.imgCuenta).pack(padx=5,pady =5,fill = X)
        self.FuncionesRestaurante = {}
    def funcionPedidos(self):
        try:
            self.cuadernoPedios.destroy()
        except:
            pass
        self.cuadernoPedios = Frame(self.pagina2)
        #self.cuadernoPedios.bind('<Key>',self.NuevoMesero)
        self.FuncionesRestaurante["PEDIDOS"] = self.cuadernoPedios
        #self.cuadernoPedios.pack(fill='both',expand = 1)
        self.cuadernoPedios.rowconfigure(0, weight=10)
        self.cuadernoPedios.columnconfigure(0, weight=9)
        self.cuadernoPedios.columnconfigure(1, weight=1)
        
        self.BalancePedidos = Frame(self.cuadernoPedios)
        self.IconoNuevoPedido = Frame(self.BalancePedidos)
        
        CrearBotones.BotonesImagenes(self.IconoNuevoPedido,self.imgMas,self.imgMas1,self.PedidoNuevo).pack(side="bottom")

        ventana = Frame(self.cuadernoPedios,bg="white")
        ventana.grid(row=0, column=0, sticky="nsew")
        self.BalancePedidos.grid(row=0, column=1, sticky="nsew")
        self.IconoNuevoPedido.pack(fill='y',side ="bottom",padx = 5,pady=5)
        self.scrollventanaPedido = AgregarScrollVerticar(ventana)
        self.scrollventanaPedido.canvas.config(bg="white")
        self.scrobollInterfazPedidos = self.scrollventanaPedido.frame
        self.EnMesa = Frame(self.scrobollInterfazPedidos,bg=self.Datos["Fondo"])
        self.EnMesa.pack(fill='both',expand = 1)
        self.EnMesa.bind_all('<Key>',self.NuevoMesero)
    def PedidoNuevo(self,texto=None):

        Pedido = Nuevo_Pedido()
    def ejecutarFunRes(self,texto):
        if texto == "MENU":
            if self.activarMenu:
                self.contenedorSubMenu.pack_forget()
                self.activarMenu = False

            else:
                self.contenedorSubMenu.pack(fill = "x")
                self.activarMenu = True
        else:
            if texto in self.FuncionesRestaurante:
                self.FuncionesRestaurante[self.funcionRestauranteActiva].pack_forget()
                self.funcionRestauranteActiva = texto
                self.FuncionesRestaurante[texto].pack(fill="both",expand=True)
        
    def crearlistaCajabox(self,query):
        listas = self.run_query(query)
        lista1 = []
        lista = {}
        for i in listas:
            lista1.append(i[1])
            lista[i[1]]=i[2]
        lista[""]=""
        salida ={"lista":lista1,"abreviacion":lista}
        return salida
    def pasarapedidos(self):
        query = "SELECT *FROM Pedidos"# where #Comanda = '10'")
        conect = sqlite3.connect("Base.s3db")
        cursor = conect.cursor()
        cursor.execute(query)
        Pedido = cursor.fetchall()
        conect.commit()
        conect.close()
        parameters = []
        Pedidos = []

        for Ped in Pedido:
            Orden = self.OrganizarPedido(Ped)
            listaPedidos = (
                Orden["Comanda"],
                Orden["Fecha"],
                Orden["Mesero"],
                Orden["Mesa"],
                Orden["Hora"],
                Orden["TipoCliente"],
                Orden["cliente"],
                Orden["Total"],
                Orden["TipoPago"],
                Orden["observaciones"],
                Orden["Activo"])
            Pedidos.append(listaPedidos)
            for Categoria,Cantidad,Pagos in zip(enumerate(Orden["categoria"]),Orden["cantidad"],Orden["pagos"]):
                codigoCategoria = self.run_query(f"SELECT Codigo From Categorias where Descripcion = '{Categoria[1]}'")[0][0]
                for articulo,cantidad in zip(Orden["descripcion"][Categoria[0]],Orden["SubCant"][Categoria[0]]):

                    codigoArticulo = self.run_query(f"SELECT Codigo, Valor From ArticulosCategorias where Categoria = '{codigoCategoria}' and Descripcion = '{articulo}'")
                    Precio = int(cantidad)*int(codigoArticulo[0][1])
                    lista = (Orden["Comanda"],Orden["Fecha"],codigoArticulo[0][0],articulo,codigoCategoria,Categoria[1],int(cantidad),int(codigoArticulo[0][1]),Precio)
                    parameters.append(lista)
                lista = (Orden["Comanda"],Orden["Fecha"],"--","--",codigoCategoria,Categoria[1],Cantidad,0,Pagos)
                parameters.append(lista)
        self.run_query_many("INSERT INTO RegistroPedidos Values (?,?,?,?,?,?,?,?,?)",parameters)
        self.run_query_many("INSERT INTO Pedido Values (?,?,?,?,?,?,?,?,?,?,?)",Pedidos) 
    def ordenar_lista(self,datos,i,j,k,desendente = True):
        datos_ordenados = sorted(datos, key=lambda x: (x[i], x[j], x[k]), reverse=desendente)
        return datos_ordenados
    def imprimir_desde_web(self, id, accion):
        print(id, type(id))
        print(accion, type(accion))
        if id in self.TotalOrdenes:
            print(self.TotalOrdenes[id])
            if accion=="Recepcion":
                self.TotalOrdenes[id].imprimir_Recep()
            else:
                self.TotalOrdenes[id].imprimir()
            return True
        else:
            print(f"❌ Error: No se encontró el pedido con ID {id}")
    def enviar_categorias_platos_web(self):
        self.Menu_web = {}
        query = "SELECT * FROM Categorias ORDER BY ordenar ASC"
        self.listaCategorias = self.run_query(query)
        for categoria in self.listaCategorias:
            query = f"SELECT *FROM ArticulosCategorias WHERE Categoria == '{categoria[0]}'"
            Platos = self.run_query(query)
            articulos = {"Codigo":categoria[0],
                         "Platos":{}}
            for plato in Platos:
                articulos["Platos"][plato[3]] = {"codigo":plato[1],
                                                                "precio":plato[4]}

            self.Menu_web[categoria[1]] = articulos
        """
        for categoria in self.Menu_web:
            print(f"{categoria.center(20," ")}:\tCodigo: {self.Menu_web[categoria]["Codigo"]}")
        
            for plato in self.Menu_web[categoria]["Platos"]:
                print(f"\t{plato}\tCodigo: {self.Menu_web[categoria]["Platos"][plato]["codigo"]}")
                print(f"\t\t\tPrecio: {self.Menu_web[categoria]["Platos"][plato]["precio"]}")
        """
        return self.Menu_web
    def enviar_pedidos_web(self):
        return self.TotalOrdenes_1        

###################     Teinda        ##################################

    def interzaTienda(self):
        self.pagina3 = Frame(self.cuaderno1,bg=self.Datos["Fondo"])
        self.pagina3.pack(fill='both',expand = 1)
        self.cuaderno1.add(self.pagina3, text="Tienda")
        self.cuaderno1.bind("<<NotebookTabChanged>>", self.cargar_interfaz_tienda)

    def cargar_interfaz_tienda(self, event):
        pestaña_actual = self.cuaderno1.tab(self.cuaderno1.select(), "text")  # Obtener el nombre de la pestaña activa
        if pestaña_actual == "Tienda":
            self.abrir_interfaz_tienda()

    def abrir_interfaz_tienda(self):
        # Aquí cargas la interfaz de la tienda
        print("Interfaz de Tienda cargada.")
        InterfazPrincipal(self.pagina3, self.menu_principal, self.ventana1)

########################################################################
########################################################################
################     Nuevo Mesero   ####################################
    def Cierre_Dia(self,texto=None):
        otras = [self.EntryBarRest.get(),self.EntryArte.get(),self.EntryCholo.get()]
        parametro = PDF.CrearCierreDia(self.cierrePedidos,self.Fecha,self.Datos,self.cosecutivo,otras,self.Transferencia)
        self.run_query("INSERT INTO Cierre_Dia values (NUll,?,?,?,?,?,?,?,?)",parametro)
        self.ventanaCierreDia1.destroy()
        self.ActualizarInterfazPedido()
    def NuevoMesero(self,event):
        
        if event.keysym =="F1":
            self.finalizarPedidosCXC()

        if event.keysym =="F2":
            self.verPedidosCXC()
        if event.keysym == "F5":
            self.ActualizarInterfazPedido()
        if event.keycode == 82 and event.char == "\x12" and event.keysym == "r":
            PDF.CrearReporte(self.Datos,self.EtiquetaBalance)
        if event.keycode == 68 and event.char == "\x04" and (event.keysym == "d"):
            query = f"SELECT *FROM Pedido WHERE Activo != '5' AND TipoPago != 'CXC'"
            self.cierrePedidos = self.run_query(query)
            if len(self.cierrePedidos)>0:
                self.ventanaCierreDia1 = Toplevel(self.ventana1)
                frame = Frame(self.ventanaCierreDia1)
                frame.pack()
                frame1 = Frame(self.ventanaCierreDia1)
                frame1.pack(fill="both",side = "bottom")
                self.ventanaCierreDia = AgregarScrollVerticar(self.ventanaCierreDia1)
                self.ventanaCierreDia.canvas.config(width=25)
                Label(self.ventanaCierreDia1,text = "Cierre de Día",font = 30).pack(pady=0,padx=5)
                Label(self.ventanaCierreDia1,text = "Vista Previa",font = 30).pack(pady=0,padx=5)
                Label(self.ventanaCierreDia1,text = "Ped\tMesero\tValor",font = 30).pack(pady=0,padx=5)
                self.cosecutivo = len(self.run_query("SELECT *FROM Cierre_Dia"))
                Total=0
                self.Transferencia = 0
                for pedido in self.cierrePedidos:
                    trans = self.run_query(f"select sum(Valor) from PagosTransferencias where Comanda = '{pedido[0]}'")
                    icono = "#"
                    if trans[0][0] != None:
                        icono = "⁕"
                        self.Transferencia = self.Transferencia +int(trans[0][0])
                    Label(self.ventanaCierreDia1,text = f"{icono} {pedido[0]}\t{pedido[2]}\t{'$ {:,}'.format(int(pedido[7]))}",font=25).pack(pady=5,padx=5)
                    Total = Total + int(pedido[7])
                Label(frame1,text = f"\tSubTotal\t{'$ {:,}'.format(Total)}'",font=25).pack(pady=5,padx=5)
                frame2 = Frame(frame1)
                frame2.pack()
                Label(frame2,text = f"Bar Restaurante",font=25).grid(row=0,column=0)
                Label(frame2,text = f"Artesanias",font=25).grid(row=1,column=0)
                Label(frame2,text = f"Chocolate y Cafe",font=25).grid(row=2,column=0)
                #self.sumar = CrearBotones.Botones(frame2,"Sumar",self.actulizarDatosCierredia,self.Datos)
                #self.sumar.grid(row=3,columnspan = 2,column=0,sticky="we",padx=5,pady =5)

                self.EntryBarRest = StringVar()
                self.EntryArte = StringVar()
                self.EntryCholo = StringVar()
                self.EntryTotal = StringVar()
                self.EntryTotal.set(Total)
                self.entradaBar = CrearBotones.entrada(frame2,self.EntryBarRest,self.Datos,"Valor")
                self.entradaBar.grid(row=0,column=1)
                self.entradaArt = CrearBotones.entrada(frame2,self.EntryArte,self.Datos,"Valor")
                self.entradaArt.grid(row=1,column=1)
                self.entradaCho = CrearBotones.entrada(frame2,self.EntryCholo,self.Datos,"Valor")
                self.entradaCho.grid(row=2,column=1)
                self.entradaBar.bind("<KeyRelease>",self.actulizarDatosCierredia)
                self.entradaArt.bind("<KeyRelease>",self.actulizarDatosCierredia)
                self.entradaCho.bind("<KeyRelease>",self.actulizarDatosCierredia)
                frame3 = LabelFrame(frame1,text="")
                frame3.pack(padx=5,pady=5,fill="x")
                Label(frame3,text = f"Total:",font=25).grid(row=0,column=0,sticky="we")
                Label(frame3,text = f"Efectivo:",font=25).grid(row=1,column=0,sticky="we")
                Label(frame3,text = f"Transferencia:",font=25).grid(row=2,column=0,sticky="we")

                self.labelTotalCierredia = Label(frame3,text = f"{'$ {:,}'.format(int(self.EntryTotal.get()))}",font=25)
                self.labelTotalCierredia.grid(ipadx=50,row=0,column=1)
                self.labelefectivoCierredia = Label(frame3,text = f"{'$ {:,}'.format(int(self.EntryTotal.get()) - self.Transferencia)}",font=25)
                self.labelefectivoCierredia.grid(row=1,column=1)
                Label(frame3,text = f"{'$ {:,}'.format(self.Transferencia)}",font=25).grid(row=2,column=1)
                self.imprimir = CrearBotones.Botones(frame1,"Imprimir",self.Cierre_Dia,self.imgImprimir)
                self.imprimir.pack(padx=5,pady =5,fill="x")
                self.imprimir.bind('<Return>', self.Cierre_Dia)
                
            else:
                messagebox.showinfo(message="Cierre de dia Vacio", title="Cierre de dia")
                
        if event.keycode == 78 and event.char == "\x0e" and event.keysym == "n":
            self.PedidoNuevo()
        if event.keycode == 77 and event.char == "\r" and event.keysym == "m":
            mesero = NuevoMesero()   
    def actulizarDatosCierredia(self,e =None):
        lista = [self.EntryBarRest,self.EntryArte,self.EntryCholo]
        total = 0
        for i in lista:
            try:
                total = int(i.get())+total                
            except:
                pass
        self.labelTotalCierredia.config(text = f"{'$ {:,}'.format(int(self.EntryTotal.get())+ total)}")
        self.labelefectivoCierredia.config(text = f"{'$ {:,}'.format(int(self.EntryTotal.get())+ total - self.Transferencia)}")
    def GuardarNuevoMesero(self,texto):
        if self.VariableNuevoMesero[0].get() != self.EntradasNuevoMesero[0] and self.VariableNuevoMesero[2].get() != self.EntradasNuevoMesero[2] and self.VariableNuevoMesero[3].get() != self.EntradasNuevoMesero[3] :
            if self.VariableNuevoMesero[1].get()=="" or self.VariableNuevoMesero[1].get()== "Segundo Nombre":
                self.VariableNuevoMesero[1]="."
            else:
                self.VariableNuevoMesero[1] = f".{self.VariableNuevoMesero[1].get()}."
            query = "SELECT *FROM Meseros"
            lista = len(self.run_query(query))
            if lista<10:
                codigo = f"D0{lista+1}"
            else:
                codigo =f"D{lista+1}"
            nombre = f"{self.VariableNuevoMesero[0].get()}{self.VariableNuevoMesero[1]}{self.VariableNuevoMesero[2].get()}"
            runquery = [codigo,nombre,self.VariableNuevoMesero[0].get(),self.VariableNuevoMesero[3].get(),"Y",0]
            try:
                query = "INSERT INTO Meseros values(?,?,?,?,?,?)"
                self.run_query(query,runquery)
                messagebox.showinfo(message=f"Mesero Guardado con codigo: {codigo}", title="Nuevo Mesero Guardado")
                self.ventanaNuevoMesero.destroy()
            except:
                messagebox.showinfo(message=f"Intente con otro pin", title="Nuevo Mesero Guardado")
        else:
            messagebox.showinfo(message="Datos incompletos", title="Nuevo Mesero")
            self.ventanaNuevoMesero.deiconify()
            self.entradas[0].focus()
########################################################################
##############     Menu Restaurante ####################################        
    def inventarioArticulos(self,texto=None):
        self.ventanaRegistroEntrada = False
        try:
            self.inventarioMenu.destroy()
            self.ventanaRegistroEntrada = True
        except:
            pass
        
        self.inventarioMenu = Toplevel(self.ventana1)

        self.inventarioMenu.geometry(f"400x{self.alto-100}+0+0")
        datos = self.run_query("select * from Articulos order by Prioridad")
        datos = self.ordenar_lista(datos,3,0,1,False)
        print(datos[1])
        nombre_columnas = ["Cod", "Descripcion", "Cant", "Clasificación"]
        ancho_columnas =[30,150,30,90]
        self.tabla_listado_articulos = CrearBotones.Tabla_filtro(self.inventarioMenu,datos,nombre_columnas,ancho_columnas,self.editar_articulo,"Ariticulo",self.imgContinuar)
        self.tabla_listado_articulos.boton_seleccionar.config(text="Editar Ariticulo")
        botonRegistrar = CrearBotones.Botones(self.tabla_listado_articulos.frame_seleccionar,"Registrar Entrada",self.InterfazRegistroEntrada,self.imgGuardar)
        botonRegistrar.pack(side="left",fill="both", expand=True, pady=5, padx=5)
        botonRegistrar.config(command=partial(self.InterfazRegistroEntrada, self.tabla_listado_articulos.treeview,self.tabla_listado_articulos.ventana))
        CrearBotones.CenterWindow(self.inventarioMenu)
        self.inventarioMenu.protocol("WM_DELETE_WINDOW", self.cerrarVentanaInventario)
    def cerrarVentanaInventario(self):
        if tk.messagebox.askokcancel("Cerrar ventana", "¿Estás seguro de que quieres cerrar la ventana?"):
            self.inventarioMenu.destroy()
            try:
                self.AriculoMenu.destroy()
            except:
                pass
            try:
                self.ventanaRegistroEntrada.destroy()
            except:
                pass

    def nuevoArticulo(self,texto=None):
        self.Id = StringVar()
        self.Id.set("")
        self.categoriasSeleccionada = {}
        self.AriculoMenu = Toplevel(self.ventana1)

        self.AriculoMenu.lift(self.ventana1)
        self.contenedorFrameEditarArticulo = LabelFrame(self.AriculoMenu,text=f"Articulo {self.Id.get()}",font = ("Times New Roman",20), labelanchor="n")
        self.contenedorFrameEditarArticulo.pack(fill="both",expand=True)
        self.entradaAriculoNombre = StringVar()
        self.entradaAriculoNombre.set("Nombre de Articulo")
        self.entradaNombre = CrearBotones.entrada(self.contenedorFrameEditarArticulo,self.entradaAriculoNombre,self.Datos,"Nombre de Articulo")
        self.entradaNombre.grid(padx=5,pady=5,row =0,column=0,columnspan=2,sticky="we")
        frameClasificacion = LabelFrame(self.contenedorFrameEditarArticulo,text = "Clasificación",font = ("Times New Roman",15), labelanchor="n")
        framePriopiridad = LabelFrame(self.contenedorFrameEditarArticulo,text = "Prioridad",font = ("Times New Roman",15), labelanchor="n")
        frameClasificacion.grid(padx=5,pady=5,row =1,column=0,sticky="we")
        framePriopiridad.grid(padx=5,pady=5,row =1,column=1,sticky="we")
        self.articuloClasificacion = CrearBotones.ComboLista(frameClasificacion,self.Datos["Clasificacion"],self.Datos,5)
        self.articuloClasificacion.config(state="Normal")
        self.articuloPrioridad = CrearBotones.ComboLista(framePriopiridad,self.Datos["Prioridad"],self.Datos,5)
        self.articuloClasificacion.pack(pady=5,padx=5,fill="x")
        self.articuloPrioridad.pack(pady=5,padx=5,fill="x")
        frameAgregarCategoria = LabelFrame(self.contenedorFrameEditarArticulo,text="Agregar Categoria",font = ("Times New Roman",15), labelanchor="n")
        frameAgregarCategoria.grid(padx=5,pady=5,row =2,column=0,columnspan=2)
        listaCategorias = []
        for dato in self.run_query("select Codigo,Descripcion from Categorias"):
            listaCategorias.append(dato[1])
            self.categoriasSeleccionada[dato[1]]={"Codigo":dato[0],"Precio":""}
            self.categoriasSeleccionada[dato[0]]={"descripcion":dato[1]}
        self.entradaId = StringVar()
        self.entradaId.set("")
        entradaId = Label(frameAgregarCategoria,textvariable=self.entradaId,font = ("Times New Roman",15),width=3)
        entradaId.pack(pady=5,padx=5,side="left")
        self.nuevaCategoriaArticulo = CrearBotones.ComboLista(frameAgregarCategoria,listaCategorias,self.Datos,15)
        self.nuevaCategoriaArticulo.pack(pady=5,padx=5,fill="x",side="left")
        self.entradaArticuloPrecio = StringVar()
        self.entradaArticuloPrecio.set("Precio")
        self.entradaArticuloPrecio1 = CrearBotones.entrada(frameAgregarCategoria,self.entradaArticuloPrecio,self.Datos,"Precio")
        self.entradaArticuloPrecio1.config(width=6)
        self.entradaArticuloPrecio1.pack(pady=5,padx=5,fill="x",side="left")
        self.botonagregarCategoriaArticulo = CrearBotones.BotonesImagenes(frameAgregarCategoria,self.imgMas_24,self.imgMas1_24,self.agregarCategoria,[self.nuevaCategoriaArticulo,self.entradaArticuloPrecio,self.entradaId,1])
        self.botonagregarCategoriaArticulo.pack(side="left",pady=5,padx=5)
        frameListaCategoria = LabelFrame(self.contenedorFrameEditarArticulo,text="",bd=0)
        frameListaCategoria.grid(padx=5,pady=5,row =3,column=0,columnspan=2,sticky="nsew")
        F1 = AgregarScrollVerticar(frameListaCategoria)
        F1.canvas.config(width=300)
        self.frameListaCategoria = F1.frame
        self.guardarArticulo = CrearBotones.Botones(self.AriculoMenu,"Guardar",self.guardarNuevoArticulo,self.imgGuardar)
        self.guardarArticulo.pack(padx=5, pady=5,fill="x",side="bottom")
        try:
            ubic = self.inventarioMenu.geometry().split("+")
            self.AriculoMenu.geometry(f"338x{self.alto-300}+{int(ubic[1])-348}+{ubic[2]}")
        except:
            self.AriculoMenu.geometry(f"338x{self.alto-300}")
            CrearBotones.CenterWindow(self.AriculoMenu)
    def agregarCategoria(self,dato=None):
        if dato[3]==1:
            Articulo = dato[0].get()
            valor = dato[1].get()
            reg = dato[2].get()
        else:
            Articulo = dato[0]
            valor = dato[1]
            reg = dato[2]
        
        if Articulo!=None and valor!="Precio":
            try:
                if "frame" in self.categoriasSeleccionada[Articulo]:
                    self.categoriasSeleccionada[Articulo]["frame"].destroy()
                frame = LabelFrame(self.frameListaCategoria,text="")
                frame.grid(padx=5,pady=1,sticky="nsew")
                self.categoriasSeleccionada[Articulo]["frame"]=frame
                precio = '$ {:,}'.format(int(valor))
                self.categoriasSeleccionada[Articulo]["Precio"]=valor
                
                self.categoriasSeleccionada[Articulo]["Id"]=reg
                
                Label(frame,text=self.categoriasSeleccionada[Articulo]["Codigo"],font = ("Times New Roman",15)).pack(side="left",pady=2,padx=5)
                Label(frame,text=self.agregar_salto_linea_frase(Articulo,10),font = ("Times New Roman",15)).pack(side="left",pady=2,padx=5,fill="x",expand=True)
                Label(frame,text=precio,font = ("Times New Roman",15)).pack(side="left",pady=2,padx=5)
                self.botonEditarCategoriaArticulo = CrearBotones.BotonesImagenes(frame,self.imgEdita,self.imgEdita1,self.EditarCategoria,[Articulo,self.categoriasSeleccionada[Articulo]["Precio"],self.categoriasSeleccionada[Articulo]["Id"]])
                self.botonEditarCategoriaArticulo.pack(side="left",pady=5,padx=5)
                self.botonEditarCategoriaArticulo = CrearBotones.BotonesImagenes(frame,self.imgEliminar,self.imgEliminar1,self.EliminarCategoria,Articulo)
                self.botonEditarCategoriaArticulo.pack(side="left",pady=5,padx=5)
                lista = list(self.nuevaCategoriaArticulo["values"])
                lista.remove(Articulo)
                self.nuevaCategoriaArticulo.set("")
                self.entradaArticuloPrecio.set("")
                self.nuevaCategoriaArticulo["values"]= lista
                self.nuevaCategoriaArticulo.focus()

            except:
                messagebox.showinfo(message="Precio Dato incorrecto", title="Nuevo Articulo")
                self.entradaArticuloPrecio1.focus()
                self.AriculoMenu.lift(self.ventana1)
        else:
            messagebox.showinfo(message="Datos incompletos", title="Nuevo Articulo")
            self.AriculoMenu.lift(self.ventana1)
    def EliminarCategoria(self,Datos):
        self.categoriasSeleccionada[Datos]["frame"].destroy()
        self.categoriasSeleccionada[Datos]["Precio"] = ""
        lista = list(self.nuevaCategoriaArticulo["values"])
        lista.append(Datos)
        self.nuevaCategoriaArticulo.set("")
        self.entradaArticuloPrecio.set("")
        self.nuevaCategoriaArticulo["values"]= lista
        self.nuevaCategoriaArticulo.focus()
    def EditarCategoria(self,Datos):
        lista = list(self.nuevaCategoriaArticulo["values"])
        lista.append(Datos[0])
        self.nuevaCategoriaArticulo["values"]= lista
        self.nuevaCategoriaArticulo.set("")
        self.entradaArticuloPrecio.set("")
        self.nuevaCategoriaArticulo.focus()
        self.entradaId.set(Datos[2])
        self.nuevaCategoriaArticulo.set(Datos[0])
        self.entradaArticuloPrecio.set(Datos[1])
    def editar_articulo(self,tabla,ventana):
        try:
            selection = tabla.selection()[0]
            id = tabla.item(selection)["text"]
            datos = tabla.item(selection)["values"]
            self.nuevoArticulo()
            self.AriculoMenu.lift(self.inventarioMenu)
            self.Id.set(id)
            self.contenedorFrameEditarArticulo.config(text=f"Articulo {self.Id.get()}")
            self.entradaAriculoNombre.set(datos[0])
            self.articuloClasificacion.set(datos[2])
            self.articuloPrioridad.set(datos[3])
            self.datosAntiguos = datos
            articulos = self.run_query(f"select * from ArticulosCategorias where Codigo = '{id}'")
            for articulo in articulos:
                if articulo[2] in self.categoriasSeleccionada:
                    categoria = self.categoriasSeleccionada[articulo[2]]["descripcion"]
                    self.agregarCategoria([categoria,articulo[4],articulo[0],0])
            self.guardarArticulo.config(text="Editar")
            self.guardarArticulo.config(command = partial(self.editarNuevoArticulo,""))
        except:
            messagebox.showerror(title="Editar Articulos", message="Para continuar, seleccione un articulo de la lista.")
            self.inventarioMenu.lift(self.ventana1)
    def NuevaCategoria(self,texto = None):
        self.ventanaNuevaCategoria = Toplevel(self.ventana1)
        self.ruta_imagen = self.imgSubir
        frame = LabelFrame(self.ventanaNuevaCategoria,text="Nueva Categoria",labelanchor="n",bd=0,font=("Times New Roman",20))
        frame.pack(fill = "both",expand=True,padx=5,pady=5)
        self.entradaNuevaCategoria = StringVar()
        self.entradaNuevaCategoria.set("Ingrese Categoria")
        CrearBotones.entrada(frame,self.entradaNuevaCategoria,self.Datos,"Ingrese Categoria").pack(fill = "both",expand=True,padx=5,pady=5)
        self.botonSubirIcoCategoria = CrearBotones.Botones(frame,"Subir icono",self.subirIconoCategoria,self.imgSubir)
        self.botonSubirIcoCategoria.pack(fill = "both",expand=True,padx=5,pady=5)
        CrearBotones.Botones(frame,"Guardar",self.guardarNuevaCategoria,self.imgContinuar).pack(fill = "both",expand=True,padx=5,pady=5)
        CrearBotones.CenterWindow(self.ventanaNuevaCategoria)
        self.ventanaNuevaCategoria.attributes('-topmost', 1)
    def editarCategoriaInterfaz(self,texto = None):
        self.ventanaEditarCategoria = Toplevel(self.ventana1)
        self.image_data = None
        frame = LabelFrame(self.ventanaEditarCategoria,text="Editar Categoria",labelanchor="n",bd=0,font=("Times New Roman",20))
        frame.pack(fill = "both",expand=True,padx=5,pady=5)
        self.listaCategoria = self.run_query("select * From Categorias")
        self.dicCategorias ={}
        lista = []
        for i in self.listaCategoria:
            self.dicCategorias[i[1]] = {"icono":i[3],"codigo":i[0]}
            lista.append(i[1])
        self.listaCategorias = CrearBotones.ComboLista(frame,lista,self.Datos,20)
        self.listaCategorias.pack(fill = "x",expand=True,padx=5,pady=5)
        self.listaCategorias.bind('<<ComboboxSelected>>', self.on_combobox_select)
        self.entradaNuevaCategoria = StringVar()
        self.entradaNuevaCategoria.set("Ingrese Categoria")
        self.entradaEditarCategoria = CrearBotones.entrada(frame,self.entradaNuevaCategoria,self.Datos,"Seleccione la Categoria")
        self.entradaEditarCategoria.pack(fill = "both",expand=True,padx=5,pady=5)
        self.entradaEditarCategoria.config(state="readonly")
        self.botonSubirIcoCategoria = CrearBotones.Botones(frame,"icono",self.subirIconoCategoria,self.imgSubir)
        self.botonSubirIcoCategoria.pack(fill = "both",expand=True,padx=5,pady=5)
        self.botonSubirIcoCategoria.config(state="disable")
        self.btnEditarCategoria = CrearBotones.Botones(frame,"Editar",self.editarNuevaCategoria,self.imgRegistrar)
        self.btnEditarCategoria.pack(fill = "both",expand=True,padx=5,pady=5)
        self.btnEditarCategoria.config(state="disable")
        CrearBotones.CenterWindow(self.ventanaEditarCategoria)
        self.ventanaEditarCategoria.attributes('-topmost', 1)
    def on_combobox_select(self,event):
        selected_item = self.listaCategorias.get()
        self.entradaEditarCategoria.config(state="normal")
        self.entradaEditarCategoria.set_text(selected_item)
        self.botonSubirIcoCategoria.config(state="normal")
        self.btnEditarCategoria.config(state="normal")
        if self.dicCategorias[selected_item]["icono"] != None:
            self.image_data = self.dicCategorias[selected_item]["icono"]
            image = Image.open(io.BytesIO(self.dicCategorias[selected_item]["icono"]))
            photo = ImageTk.PhotoImage(image)
            self.botonSubirIcoCategoria.cambiarIcono(photo)
        else:
            self.botonSubirIcoCategoria.cambiarIcono(self.imgSubir)
    def editarNuevaCategoria(self,event):
        descripcion = self.entradaEditarCategoria.get()
        codigo = self.dicCategorias[self.listaCategorias.get()]["codigo"]
        icono = self.image_data
        self.run_query("UPDATE Categorias SET Descripcion = ?, icono = ? WHERE Codigo = ?",(descripcion,icono,codigo))
        self.ventanaEditarCategoria.destroy()
        messagebox.showinfo(message="Actulizado",title="Actulizar Categoria")
        self.editarCategoriaInterfaz()

    def subirIconoCategoria(self,texto =None):
        try:
            self.ventanaNuevaCategoria.attributes('-topmost', 0)
            self.ventanaEditarCategoria.attributes('-topmost', 0)
        except:
            pass
        self.subirIcono(self.botonSubirIcoCategoria)
        try:
            self.ventanaNuevaCategoria.attributes('-topmost', 1)
            self.ventanaEditarCategoria.attributes('-topmost', 1)
        except:
            pass
    def guardarNuevaCategoria(self,texto=None):
        if self.entradaNuevaCategoria.get() != "Ingrese Categoria":
            categoria = self.entradaNuevaCategoria.get().capitalize()
            x = len(self.run_query("select *from Categorias"))
            codigo = f"A{x}"
            try:
                self.run_query("INSERT INTO Categorias values (?,?,?,?)",(codigo,categoria,x,self.image_data))
                messagebox.showinfo(message="Categoria Guardada Exitosamente",title="Nueva Categoria")
                self.ventanaNuevaCategoria.destroy()
            except:
                messagebox.showerror(message="No fue posible guardar la categoria",title="Nueva Categoria")
                self.ventanaNuevaCategoria.lift(self.ventana1)
        else:
            messagebox.showinfo(message="Campo de categoria invalido",title="Nueva Categoria")
            self.ventanaNuevaCategoria.lift(self.ventana1)
    def guardarNuevoArticulo(self,texto = None):
        if self.entradaAriculoNombre.get() != "Nombre de Articulo" and self.articuloClasificacion.get() != None and self.articuloPrioridad.get() != None:
            parameters = (self.entradaAriculoNombre.get(),0,self.articuloClasificacion.get(),self.articuloPrioridad.get())
            if not self.run_query(f"select *from Articulos where Descripcion = '{self.entradaAriculoNombre.get()}' and  Gramos = '{self.articuloClasificacion.get()}' and Prioridad = '{self.articuloPrioridad.get()}'"):
                self.run_query("insert into Articulos values (Null,?,?,?,?)",parameters)
                elementos = self.run_query("select *from Articulos")
                Codigo = elementos[len(elementos)-1][0]
                listaCategoria =[]
                for datos in self.categoriasSeleccionada:
                    if "frame" in self.categoriasSeleccionada[datos]:
                        lista = (Codigo,self.categoriasSeleccionada[datos]["Codigo"],self.entradaAriculoNombre.get(),self.categoriasSeleccionada[datos]["Precio"])
                        listaCategoria.append(lista)
                if listaCategoria != None:
                    self.run_query_many("insert into ArticulosCategorias values (Null,?,?,?,?)",listaCategoria)
                    
                messagebox.showinfo(message="Articulo Guardado Exitosamente", title="Nuevo Articulo")
                self.AriculoMenu.destroy()
            else:
                messagebox.showinfo(message="Articulo ya esta registrado", title="Nuevo Articulo")
                self.AriculoMenu.lift(self.ventana1)
        else:
            messagebox.showinfo(message="Datos incompletos", title="Nuevo Articulo")
            self.AriculoMenu.lift(self.ventana1)
    def editarNuevoArticulo(self,texto = None):
        if self.entradaAriculoNombre.get() != "Nombre de Articulo" and self.articuloClasificacion.get() != None and self.articuloPrioridad.get() != None:
            parameters = (self.entradaAriculoNombre.get(),self.articuloClasificacion.get(),self.articuloPrioridad.get())
            ayuda = ["Nombre de Articulo","",""]
            columas =["Descripcion","Gramos","Prioridad"]
            if not self.run_query(f"select *from Articulos where Descripcion = '{self.entradaAriculoNombre.get()}' and  Gramos = '{self.articuloClasificacion.get()}' and Prioridad = '{self.articuloPrioridad.get()}'"):
                for antiguo,Nuevo,temp,column in zip(self.datosAntiguos,parameters,ayuda,columas):
                    if Nuevo != antiguo and Nuevo != temp:
                        self.run_query(f"UPDATE Articulos SET '{column}' = '{Nuevo}' WHERE Codigo =='{self.Id}'")
                
            else:
                elementos = self.run_query("select *from Articulos")
                Codigo = self.Id.get()
                listaCategoria =[]
                for datos in self.categoriasSeleccionada:

                    if "frame" in self.categoriasSeleccionada[datos]:
                        if self.categoriasSeleccionada[datos]["Id"]=="":
                            lista = (Codigo,self.categoriasSeleccionada[datos]["Codigo"],self.entradaAriculoNombre.get(),self.categoriasSeleccionada[datos]["Precio"])
                            listaCategoria.append(lista)
                        else:

                            cat = self.categoriasSeleccionada[datos]["Codigo"]
                            valor = self.categoriasSeleccionada[datos]["Precio"]
                            reg = self.categoriasSeleccionada[datos]["Id"]
                            self.run_query(f"UPDATE ArticulosCategorias SET Codigo = '{self.Id.get()}' WHERE Reg =='{reg}'")
                            self.run_query(f"UPDATE ArticulosCategorias SET Categoria = '{cat}' WHERE Reg =='{reg}'")
                            self.run_query(f"UPDATE ArticulosCategorias SET Descripcion = '{self.entradaAriculoNombre.get()}' WHERE Reg =='{reg}'")
                            self.run_query(f"UPDATE ArticulosCategorias SET Valor = '{valor}' WHERE Reg =='{reg}'")
                if listaCategoria != None:
                    self.run_query_many("insert into ArticulosCategorias values (Null,?,?,?,?)",listaCategoria)
                messagebox.showinfo(message="Articulo Editado Exitosamente", title="Nuevo Articulo")
                self.AriculoMenu.destroy()
                self.inventarioMenu.lift(self.ventana1)
        else:
            messagebox.showinfo(message="Datos incompletos", title="Nuevo Articulo")
            self.AriculoMenu.lift(self.ventana1)
    def InterfazRegistroEntrada(self, tabla, ventana):
        try:
            selection = tabla.selection()[0]
            self.IdArticuloReg = StringVar()
            self.IdArticuloReg.set(tabla.item(selection)["text"])
            datos = tabla.item(selection)["values"]
            if self.ventanaRegistroEntrada:
                self.registroArticulo.set(datos[0])
                self.frameRegistro.config(text=self.registroArticulo.get())
                self.cantidadRegistro.set(0)

            else:
                self.registroArticulo = StringVar()
                self.registroArticulo.set(datos[0])
                ubic = self.inventarioMenu.geometry().split("+")
                self.ventanaRegistroEntrada = Toplevel(self.ventana1)
                self.ventanaRegistroEntrada.protocol("WM_DELETE_WINDOW", self.ventanaRegistroEntradaCerrada)
                self.ventanaRegistroEntrada.geometry(f"200x{self.alto-300}+{int(ubic[1])+410}+{ubic[2]}")
                self.fechaRegistro = StringVar()
                self.fechaRegistro.set(self.Fecha)
                self.framefechaRegistro = LabelFrame(self.ventanaRegistroEntrada,text="Fecha",font= ("Times New Roman",20))
                self.framefechaRegistro.pack(fill="x",padx=5,pady=5)
                entradafecha = CrearBotones.entrada(self.framefechaRegistro,self.fechaRegistro,self.Datos,self.fechaRegistro.get())
                entradafecha.pack(fill="x",padx=5,pady=5)
                entradafecha.config(state="disable",justify="center")
                self.frameRegistro = LabelFrame(self.ventanaRegistroEntrada,text=self.registroArticulo.get(),font= ("Times New Roman",20))
                self.frameRegistro.pack(fill="x",padx=5,pady=5)
                Label(self.frameRegistro,text="Cantidad",font= ("Times New Roman",15)).pack(side="left",padx=5,pady=5)
                self.cantidadRegistro = IntVar()
                #
                entradaCantidad = CrearBotones.entrada(self.frameRegistro,self.cantidadRegistro,self.Datos,self.fechaRegistro.get())
                entradaCantidad.config(justify="center",width=5)
                entradaCantidad.pack(side="left",padx=5,pady=5)

                self.botonregistarEntradaInvArticulo = CrearBotones.BotonesImagenes(self.frameRegistro,PhotoImage(file="Imagenes/agregar.png"),PhotoImage(file="Imagenes/agregar1.png"),self.agregarRegistrarentrada,[self.fechaRegistro, self.IdArticuloReg,self.registroArticulo,self.cantidadRegistro])
                self.botonregistarEntradaInvArticulo.pack(side="left",pady=5,padx=5)

                frameListadoRegistro = LabelFrame(self.ventanaRegistroEntrada,text="")
                frameListadoRegistro.pack(fill="both",padx=5,pady=5,expand=True)
                F1 = AgregarScrollVerticar(frameListadoRegistro)
                F1.canvas.config(width=150,height=300)
                self.frameListadoRegistro = F1.frame
                self.filasRegEntradas = 1
                Label(self.frameListadoRegistro,text="Cod",font=("Times New Roman",15)).grid(row = 0,column =0)
                Label(self.frameListadoRegistro,text="Articulo",font=("Times New Roman",15)).grid(row = 0,column =1,sticky="we")
                Label(self.frameListadoRegistro,text="Cant",font=("Times New Roman",15)).grid(row = 0,column =2)
        except ZeroDivisionError as e:
            tb = traceback.TracebackException.from_exception(e)
            # Obtener la línea de código que causó la excepción
            line = tb.stack[0].line
            messagebox.showerror(title="Registro de Articulos", message="Para continuar, seleccione un articulo de la lista.")
            self.inventarioMenu.lift(self.ventana1)
    def agregarRegistrarentrada(self,dato=None):
        try:
            if int(dato[3].get())>0:
                Label(self.frameListadoRegistro,text=self.IdArticuloReg.get(),font=("Times New Roman",12)).grid(row = self.filasRegEntradas,column =0)
                Label(self.frameListadoRegistro,text=self.agregar_salto_linea_frase(dato[2].get(),8),font=("Times New Roman",12)).grid(row = self.filasRegEntradas,column =1)
                Label(self.frameListadoRegistro,text=dato[3].get(),font=("Times New Roman",12)).grid(row = self.filasRegEntradas,column =2)
                self.filasRegEntradas = self.filasRegEntradas+1
                self.run_query("insert into RegEntrada values(Null,?,?,?,?)",(self.fechaRegistro.get(),self.IdArticuloReg.get(),self.registroArticulo.get(),self.cantidadRegistro.get()))
                dato = self.run_query(f"select * from Articulos where Codigo = '{self.IdArticuloReg.get()}'")
                total = int(dato[0][2]) + int(self.cantidadRegistro.get())
                self.run_query(f"UPDATE Articulos set Cantidad = '{total}' where Codigo ='{self.IdArticuloReg.get()}'")
                datos = self.run_query("select * from Articulos order by Prioridad")
                datos = self.ordenar_lista(datos,3,0,1,False)
                temp = self.tabla_listado_articulos.filtro.get()
                self.inventarioArticulos()
                   
        except:
            messagebox.showinfo(message="Datos erroneos", title="Registro de entradas")
    def ventanaRegistroEntradaCerrada(self):
        self.ventanaRegistroEntrada.destroy()
        self.ventanaRegistroEntrada =False
######################  Reporte  ############################################
    def funcionReportes(self):
        try:
            self.cuadernoReporte.destroy()
        except:
            pass
        self.cuadernoReporte = Frame(self.pagina2)
        #self.cuadernoReporte.bind('<Key>',self.NuevoMesero)
        self.FuncionesRestaurante["REPORTES"] = self.cuadernoReporte
        #self.cuadernoReporte.pack(fill='both',expand = 1)
        self.cuadernoReporte.rowconfigure(0, weight=10)
        self.cuadernoReporte.columnconfigure(0, weight=10)

        ventana = Frame(self.cuadernoReporte)
        ventana.grid(row=0, column=0, sticky="nsew")
        
        self.scrollventanaReporte = AgregarScrollVerticar(ventana)
        self.scrobollInterfazReporte = self.scrollventanaReporte.frame
        self.cuadernoReportes = Frame(self.scrobollInterfazReporte)

        self.cuadernoReportes.pack(fill="both",expand=True)

        frame_lista_pedidos = Frame(self.cuadernoReportes, width=320, height=300)
        frame_lista_pedidos.grid(row=0,column=0,padx=5, pady=5, rowspan=2,sticky="wnes")
        subframe_1_1 = LabelFrame(frame_lista_pedidos,text = "",font = self.tamañoLabelFrame)
        
        self.frameFechaFiltrar = LabelFrame(subframe_1_1,text="Fecha",labelanchor='n',font = self.tamañoLabelFrame)
        self.frameFechaFiltrar.pack(fill="x")
        
        if self.permisos:
            lista = ["Hoy","Semana","Mes","Personalizada"]
        else:
            lista = ["Hoy","Semana"]
        self.filtroFecha = CrearBotones.ComboLista(self.frameFechaFiltrar,lista,self.Datos,20)
        self.filtroFecha.pack(fill="x",padx=5,pady=5)
        self.filtroFecha.bind("<<ComboboxSelected>>", self.seleccionComboFiltroFecha)

        self.contenedorfiltroFechasPersonalizadas = Frame(self.frameFechaFiltrar)
        tk.Label(self.contenedorfiltroFechasPersonalizadas, text="Fecha inicio",font = (self.Datos["Tipo de letra"],13)).pack(side="left")
        self.fechaInicio = DateEntry(self.contenedorfiltroFechasPersonalizadas, locale="es_ES", date_pattern="yyyy-mm-dd",font = (self.Datos["Tipo de letra"],12))
        self.fechaInicio.pack(side="left")
        self.fechaInicio.bind("<<DateEntrySelected>>", self.evento_apertura_dateentry)
                
        tk.Label(self.contenedorfiltroFechasPersonalizadas, text="Fin",font = (self.Datos["Tipo de letra"],13)).pack(side="left")
        
        self.fechaFin = DateEntry(self.contenedorfiltroFechasPersonalizadas, locale="es_ES", date_pattern="yyyy-mm-dd", state="disable",font = (self.Datos["Tipo de letra"],12))


        self.fechaFin.pack(side="left",padx=2)
        self.fechaFin.bind("<<DateEntrySelected>>", self.evento_apertura_dateentry_fin)

   
        # lista de añospara la Segunda Grafica de tendencia
        self.contenedorfiltroFechasPersonalizadasComparar = Frame(self.frameFechaFiltrar)
        Label(self.contenedorfiltroFechasPersonalizadasComparar,text="Año a comparar: ").pack(side="left")
        self.segundaTendeciaGraficaTiempo = CrearBotones.ComboLista(self.contenedorfiltroFechasPersonalizadasComparar,self.obtener_años(),self.Datos,20)
        self.segundaTendeciaGraficaTiempo.pack(side="left",padx=5,pady=5,fill="x")
        self.segundaTendeciaGraficaTiempo.bind("<<ComboboxSelected>>", self.agregarGrafica2Tiempo)


        # Aquí creas el treeview en subframe_1_1 con las columnas Comanda y Cliente
        self.tablaVerPedidos = CrearBotones.Tabla_filtro(subframe_1_1,[],["Comanda","Fecha", "Cliente", "Total"],[5,10,10,10],self.vistaPreviaPedidos,"Comanda",self.imgContinuar)

        frame_crear_menu = LabelFrame(frame_lista_pedidos,text = "",font = self.tamañoLabelFrame)

        subframe_1_1.pack(side="left", fill="y",anchor="nw",expand=True)
        frame_crear_menu.pack(side="left", fill="both", expand=True,anchor="nw")

        # Frame ventas- ineventarios
        self.graficoPastel = CrearBotones.GraficoPastel(self.cuadernoReportes,"Tipos de Pagos",xlabel=None, ylabel=None,ancho = 4, alto =4)
        self.graficoPastel.canvas.get_tk_widget().grid(row=2,column=0,padx=5, pady=5,columnspan=2)
        self.graficoBarrasArticulo = CrearBotones.GraficoBarras(self.cuadernoReportes,titulo="Platos",xlabel="Platos",ylabel="Cantidad",ancho=10)
        self.graficoBarrasArticulo.canvas.get_tk_widget().grid(row=0,column=1,padx=5, pady=5, sticky="nsew",columnspan=2,rowspan=2)
        self.graficoBarrasCategoria = CrearBotones.GraficoBarras(self.cuadernoReportes,titulo="Categorias",xlabel="Categorias",ylabel="Cantidad",ancho=8,alto=4)
        self.graficoBarrasCategoria.canvas.get_tk_widget().grid(row=2,column=2,padx=5, pady=5, sticky="nsew")
        self.graficoLineaTiempo = CrearBotones.GraficoLinea(self.cuadernoReportes,titulo="Tiempo VS Ventas",xlabel="Tiempo",ylabel="Ventas",ancho=9)
        self.graficoLineaTiempo.canvas.get_tk_widget().grid_remove() 
    def vistaPreviaPedidos(self,comanda, ventana):
        try:
            self.top = ventana
            seleccion = comanda.selection()[0]
            id = comanda.item(seleccion)["text"]
            datos = comanda.item(seleccion)["values"]

            query = f"SELECT *FROM Pedido WHERE Comanda = '{id}'"
            Pedido = self.run_query(query)[0]
            Orden = self.OrganizarPedido1(Pedido)
            try:
                self.ventanaPedidoVistaPrevia.destroy()
            except:
                pass
            self.ventanaPedidoVistaPrevia = Toplevel(self.ventana1)
            pedido = PEDIDOS(self.ventanaPedidoVistaPrevia,Orden,self.Datos,0)
            #pedido.verMasOpciones.desactivar_eventos()
            self.ventanaPedidoVistaPrevia.lift()
            CrearBotones.CenterWindow(self.ventanaPedidoVistaPrevia)
            pedido.NuevoPedido.grid(row = 0,column = 0,padx=5,pady=5)


        except IndexError as e:
            messagebox.showerror(title = "Comanda",message="Para continuar, seleccione una comanda.")
    def seleccionComboFiltroFecha(self, event):
        seleccion = self.filtroFecha.get()

        self.contenedorfiltroFechasPersonalizadas.pack_forget()
        self.contenedorfiltroFechasPersonalizadasComparar.pack_forget()
        if seleccion == "Hoy":
            self.obtenerDatosReportes(f"Fecha = DATE('now')","Hoy")
        elif seleccion == "Semana":
            self.obtenerDatosReportes(f"Fecha BETWEEN DATE('now', 'weekday 0', '-7 days') AND DATE('now')","Dias")
        elif seleccion == "Mes":
            self.obtenerDatosReportes(f"strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')","Dias")
        elif seleccion == "Personalizada":
            # Crear DateEntry para fechas personalizadas            
            self.contenedorfiltroFechasPersonalizadas.pack(fill="x", expand=True, padx=5, pady=5)       
    def evento_apertura_dateentry(self,e):
        self.fechaFin.config(state="readonly")
        fecha_seleccionada = self.fechaInicio.get_date()
        self.fechaFin.configure(mindate=fecha_seleccionada)
    def evento_apertura_dateentry_fin(self, e):
        self.fecha_inicio = self.fechaInicio.get_date()
        self.fecha_fin = self.fechaFin.get_date()
        # Convertir fecha_inicio a una cadena de texto en el formato Y-m-d
        fecha_inicio_str = self.fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_str = self.fecha_fin.strftime('%Y-%m-%d')

        # Luego puedes usar strptime con la cadena de texto
        fecha1 = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha2 = datetime.strptime(fecha_fin_str, '%Y-%m-%d')

        # Verificar si las fechas están en el mismo mes
        if fecha1.month == fecha2.month and fecha1.day == fecha2.day:
            tiempo  ="Hoy"
        elif fecha1.month == fecha2.month:
            tiempo  = "Dias"
        elif fecha1.month != fecha2.month:
            tiempo = "Mes"
        else:
            tiempo = "Año"
        consulta =f"Fecha BETWEEN '{self.fecha_inicio}' AND '{self.fecha_fin}'"
        self.obtenerDatosReportes(consulta,tiempo)
        if tiempo =="Dias" or tiempo =="Mes":
            self.contenedorfiltroFechasPersonalizadasComparar.pack(fill="x", expand=True, padx=5, pady=5)    
    def obtenerDatosReportes(self, consulta,tiempo):
        
        query = f"SELECT Comanda, Fecha, cliente, Total FROM Pedido WHERE {consulta}"
        lista = self.run_query(query)
        self.tablaVerPedidos.datos= lista
        self.tablaVerPedidos.actualizar_tabla()
        if self.permisos and tiempo == "Dias":
            query = f"""SELECT strftime('%d', Fecha) AS Dias, SUM(Total) AS total_mes
                    FROM Pedido
                    WHERE {consulta}
                    GROUP BY strftime('%d', Fecha)
                    ORDER BY strftime('%d', Fecha)
                """
            
            lista = self.run_query(query)
            
            lista1 = self.process_list(lista)            
            self.graficoLineaTiempo.xlabel = "DIAS"
            self.graficoLineaTiempo.graficar_datos(lista1)
            self.graficoLineaTiempo.canvas.get_tk_widget().grid(row=3,column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        elif self.permisos and tiempo == "Mes":
            query = f"""SELECT strftime('%m', Fecha) AS Dias, SUM(Total) AS total_mes
                    FROM Pedido
                    WHERE {consulta}
                    GROUP BY strftime('%m', Fecha)
                    ORDER BY strftime('%m', Fecha)
                """
            lista = self.run_query(query)
            self.graficoLineaTiempo.titulo = f"AÑO {lista[0][0][:2]}" 
            self.graficoLineaTiempo.xlabel = "MESES"
            self.graficoLineaTiempo.graficar_datos(lista)
            self.graficoLineaTiempo.canvas.get_tk_widget().grid(row=3,column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        else:
            self.graficoLineaTiempo.canvas.get_tk_widget().grid_remove()
            

        query = f"""SELECT TipoPago, COUNT(*) as cantidad
                    FROM Pedido
                    WHERE {consulta}
                    GROUP BY TipoPago
                """
        lista = self.run_query(query)
        print(lista)
        self.graficoPastel.graficar_datos(lista)

        query  = f"""SELECT DescripcionCategoria, SUM(Cantidad) as cantidad
                    FROM RegistroPedidos
                    WHERE {consulta} and
                    DescripcionArticulo = '--'
                    GROUP BY DescripcionCategoria
                    ORDER BY Cantidad DESC
                """
        lista = self.run_query(query)
        self.graficoBarrasCategoria.graficar_datos(lista)
        


        query  = f"""SELECT DescripcionArticulo, SUM(Cantidad) as cantidad
                    FROM RegistroPedidos
                    WHERE {consulta} and
                    DescripcionArticulo != '--'
                    GROUP BY CodigoArticulo
                    ORDER BY Cantidad DESC
                """
        lista = self.run_query(query)
        lista = self.graficoBarrasArticulo.clasificar_datos(lista,15,0.95)
        self.graficoBarrasArticulo.graficar_datos(lista)

        
        #self.graficoLineaTiempo.canvas.get_tk_widget().grid(row=3,column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
    def process_list(self, lista):
        # Extract days and sales from the input list
        dias, ventas = zip(*lista)
        dias1 = [int(dia) for dia in dias]
        
        # Create a new list with missing days filled with zeros
        lista1 = [(dia, ventas[dias1.index(dia)]) if dia in dias1 else (dia, 0) for dia in range(int(str(self.fecha_inicio)[-2:]), int(str(self.fecha_fin)[-2:])+1)]
        
        return lista1
    
    def agregarGrafica2Tiempo(self,event):
        # Convertir las cadenas de fecha a objetos datetime
        
        fecha_inicio_str = self.fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_str = self.fecha_fin.strftime('%Y-%m-%d')
        # Convertir fecha_inicio a una cadena de texto en el formato Y-m-d
        fecha_inicio_obj = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin_obj = datetime.strptime(fecha_fin_str, "%Y-%m-%d")

        # Cambiar el año de las fechas
        nuevo_anio = int(self.segundaTendeciaGraficaTiempo.get())
        fecha_inicio_mod = fecha_inicio_obj.replace(year=nuevo_anio)
        fecha_fin_mod = fecha_fin_obj.replace(year=nuevo_anio)

        # Formatear las fechas al formato "%Y-%m-%d"
        fecha_inicio_str = fecha_inicio_mod.strftime("%Y-%m-%d")
        fecha_fin_str = fecha_fin_mod.strftime("%Y-%m-%d")

        consulta =f"Fecha BETWEEN '{fecha_inicio_str}' AND '{fecha_fin_str}'"
        
        # Verificar si las fechas están en el mismo mes
        if fecha_inicio_mod.month == fecha_fin_mod.month and fecha_inicio_mod.day == fecha_fin_mod.day:
            pass
        elif fecha_inicio_mod.month == fecha_fin_mod.month:
            query = f"""SELECT strftime('%d', Fecha) AS Dias, SUM(Total) AS total_mes
                    FROM Pedido
                    WHERE {consulta}
                    GROUP BY strftime('%d', Fecha)
                    ORDER BY strftime('%d', Fecha)
                """
            lista = self.run_query(query)
            lista1 = self.process_list(lista)
            self.graficoLineaTiempo.graficar_datos_2(lista1,nuevo_anio)
        else:
            query = f"""SELECT strftime('%m', Fecha) AS Dias, SUM(Total) AS total_mes
                    FROM Pedido
                    WHERE {consulta}
                    GROUP BY strftime('%m', Fecha)
                    ORDER BY strftime('%m', Fecha)
                """
            lista = self.run_query(query)
            self.graficoLineaTiempo.graficar_datos_2(lista,nuevo_anio)
    def obtener_años(self):
        # Obtener el año actual
        anio_actual = datetime.now().year
        
        # Crear una lista de años desde el año actual hasta 10 años atrás
        anios = [int(anio) for anio in range(anio_actual, anio_actual - 10, -1)]
        return anios
########################################################################
########################################################################
    def ActualizarInterfazPedido(self):
        self.Fecha = time.strftime("%Y-%m-%d") 
        self.actulizarDatos()

        position = self.scrollventanaPedido.vscrollbar.get()
        aplicacion1.funcionPedidos()
        aplicacion1.cargarpedidos()
        self.ejecutarFunRes("PEDIDOS")
        
        
        #self.funcionReportes()
        self.scrollventanaPedido.vscrollbar.set(position[0],position[1]+0.1)
        self.ventana1.after(2000,self.notificar_actualizacion())
########################################################################
    def agregar_salto_linea_frase(self,frase, longitud):
        palabras = frase.split()
        subcadenas = []
        subcadena_actual = palabras[0]
        for palabra in palabras[1:]:
            if len(subcadena_actual) + len(palabra) + 1 <= longitud:
                subcadena_actual += ' ' + palabra
            else:
                subcadenas.append(subcadena_actual)
                subcadena_actual = palabra
        subcadenas.append(subcadena_actual)
        return '\n'.join(subcadenas)
########################################################################
    def notificar_actualizacion(self):
        """Envía una notificación a Flask para actualizar las páginas web"""
        """Envía una notificación a Flask para actualizar las páginas web"""
        try:
            requests.post(f"http://{self.obtener_ip_servidor()}:5000/api/actualizar_pedidos")
            print("📢 Notificación enviada a Flask")
        except Exception as e:
            print("❌ Error al notificar actualización:", e)
class Administrador(Interfaz):
    pass
class PEDIDOS(Interfaz):
    def __init__(self,ENMESA,ORDEN,DATOS, C=1):
        self.ENMESA =ENMESA
        self.ORDEN = ORDEN
        self.DATOS = DATOS
        self.C = C
        self.validarSalidasPlatos = {}
        self.comando_editar = False
        self.imgImprimir = aplicacion1.imgImprimir
        self.NuevoPedido = Frame(self.ENMESA)
        self.NuevoPedido.bind_all('<Button-1>', self.selectPedido)
        self.menuPedido = Menu(self.NuevoPedido, tearoff = 0)
        self.menuPedido.add_command(label =" Cocina",command = self.imprimir, image=self.imgImprimir, compound="left")
        if self.ORDEN["Activo"]==2:
            self.Etiqueta = self.DATOS["En mesa"]
        elif self.ORDEN["Activo"]==1:
            self.Etiqueta = self.DATOS["En espera"]
        else:
            self.Etiqueta = self.DATOS["Por finish"]
        if self.ORDEN["TipoPago"] == "CXC":
            self.menuPedido.add_command(label =" Recepción",command = self.imprimir_Recep, image=self.imgImprimir, compound="left")
        
        if C ==1:
            self.menuPedido.add_command(label ="Descuento",command = self.descuentos)
            self.menuPedido.add_command(label ="Cancelar")
            self.menuPedido.add_separator()
            if self.ORDEN["Activo"]==2:
                self.menuPedido.add_command(label ="Entregado",command = self.Pasar_A_Finalizar)
                self.menuPedido.add_command(label ="Finalizar",command = self.Finalizar)
            elif self.ORDEN["Activo"]==1:
                self.menuPedido.add_command(label ="Pasar Mesa",command = self.Pasar_A_Mesa)
                self.menuPedido.add_command(label ="Entregado",command = self.Pasar_A_Finalizar)
                self.menuPedido.add_command(label ="Finalizar",command = self.Finalizar)
                self.menuPedido.add_separator()
                self.menuPedido.add_command(label ="Editar",command = self.EditarPedido)
            else:
                self.menuPedido.add_command(label ="Pasar Mesa",command = self.Pasar_A_Mesa)
                self.menuPedido.add_command(label ="Finalizar",command = self.Finalizar)

            self.subMenuPagos = Menu(self.menuPedido, tearoff = 0)
            for Medios in aplicacion1.run_query("select Abreviacion from MediosPagos"):    
                self.subMenuPagos.add_command(label = Medios[0], command = partial(self.cambiarPago,Medios[0]))
            self.menuPedido.add_cascade(label = "Medios de pagos", menu = self.subMenuPagos)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = f"{self.ORDEN['Comanda']}",
              bg = self.Etiqueta,
              font = (self.DATOS["Tipo de letra"],20,"bold")).grid(row = 0,column=0,columnspan=5,sticky=W+E)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = self.ORDEN["TipoCliente"],
              font = (self.DATOS["Tipo de letra"],15,"bold")).grid(row = 1,column=0,sticky=W+E)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = self.ORDEN["cliente"],
              font = (self.DATOS["Tipo de letra"],15,"bold")).grid(row = 1,column=1,columnspan=4,sticky=W+E)

        self.verMasOpciones = CrearBotones.LabelVermas(self.NuevoPedido,aplicacion1.imgHambur1,aplicacion1.imgHambur2,self.Vermas,self.verMAsClik,self.DATOS,30)
        self.verMasOpciones.grid(row = 0,column=5,rowspan= 3)
        Label(self.NuevoPedido,
              bd=0,
              relief="solid",
              text = "Mesa",
              font = (self.DATOS["Tipo de letra"],self.DATOS["TamCategoria"],"bold")).grid(row = 2,column=0,columnspan=3,sticky=W+E)
        self.NumeroDeMesa =  IntVar()
        self.NumeroDeMesa.set(self.ORDEN["Mesa"])
        Entry(self.NuevoPedido,bd=1,relief="solid",width=3,
              textvariable = self.NumeroDeMesa,
              font = (self.DATOS["Tipo de letra"],self.DATOS["TamCategoria"],"bold")).grid(row = 2,column=3)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = self.ORDEN["Hora"],
              font = (self.DATOS["Tipo de letra"],self.DATOS["TamCategoria"],"bold")).grid(row = 2,column=4)
        x = 3
        for cant,cate,pag,item in zip(self.ORDEN["cantidad"],self.ORDEN["categoria"],self.ORDEN["pagos"],enumerate(self.ORDEN["pagos"])):
            Label(self.NuevoPedido,bd=0,relief="solid",
                  text = str(cant),
                  font = (self.DATOS["Tipo de letra"],self.DATOS["TamCategoria"],"bold"),
                  bg = self.DATOS["Color categoria"],
                  fg = self.DATOS["Fondo"],
                  justify="right").grid(row = x,column=0,sticky=E,pady=2)
            Label(self.NuevoPedido,bd=0,relief="solid",
                  text = cate,
                  font = (self.DATOS["Tipo de letra"],self.DATOS["TamCategoria"],"bold"),
                  bg = self.DATOS["Color categoria"],
                  fg = self.DATOS["Fondo"]).grid(row = x,column=1,sticky=W+E,columnspan=4,ipadx=3)
            try:
                precio = '$ {:,}'.format(int(pag))
            except:
                precio = '$ {:,}'.format(0)
            Label(self.NuevoPedido,bd=0,relief="solid",width=7,
                  text = str(precio),
                  font = (self.DATOS["Tipo de letra"],self.DATOS["TamCategoria"],"bold"),
                  bg = self.DATOS["Color categoria"],
                  fg = self.DATOS["Fondo"]).grid(row = x,sticky=W+E,column=5,ipadx=5)
            x = x+1
            platos={}
            for subcant,articulo in zip(self.ORDEN["SubCant"][item[0]],self.ORDEN["descripcion"][item[0]]):

                Label(self.NuevoPedido,bd=1,relief="solid",
                      text = str(subcant),
                      font = (self.DATOS["Tipo de letra"],self.DATOS["TamArticulos"],"bold"),
                      fg = self.DATOS["Color categoria"]).grid(row = x,column=1,sticky=E,padx=2)
                variable = StringVar()
                variable.set("")
                CrearBotones.LabelArticulo(self.NuevoPedido,articulo,cate,self.sumar,self.DATOS).grid(row = x,column=2,columnspan=3,sticky=W,pady=3)
                label = Label(self.NuevoPedido,
                      textvariable = variable,
                      font = (self.DATOS["Tipo de letra"],int(self.DATOS["TamArticulos"])-4,"bold"),
                      fg = self.DATOS["Color categoria"])
                label.grid(row = x,column=5,sticky=W)

                platos[articulo]=[subcant,variable,label]
                x = x+1
            self.validarSalidasPlatos[cate] =platos


        Label(self.NuevoPedido,bd=0,relief="solid",
              text = self.ORDEN["Mesero"],
              font = (self.DATOS["Tipo de letra"],10)).grid(row = x+1,column=0,columnspan=4,sticky=W+E)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = self.ORDEN["TipoPago"],width=10,
              font = (self.DATOS["Tipo de letra"],self.DATOS["TamTotal"],"bold")).grid(row = x+2,column=0,columnspan=4,sticky=W+E)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = "TOTAL",
              font = (self.DATOS["Tipo de letra"],self.DATOS["TamTotal"])).grid(row = x+2,column=4)
        Label(self.NuevoPedido,bd=0,relief="solid",
              text = '$ {:,}'.format(int(self.ORDEN["Total"])),width=7,
              font = (self.DATOS["Tipo de letra"],self.DATOS["TamTotal"],"bold")).grid(row = x+2,column=5,sticky=W+E)
        if self.ORDEN["observaciones"]!='':
            X = self.ORDEN["observaciones"]
            Label(self.NuevoPedido,bd=0,relief="solid",
                  text = f"Observaciones:\n{X}",
                  bg = self.DATOS["Fondo"],
                  font = (self.DATOS["Tipo de letra"],8)).grid(row = x+4,column=0,columnspan=5,pady=3,sticky=N+W+S+E,padx=5)
    def cambiarPago(self, Medio):
        if Medio in "QR":
            self.InterfazPagosQr()
        else:
            self.actulizarMedioPago(Medio)
    def InterfazPagosQr(self):
            self.interfazePagosQr = Toplevel(aplicacion1.ventana1)
            label = LabelFrame(self.interfazePagosQr, text = "Pago Por\nTransferencia",labelanchor="n",bd=0,font=("Times New Roman",20))
            label.pack(padx=5, pady=5)
            Label(label,text = "Precio",font=("Times New Roman",15)).grid(row = 0,column = 0,padx=5,pady=5)
            self.precioPagoQR = StringVar()
            self.precioPagoQR.set(self.ORDEN["Total"])
            CrearBotones.entrada(label,self.precioPagoQR,aplicacion1.Datos,"Continuar").grid(row = 0,column = 1,padx=5 ,pady=5)
            boton = CrearBotones.Botones(label,"Continuar",self.agregarMedioPago,aplicacion1.imgContinuar)
            boton.grid(row = 1,columnspan=2,column = 0,padx=5 ,pady=5,sticky="we")
            #boton = CrearBotones.Botones()
    def actulizarMedioPago(self,Medio):
        query = f"UPDATE Pedido SET TipoPago = '{Medio}' WHERE Comanda =={self.ORDEN['Comanda']}"
        aplicacion1.run_query(query)
        aplicacion1.ActualizarInterfazPedido()
    def agregarMedioPago(self, texto):
        aplicacion1.run_query(f"insert into PagosTransferencias values(Null,?,?,?)",(self.ORDEN["Fecha"],self.ORDEN["Comanda"],self.precioPagoQR.get()))
        messagebox.showinfo(title="Medios de pagos", message="Pago Registrado")
        self.interfazePagosQr.destroy()
        self.actulizarMedioPago("QR")
    def sumar(self,co,articulo,categoria,event):

        if articulo in self.validarSalidasPlatos[categoria]:
            contador = self.validarSalidasPlatos[categoria][articulo][1].get()
            comparar = int(self.validarSalidasPlatos[categoria][articulo][0])
            try:
                contador=int(contador)

            except:
                contador = 0
            x = contador + co

            if  x >= comparar:
                self.validarSalidasPlatos[categoria][articulo][1].set(str(comparar))
                self.validarSalidasPlatos[categoria][articulo][2].configure(bg=self.DATOS["En mesa"])

            elif x <= 0:
                self.validarSalidasPlatos[categoria][articulo][1].set("")
                self.validarSalidasPlatos[categoria][articulo][2].configure(bg="SystemButtonFace")

            else:
                self.validarSalidasPlatos[categoria][articulo][2].configure(bg="SystemButtonFace")
                self.validarSalidasPlatos[categoria][articulo][1].set(str(x))
            #valor = ar
    def imprimir(self):
        if self.ORDEN['Activo'] == 1:
            self.Pasar_A_Mesa()
            aplicacion1.ActualizarInterfazPedido()
            time.sleep(1)
        if self.ORDEN['TipoPago']=="CXC":
            self.imprimir_Recep()
            time.sleep(1)
        try:
            PDF.crearPDF(self.DATOS,self.ORDEN)
        except:
            pass
    def imprimir_Recep(self):
        try:
            PDF.Recepcion(self.DATOS,self.ORDEN)
        except:
            pass
    def verMAsClik(self,event):
        self.menuPedido.delete(8)
        self.menuPedido.delete(8)
        if self.ORDEN["Activo"]!=1 and self.C == 1:
            self.menuPedido.add_command(label ="A Espera",command = self.Pasar_A_Espera)
            self.menuPedido.add_command(label ="Editar",command = self.EditarPedido)
            
        try:
            self.menuPedido.tk_popup(event.x_root, event.y_root)
        finally:
            self.menuPedido.grab_release()

    def Vermas(self,event):
        if self.ORDEN["Activo"]!=1 and self.C == 1:
            self.menuPedido.delete(8)
            self.menuPedido.delete(8)
        try:
            self.menuPedido.tk_popup(event.x_root, event.y_root)
        finally:
            self.menuPedido.grab_release()

        #self.NuevoPedido.place(x=Cx,y=Cy)
            
    def Pasar_A_Espera(self):
        query = f"UPDATE Pedido SET Activo = '1' WHERE Comanda =={self.ORDEN['Comanda']}"
        aplicacion1.run_query(query)
        aplicacion1.ActualizarInterfazPedido()
    def Pasar_A_Mesa(self):
        query = f"UPDATE Pedido SET Activo = '2' WHERE Comanda =={self.ORDEN['Comanda']}"
        aplicacion1.run_query(query)
        aplicacion1.ActualizarInterfazPedido()

    def Pasar_A_Finalizar(self):
        query = f"UPDATE Pedido SET Activo = '0' WHERE Comanda =={self.ORDEN['Comanda']}"
        aplicacion1.run_query(query)
        aplicacion1.ActualizarInterfazPedido()
    def Finalizar(self):
        query = f"UPDATE Pedido SET Activo = '4' WHERE Comanda =={self.ORDEN['Comanda']}"
        aplicacion1.run_query(query)
        if self.ORDEN['TipoPago'] != "CXC":
            query = f"UPDATE Pedido SET TipoPago = 'PAGO' WHERE Comanda =={self.ORDEN['Comanda']}"
            aplicacion1.run_query(query)
        aplicacion1.ActualizarInterfazPedido()

        #query = f"UPDATE Pedidos SET Activo = '2' WHERE Comanda =={self.ORDEN['Comanda']}"
        #self.run_query(query)
    def EditarPedido(self):

        editar = Nuevo_Pedido("Editar",self.ORDEN)
    def selectPedido(self,event):

        pass

    def descuentos(self):
        self.ventanaDescuento = Toplevel(aplicacion1.ventana1)
        self.ventanaDescuento.title(f"Descuento comanda {self.ORDEN['Comanda']}")
        self.Descripcion = StringVar()
        self.Total = StringVar()
        self.Pin = StringVar()
        self.Descripcion.set("Descripcion")
        self.Total.set("Total")
        self.Pin.set("Pin de autorizacion")
        Label(self.ventanaDescuento,text = "DESCUENTOS",font = 25).pack(expand  =1,fill = X,pady=5,padx=5)
        self.IngresoDecripcionDescuento = CrearBotones.entrada(self.ventanaDescuento,self.Descripcion,aplicacion1.Datos,"Descripción")
        self.IngresoDecripcionDescuento.pack(expand  =1,fill = X,pady=5,padx=5)
        self.IngresoDecripcionTotal = CrearBotones.entrada(self.ventanaDescuento,self.Total,aplicacion1.Datos,"Total de Descuento")
        self.IngresoDecripcionTotal.pack(expand  =1,fill = X,pady=5,padx=5)
        self.IngresoDecripcionDescuento = CrearBotones.entrada(self.ventanaDescuento,self.Pin,aplicacion1.Datos,"Pin de autorizacion",1)
        self.IngresoDecripcionDescuento.pack(expand  =1,fill = X,pady=5,padx=5)
        self.continuarMesero = CrearBotones.Botones(self.ventanaDescuento,"CONTINUAR",self.guardarDescuento,aplicacion1.imgContinuar,10)
        self.continuarMesero.pack(fill = X,padx=5,pady =5,side="bottom")
    def guardarDescuento(self,text = ""):
        query  = f"select *from Usuarios where pass= '{self.Pin.get()}'"
        contra = aplicacion1.run_query(query)
        if self.Descripcion.get()!="Descripcion" and self.Total.get()!="Total" and self.Pin.get() == contra[0][3]:
            nuevoPrecio = int(self.ORDEN["Total"]) - int(self.Total.get())
            query = f"UPDATE Pedido SET Total = '{nuevoPrecio}' WHERE Comanda =={self.ORDEN['Comanda']}"
            aplicacion1.run_query(query)
            parameters = (self.ORDEN['Comanda'],self.ORDEN['Fecha'],"Des",self.Descripcion.get(),"Des","Descuento",1,self.Total.get(),self.Total.get())

            if self.ORDEN['Activo'] == 1:
                tabbla = "TempRegistroPedidos"
            else:
                tabbla = "RegistroPedidos"
            query = f"INSERT INTO {tabbla} values(?,?,?,?,?,?,?,?,?)"
            aplicacion1.run_query(query,parameters)
            lista = aplicacion1.run_query(f"select * from {tabbla} WHERE Comanda =='{self.ORDEN['Comanda']}' and DescripcionCategoria = 'Descuento' and CodigoArticulo = '--'")
            precio = int(self.Total.get()) + int(lista[0][8])
            cant = int(lista[0][6])+1
            if lista:
                
                queryA = f"delete from {tabbla} WHERE Comanda =='{self.ORDEN['Comanda']}' and DescripcionCategoria == 'Descuento' and CodigoArticulo == '--'"
                aplicacion1.run_query(queryA)
            
            
            parameters1=(self.ORDEN['Comanda'],self.ORDEN['Fecha'],"--","--","Des","Descuento",cant,0,precio)
            aplicacion1.run_query(query,parameters1)
            self.ventanaDescuento.destroy()
            aplicacion1.ActualizarInterfazPedido()
class Nuevo_Pedido(Interfaz):
    def __init__(self,texto = "Normal",OrdenEditar ={}):
        self.texto= texto
        self.OrdenEditar = OrdenEditar
        self.CaracteristicaPepidos = aplicacion1.CaracteristicaPepidos
        self.Fecha = aplicacion1.Fecha
        self.Datos = aplicacion1.Datos
        self.imgUsu  = aplicacion1.imgUsu
        self.baseDatos = aplicacion1.baseDatos
        self.alto = aplicacion1.alto
        self.CaracPepidos = aplicacion1.CaracPepidos
        self.ventana2 = Toplevel(aplicacion1.ventana1)
        self.ventana2.title("Nuevo Pedido")
        #self.ventana2.resizable(0,0)
        #self.Centrar_Ventanas(1400, 800, self.ventana2)
        #self.ventana2.state('zoomed')
        self.ventana2.configure(bg=self.Datos["Fondo"])
        if texto == "Normal":
            self.loginInterfaz()
        else:
            self.Mesero = OrdenEditar["Mesero"]
            self.Interfaz_Nuevo_Pedido()
            self.ventana2.title(f"Editar pedido: {OrdenEditar['Comanda']}, Mesero: {self.Mesero}")
            for item in  OrdenEditar["Sumar"]:
                self.sumar(item[0],item[1],item[2],item[3])
            self.Pedido["observaciones"].insert("1.0", OrdenEditar["observaciones"])
            self.Pedido["Fecha"].set_date(OrdenEditar["Fecha"])
            if OrdenEditar["Mesa"] != "":
                self.Pedido["Mesa"].set(OrdenEditar["Mesa"])
            if OrdenEditar["Hora"] != "":
                self.Pedido["Hora"].set(OrdenEditar["Hora"])
            if OrdenEditar["cliente"] !="":
                self.Pedido["cliente"].set(OrdenEditar["cliente"])
            if OrdenEditar["TipoCliente"] in self.abreviacion["TipoCliente"]:
                self.Pedido["TipoCliente"].set(self.abreviacion["TipoCliente"][OrdenEditar["TipoCliente"]])
            if OrdenEditar["TipoPago"] in self.abreviacion["MediosPagos"]:
                self.Pedido["TipoPago"].set(self.abreviacion["MediosPagos"][OrdenEditar["TipoPago"]])
    def loginInterfaz(self):
        self.usuarioMesero = StringVar()
        self.usuarioMesero.set("Pin de Ingreso")
        self.loginMesero = Frame(self.ventana2,
                           bd = 0,
                           bg = self.Datos["Fondo"],
                           relief="groove")
        self.loginMesero.pack(expand = 1,pady=5)


        Label(self.loginMesero,image = self.imgUsu).pack(pady=6,padx=5,side = "left")
        self.IngresoUsuarioMesero = CrearBotones.entrada(self.loginMesero,self.usuarioMesero,self.Datos,"Pin de Ingreso",1)
        self.IngresoUsuarioMesero.pack(expand  =1,fill = X,pady=5,padx=5,side = "left")
        self.IngresoUsuarioMesero.select_range(0,"end")
        self.IngresoUsuarioMesero.focus()
        self.IngresoUsuarioMesero.bind('<Return>', lambda e:self.logiarseMesero("hola"))
        self.continuarMesero = CrearBotones.Botones(self.loginMesero,"CONTINUAR",self.logiarseMesero,aplicacion1.imgContinuar)
        self.continuarMesero.pack(fill = X,padx=5,pady =5,side="bottom")
    def NuevoPedido(self):
        self.Mesero = self.DatosMesero[0][2]
        self.Interfaz_Nuevo_Pedido()
    def Interfaz_Nuevo_Pedido(self):
        ########################################
        self.ventana2.geometry("1100x600+0+0")
        self.ventana2.title(f"Nuevo pedido {self.Mesero}")
        #self.ventana2.resizable(0,0)
        # Configurar los cuatro frames principales
        Informacion1 = tk.LabelFrame(self.ventana2)
        Categorias1 = tk.LabelFrame(self.ventana2)
        Articulos1 = tk.LabelFrame(self.ventana2)
        VistaPrevia = tk.LabelFrame(self.ventana2,text = "Vista Previa",font = (self.Datos["Tipo de letra"],25),labelanchor="n",bd=0)
        ArticulosVistaPrevia1 = tk.LabelFrame(VistaPrevia)
        totalPedido = tk.LabelFrame(ArticulosVistaPrevia1)
        totalPedido.pack(side="bottom",fill="x")
        Label(totalPedido,text="Total",font = (self.Datos["Tipo de letra"],18)).pack(side="left")
        GuardarPedido = tk.LabelFrame(VistaPrevia)
        self.labelTotalPedido = Label(totalPedido,text="$ 0",font = (self.Datos["Tipo de letra"],18))
        self.labelTotalPedido.pack(side="right",fill = "x",padx = 5)
        F1 = AgregarScrollVerticar(Informacion1)
        F2 = AgregarScrollVerticar(Categorias1)
        F3 = AgregarScrollVerticar(Articulos1)
        F4 = AgregarScrollVerticar(ArticulosVistaPrevia1)


        self.Articulos = F3.frame
        #self.Articulos.config(bg="white")
        F3.canvas.config(width=560, height=600)

        Informacion = F1.frame
        self.Categorias = F2.frame
        F1.canvas.config(width=180)
        F2.canvas.config(width=180)
        F4.canvas.config(width=250)
        self.ArticulosVistaPrevia = F4.frame
        #self.ArticulosVistaPrevia.pack()
        Informacion1.grid(row=0, column=0, columnspan=2, sticky="nsew")
        Categorias1.grid(row=1, column=0, sticky="nsew")
        Articulos1.grid(row=1, column=1, sticky="nsew",padx=10)
        VistaPrevia.grid(row=0, column=2, rowspan=2, sticky="nsew")
        ArticulosVistaPrevia1.grid(row=0, column=0, sticky="nsew")
        GuardarPedido.grid(row=1, column=0, sticky="nsew")
        # Configurar los cuatro frames principales
        self.ventana2.rowconfigure(0, weight=1, minsize=100)
        self.ventana2.rowconfigure(1, weight=1, minsize=500)
        self.ventana2.columnconfigure(0, weight=1)
        self.ventana2.columnconfigure(1, weight=1)
        self.ventana2.columnconfigure(2, weight=1)
        VistaPrevia.rowconfigure(0, weight=1)
        VistaPrevia.rowconfigure(1, weight=1)
        ############################################3
        #Frame de informacion
        self.Pedido = {}
        for i in self.CaracteristicaPepidos:
            self.Pedido[i] = []
        self.Pedido["Total"]=0
        #self.Pedido["Fecha"] = StringVar()
        #self.Pedido["Fecha"].set(self.Fecha)
        self.Pedido["Mesero"] = self.Mesero
        self.Pedido["Mesa"] = StringVar()
        self.Pedido["Mesa"].set("Mesa")
        self.Pedido["Hora"] = StringVar()
        self.Pedido["Hora"].set("Hora")
        self.Pedido["cliente"] = StringVar()
        self.Pedido["cliente"].set("Cliente")

        tipoClientes = []
        MediosPagos = []
        self.abreviacion = {"TipoCliente":{},"MediosPagos":{}}
        for i in self.run_query("select Descripcion,abreviatura From Clientes"):
            tipoClientes.append(i[0])
            self.abreviacion["TipoCliente"][i[0]] = i[1]
            self.abreviacion["TipoCliente"][i[1]] = i[0]
        for j in self.run_query("select Descripcion,abreviacion From MediosPagos"):
            MediosPagos.append(j[0])
            self.abreviacion["MediosPagos"][j[0]] = j[1]
            self.abreviacion["MediosPagos"][j[1]] = j[0]

        #Frame de Informacion Ubicacion

        fechaHoraMesaFrame = LabelFrame(Informacion, text="", font=(self.Datos["Tipo de letra"], 20))
        tiposClienteFrame = LabelFrame(Informacion, text="Tipo de Cliente", font=(self.Datos["Tipo de letra"], 20),labelanchor="n")
        tipoPagoFrame = LabelFrame(Informacion, text="Medio de Pago", font=(self.Datos["Tipo de letra"], 20),labelanchor="n")

        fechaHoraMesaFrame.pack(side="left",fill="both")
        tiposClienteFrame.pack(side="left",fill="both")
        tipoPagoFrame.pack(side="left",fill="both")
        self.Pedido["Fecha"] = DateEntry(fechaHoraMesaFrame, locale="es_ES", date_pattern="yyyy-mm-dd", state="readonly", font = (self.Datos["Tipo de letra"],13))
        self.Pedido["Fecha"].grid(row=0,column=0,columnspan=2,padx=5,pady=5)
        E1 = CrearBotones.entrada(fechaHoraMesaFrame, self.Pedido["Mesa"], self.Datos, "Mesa")
        E1.config(width=5)
        E1.grid(row=1, column=0, padx=5,pady=5,sticky="ew")
        E1 = CrearBotones.entrada(fechaHoraMesaFrame, self.Pedido["Hora"], self.Datos, "Hora")
        E1.config(width=5)
        E1.grid(row=1, column=1, padx=5,pady=5,sticky="ew")


        self.Pedido["TipoCliente"] = CrearBotones.ComboLista(tiposClienteFrame, tipoClientes, self.Datos, 15)
        self.Pedido["TipoCliente"].grid(row=0, column=0, padx=5, pady=5)
        E1 = CrearBotones.entrada(tiposClienteFrame, self.Pedido["cliente"], self.Datos, "Cliente")
        E1.config(width=15)
        E1.grid(row=0, column=1, padx=5, pady=5)

        self.Pedido["TipoPago"] = CrearBotones.ComboLista(tipoPagoFrame, MediosPagos, self.Datos, 19)
        self.Pedido["TipoPago"].grid(row=0, column=0, padx=5, pady=5)
        Label(GuardarPedido, text="Observaciones", font=(self.Datos["Tipo de letra"], 20)).pack(fill="x", padx=5,
                                                                                                pady=5)
        self.Pedido["observaciones"] = Text(GuardarPedido,font = (self.Datos["Tipo de letra"],20),width=10,height=4)
        self.Pedido["observaciones"].pack(fill = "x",padx=5)
        if self.texto == "Normal":
            b1 = CrearBotones.Botones(GuardarPedido,"Guardar",self.GuardarPedido,aplicacion1.imgGuardar)
        else:
            b1 = CrearBotones.Botones(GuardarPedido, "Editar", self.PedidoEditar, aplicacion1.imgGuardar)
        b1.pack(fill = "x",pady=5,padx=5)
        self.actualizarCategoriasPlatos()
        self.InterfazeBotonesMenu()
        #self.ActivarCategoria(self.CategoriaActiva)
    def prueba(self, e):
        pass
    def InterfazeBotonesMenu(self):
        self.BotonesCategoria = {}
        self.Orden ={}
        for Categoria in self.Menu:
            image = Image.open(io.BytesIO(self.MenuIcono[Categoria]))
            photo = ImageTk.PhotoImage(image)
            self.BotonesCategoria[Categoria]={"Frame":LabelFrame(self.Articulos, text=Categoria, bd=0, labelanchor="n", font=(self.Datos["Tipo de letra"], 35)),
                                              "Boton":CrearBotones.Botones(self.Categorias,Categoria,self.ActivarCategoria,photo)}
            self.BotonesCategoria[Categoria]["Boton"].pack(fill="x",pady =5, padx=5)
            x = 0
            i = 0
            for Codigo in self.Menu[Categoria]["Codigo"]:
                CrearBotones.LabelArticuloNuevoPedido(self.BotonesCategoria[Categoria]["Frame"],
                                                      Codigo,
                                                      f"{self.Menu[Categoria]['Codigo'][Codigo]['Articulo']}",
                                                      Categoria,
                                                      self.sumar,
                                                      self.Datos).grid(row =i, column=x+1,sticky="nesw",pady=5)

                Label(self.BotonesCategoria[Categoria]["Frame"],
                      textvariable=self.Menu[Categoria]["Codigo"][Codigo]["Variable"],
                      font= (self.Datos["Tipo de letra"],25),
                      justify="right").grid(row =i, column=x,pady=5)
                Label(self.BotonesCategoria[Categoria]["Frame"],
                      text="\t").grid(row =i, column=x+2,pady=5)
                x = x+3
                if x==6:
                    x=0
                    i = i+1
        self.CategoriaActiva = next(iter(self.BotonesCategoria))
        self.ActivarCategoria(self.CategoriaActiva)
    def actualizarCategoriasPlatos(self):
        self.Menu = {}
        self.MenuIcono = {}
        query = "SELECT *FROM Categorias"
        self.listaCategorias = self.run_query(query)
        for categoria in self.listaCategorias:
            query = f"SELECT *FROM ArticulosCategorias WHERE Categoria == '{categoria[0]}'"
            Platos = self.run_query(query)
            articulos = {"Codigo":{}}
            for plato in Platos:
                variable = StringVar()
                variable.set("  ")
                Articulo = self.agregar_salto_linea_frase(plato[3], 12)
                articulos["Codigo"][plato[1]] = {"Articulo":Articulo,
                                       "Variable":variable,
                                       "Precio":plato[4]}
            Cant = StringVar()
            Cant.set("  ")
            Total = StringVar()
            Total.set("  ")
            articulos["Total"] = {"Cantidad":Cant,
                                  "Total":Total}
            self.Menu[categoria[1]] = articulos
            self.MenuIcono[categoria[1]] = categoria[3]

    def ActivarCategoria(self,Categoria):
        self.BotonesCategoria[self.CategoriaActiva]["Frame"].pack_forget()
        self.BotonesCategoria[Categoria]["Frame"].pack(fill="both",expand=True,padx=15,pady=5)
        self.CategoriaActiva=Categoria
    def logiarseMesero(self,texto):
        query = f"SELECT *FROM Meseros WHERE Pin = {self.usuarioMesero.get()} AND Activo == 'Y'"
        if bool(self.run_query(query)) == True:
            self.DatosMesero = self.run_query(query)
            self.loginMesero.destroy()
            self.NuevoPedido()
        else:
            messagebox.showinfo(message="Mesero no registrado o no Activo", title="Login")
            self.ventana2.deiconify()
            self.IngresoUsuarioMesero.focus()
    def sumar(self,c,codigo,categoria,articulo,event=None):
        self.agregarVistaPrevia(codigo,categoria,articulo)
        try:
            x = int(self.Menu[categoria]["Codigo"][codigo]["Variable"].get())
        except:
            x = 0
        try:
            Total = int(self.Menu[categoria]["Total"]["Total"].get())
        except:
            Total = 0
        try:
            Cantidad = int(self.Menu[categoria]["Total"]["Cantidad"].get())
        except:
            Cantidad = 0
        precio = int(self.Menu[categoria]["Codigo"][codigo]["Precio"])
        sumar = x+c
        Total = Total + precio * c
        Cantidad = Cantidad + c
        if sumar>=0:
            self.Pedido["Total"] = self.Pedido["Total"] + precio * c
            self.labelTotalPedido.config(text='$ {:,}'.format(int(self.Pedido["Total"])))
            self.Menu[categoria]["Total"]["Total"].set(str(Total))
            self.Menu[categoria]["Total"]["Cantidad"].set(str(Cantidad))
            self.Menu[categoria]["Codigo"][codigo]["Variable"].set(str(sumar))
            if sumar==0:
                self.Menu[categoria]["Codigo"][codigo]["Variable"].set("")
                self.Orden[categoria]["Articulos"][codigo]["Frame"].destroy()
                del self.Orden[categoria]["Articulos"][codigo]
                if Cantidad<=0:
                    self.Orden[categoria]["Frame"].destroy()
                    del self.Orden[categoria]
        else:

            self.Orden[categoria]["Articulos"][codigo]["Frame"].destroy()
            del self.Orden[categoria]["Articulos"][codigo]
            if Cantidad<0:
                self.Orden[categoria]["Frame"].destroy()
                del self.Orden[categoria]
    def agregarVistaPrevia(self,codigo,categoria,articulo):
        if categoria in self.Orden:
            if codigo not in self.Orden[categoria]["Articulos"]:
                self.Orden[categoria]["Articulos"][codigo]={"Frame": Frame(self.Orden[categoria]["Frame"]),
                                                 "Pedido":{"Articulo": articulo,
                                                 "Codigo": codigo,
                                                 "Cantidad": self.Menu[categoria]["Codigo"][codigo]["Variable"],
                                                 "Precio": self.Menu[categoria]["Codigo"][codigo]["Precio"]}}
                self.Orden[categoria]["Articulos"][codigo]["Frame"].pack(fill="x")
                Label(self.Orden[categoria]["Articulos"][codigo]["Frame"],
                      text="   ",
                      font=(self.Datos["Tipo de letra"], 15)).grid(row=0, column=0)
                Label(self.Orden[categoria]["Articulos"][codigo]["Frame"],
                      textvariable=self.Menu[categoria]["Codigo"][codigo]["Variable"],
                      font=(self.Datos["Tipo de letra"], 20)).grid(row=0, column=1)
                CrearBotones.LabelArticuloNuevoPedido(self.Orden[categoria]["Articulos"][codigo]["Frame"], codigo, articulo,categoria, self.sumar, self.Datos, 15).grid(row=0, column=2)
        else:
            codigoCategoria = self.run_query(f"select codigo from Categorias where Descripcion = '{categoria}'")[0][0]
            self.Orden[categoria]={}
            self.Orden[categoria]["Frame"] = LabelFrame(self.ArticulosVistaPrevia,font=(self.Datos["Tipo de letra"],20,"bold"),bd=0)
            frameCategoria = Frame(self.Orden[categoria]["Frame"])
            frameCategoria.pack(anchor="w")
            Label(frameCategoria,textvariable=self.Menu[categoria]["Total"]["Cantidad"],font=(self.Datos["Tipo de letra"],25,"bold"),justify="left",anchor="nw").grid(row=0,column=0)
            Label(frameCategoria,text=categoria,font=(self.Datos["Tipo de letra"],25,"bold"),justify = "left",anchor="w").grid(row=0,column=1)
            self.Orden[categoria]["Frame"].pack(fill = "both",expand=True,anchor="nw")
            self.Orden[categoria]["Total"] = self.Menu[categoria]["Total"]
            self.Orden[categoria]["Codigo"] = codigoCategoria
            self.Orden[categoria]["Articulos"] = {}
            self.agregarVistaPrevia(codigo, categoria,articulo)
    def GuardarPedido(self,texto=""):
        if self.texto == "Normal":
            cant = self.run_query('SELECT * FROM Pedido')
            comanda = int(cant[len(cant)-1][0])+1
        else:
            comanda = self.OrdenEditar['Comanda']
        parametros = self.organizarListaParaGuardar()
        print(parametros)
        if self.texto =="Normal":
            self.run_query("insert into Pedido values (Null,?,?,?,?,?,?,?,?,?,?)",parametros)
        parametre = []
        for categoria in self.Orden:
            for codigo in self.Orden[categoria]["Articulos"]:

                lista=(comanda,
                       self.Pedido["Fecha"].get(),
                       codigo,
                       self.Orden[categoria]["Articulos"][codigo]["Pedido"]["Articulo"],
                       self.Orden[categoria]["Codigo"],
                       categoria,
                       self.Orden[categoria]["Articulos"][codigo]["Pedido"]["Cantidad"].get(),
                       self.Orden[categoria]["Articulos"][codigo]["Pedido"]["Precio"],
                       int(self.Orden[categoria]["Articulos"][codigo]["Pedido"]["Cantidad"].get()) * int(self.Orden[categoria]["Articulos"][codigo]["Pedido"]["Precio"]))
                
                x = int(self.run_query(f"select Cantidad from Articulos where Codigo = {codigo}")[0][0])
                y = int(self.Orden[categoria]["Articulos"][codigo]["Pedido"]["Cantidad"].get())
                x = x - y
                self.run_query(f"UPDATE Articulos SET Cantidad = '{x}' WHERE Codigo == {codigo}")
                parametre.append(lista)
            lista = (comanda,
                     self.Pedido["Fecha"].get(),
                     "--",
                     "--",
                     self.Orden[categoria]["Codigo"],
                     categoria,
                     self.Menu[categoria]["Total"]["Cantidad"].get(),
                     0,
                     self.Menu[categoria]["Total"]["Total"].get())
            parametre.append(lista)
        print(parametre)
        self.run_query_many("insert into RegistroPedidos values(?,?,?,?,?,?,?,?,?)",parametre)
        if self.texto == "Normal":
            if messagebox.askyesno(message="!Pedido guardado!\n¿Desea realizar otro pedido?",title="Pedido Guardado"):
                self.ventana2.destroy()
                self.ventana2 = Toplevel(aplicacion1.ventana1)
                self.ventana2.title("Nuevo Pedido")
                self.ventana2.deiconify()
                self.Interfaz_Nuevo_Pedido()
            else:
                self.ventana2.destroy()
            
        else:
            messagebox.showinfo(message="!Pedido Editado!", title="Pedido Editado")
            self.ventana2.destroy()
        aplicacion1.ActualizarInterfazPedido()
    def PedidoEditar(self,texto=""):
        parametros = self.organizarListaParaGuardar()
        for item,i in zip(self.CaracteristicaPepidos[1:],parametros):
            query = f"Update Pedido set {item} = '{i}' where Comanda = {self.OrdenEditar['Comanda']}"
            self.run_query(query)
        self.run_query(f"delete from RegistroPedidos where Comanda = {self.OrdenEditar['Comanda']} and DescripcionCategoria != 'Descuento'")
        for item in self.OrdenEditar["Sumar"]:
            x = int(self.run_query(f"select Cantidad from Articulos where Codigo = {item[1]}")[0][0]) + int(item[0])
            self.run_query(f"UPDATE Articulos SET Cantidad = '{x}' WHERE Codigo == {item[1]}")
        self.GuardarPedido()
    def organizarListaParaGuardar(self):
        if self.Pedido["Mesa"].get() == "Mesa":self.Pedido["Mesa"].set("")
        if self.Pedido["Hora"].get() == "Hora":self.Pedido["Hora"].set("")
        if self.Pedido["cliente"].get() == "Cliente":self.Pedido["cliente"].set("")
        tipopago = ""
        tipocliente = ""
        if self.Pedido["TipoCliente"].get() in self.abreviacion["TipoCliente"]:tipocliente = self.abreviacion["TipoCliente"][self.Pedido["TipoCliente"].get()]
        if self.Pedido["TipoPago"].get() in self.abreviacion["MediosPagos"]:tipopago = self.abreviacion["MediosPagos"][self.Pedido["TipoPago"].get()]
        parametros = [self.Pedido["Fecha"].get(),
                      self.Mesero,
                      self.Pedido["Mesa"].get(),
                      self.Pedido["Hora"].get(),
                      tipocliente,
                      self.Pedido["cliente"].get(),
                      self.Pedido["Total"],
                      tipopago,
                      self.Pedido["observaciones"].get("1.0", "end").rstrip("\n"),
                      1]
        return parametros
    
class NuevoMesero(Interfaz):
    def __init__(self):
        self.Datos = aplicacion1.Datos
        self.baseDatos = aplicacion1.baseDatos
        self.ventanaNuevoMesero = Toplevel(aplicacion1.ventana1,bg = self.Datos["Fondo"])
        self.ventanaNuevoMesero.title("Nuevo Mesero")
        ventanaNuevoMesero = Frame(self.ventanaNuevoMesero,bg = self.Datos["Fondo"])
        ventanaNuevoMesero.pack(fill="both",expand=1,pady=15,padx=15)
        self.VariableNuevoMesero = []
        self.entradas = []
        self.EntradasNuevoMesero =["Primer Nombre","Segundo Nombre","Apellidos","Ingrese Pin"]
        pos = [1,2,3,4]
        Label(ventanaNuevoMesero,
            text="Nuevo Mesero",
            bg = self.Datos["Fondo"],
            fg = self.Datos["Color de letra"],
            font = (self.Datos["Tipo de letra"],25)).grid(column=0,row =0,sticky=E+W)
        for entrada,i in zip(self.EntradasNuevoMesero,pos):
            x = StringVar()
            x.set(entrada)
            self.VariableNuevoMesero.append(x)
            if i==4:
                IngresoContra = CrearBotones.entrada(ventanaNuevoMesero,self.VariableNuevoMesero[i-1],self.Datos,entrada,1)
            else:
                IngresoContra = CrearBotones.entrada(ventanaNuevoMesero,self.VariableNuevoMesero[i-1],self.Datos,entrada)
            IngresoContra.grid(column=0,row =i,sticky=E+W,pady=5)
            self.entradas.append(IngresoContra)
        self.entradas[0].select_range(0,"end")
        self.entradas[0].focus()
        continuar = CrearBotones.Botones(ventanaNuevoMesero,"GUARDAR",self.GuardarNuevoMesero,aplicacion1.imgGuardar)
        continuar.grid(sticky=E+W,padx=5,pady =5)
        continuar.bind('<Return>', lambda e:self.GuardarNuevoMeseso("hola"))


if __name__ == '__main__':
    aplicacion1=Interfaz()
    pedidoApi = PedidoAPI(aplicacion1)
    pedidoApi.run()
    aplicacion1.ventana1.mainloop()
    