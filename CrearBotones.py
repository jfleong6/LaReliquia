
from functools import partial
from tkinter import *
import tkinter as tk
from tkinter import ttk,font, messagebox

#from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.colors as mcolors
from datetime import datetime
from collections import defaultdict


class Botones(ttk.Button):
    def __init__(self, ventana, texto, funcion, imagen,**kwargs):
        # Se llama al inicializador de la clase base (ttk.Button)
        super().__init__(ventana, text=texto, image=imagen,compound="left", style="principal.TButton", command=partial(funcion, texto), **kwargs)
        self.image = imagen  # Mantener una referencia de la imagen para evitar la recolección de basura

    def cambiarIcono(self, foto):
        self.config(image=foto)
        self.image = foto  # Actualizar la referencia de la imagen

def SubBotones(ventana,texto,funcion,imagen, T=15):
    button = ttk.Button(ventana,
                    text= texto,
                    cursor = "hand2",
                    image= imagen,
                    compound='left',
                    style= 'sub.TButton',
                    command = partial(funcion,texto))
    return button
def BotonesImagenes(ventana,Imagen,Imagen1,funcion,texto=None,ancho = None):
    def on_enter(e):
        e.widget.config(image = Imagen1)

    def on_leave(e):
        e.widget.config(image = Imagen)

    button = Button(ventana,
                    image = Imagen,
                    bd =0,
                    cursor = "hand2",
                    command = partial(funcion,texto))
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)
    #button.bind("<Button-3>", partial(funcion, texto))
    return button
class LabelVermas(tk.Label):
    def __init__(self, ventana, image, image2, funcion, funcion2, datos, T=25):
        super().__init__(ventana, image=image, bd=0, cursor="hand2", justify="center")
        self.image = image
        self.image2 = image2
        self.funcion = funcion
        self.funcion2 = funcion2
        self.datos = datos
        self.T = T
        self.bind_events()

    def bind_events(self):
        self.bind('<Button-1>', self.funcion)
        self.bind("<Control-Button-1>", self.funcion2)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self.config(image=self.image2)

    def on_leave(self, event):
        self.config(image=self.image)

    def activar_eventos(self):
        self.bind_events()

    def desactivar_eventos(self):
        self.unbind('<Button-1>')
        self.unbind("<Control-Button-1>")
        self.unbind('<Enter>')
        self.unbind('<Leave>')


def LabelArticulo(ventana,texto,categoria,funcion,datos):
    button = ttk.Label(ventana,
                    #width=15,
                    text= f"{texto}",
                    #justify = "left",
                    state = "disable",
                    font =(datos["Tipo de letra"],datos["TamArticulos"],"bold"))

    button.bind('<Button-1>', partial(funcion,1,texto,categoria))
    button.bind('<Button-3>', partial(funcion,-1,texto,categoria))
    return button
def LabelArticuloNuevoPedido(ventana,codigo,texto,categoria,funcion,datos,T=20):
    button = ttk.Button(ventana,
                    #width=15,
                    text= f"{texto}",
                    #bd = 1,
                    #relief="raised",
                    style="iconos.TButton",
                    cursor = "hand2")

    button.bind('<Button-1>', partial(funcion,1,codigo,categoria,texto))

    button.bind('<Button-3>', partial(funcion,-1,codigo,categoria,texto))

    return button
def radiobutton(ventana, texto, Var, valor, datos, funcion, imagen=None):
    radio = ttk.Radiobutton(ventana,
                            style="custom.TRadiobutton",
                            variable=Var,
                            value=valor)

    if imagen is not None:  # Si se proporciona una imagen
        # Configura la imagen en el radiobotón
        radio.config(image=imagen, compound="left")  # Compound="left" coloca la imagen a la izquierda del texto

        # Almacena una referencia a la imagen para evitar que sea eliminada por el recolector de basura
        radio.image = imagen
    if texto is not None:  # Si se proporciona una imagen
        # Configura la imagen en el radiobotón
        radio.config(text=texto.capitalize())  # Compound="left" coloca la imagen a la izquierda del texto
    if funcion is not None: 
        radio.config(command=funcion)
    return radio
class entrada(ttk.Entry):
    def __init__(self, ventana, Var,datos, texto, c=0, **kwargs):
        super().__init__(ventana, textvariable=Var,font= font.Font(family="Times", size=15),**kwargs)
        self.placeholder = texto
        self.c = c

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<Key>", self.press_Key)
        self.bind("<FocusOut>", self.on_focus_out)

        self.manage_placeholder()
    
    def manage_placeholder(self):
        if self.get() == "":
            self.insert(0, self.placeholder)
            if self.c == 1:
                self.config(show="")

    def on_focus_in(self, event):

        self.select_range(0, "end")

    def press_Key(self, event):
        if self.c == 1 and event.keysym != "Tab":
            self.config(show="*")
    def set_text(self, text):
        self.delete(0, "end")
        self.insert(0, text)
        if self.c == 1 and text:
            self.config(show="*")
        else:
            self.manage_placeholder()

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            if self.c == 1:
                self.config(show="")
    
class ComboLista(ttk.Combobox):
    def __init__(self, ventana, lista, datos, ancho):
        super().__init__(ventana, width=ancho, values=lista, cursor="hand2", state="readonly",
                         font=(datos["Tipo de letra"], datos["TamArticulos"], "bold"))

class Tabla_filtro(ttk.Frame):
    def __init__(self, parent, datos, nombre_columnas,ancho_columnas,funcion,buscar,imagen,Columna_Prioridad=[]):
        super().__init__(parent)
        self.parent = parent
        self.funcion = funcion
        self.Columna_Prioridad = Columna_Prioridad
        self.pack(side="left",fill="both",expand=True,pady=5,padx=5)
        frame_busqueda_filtro = LabelFrame(self, text = "")
        frame_busqueda_filtro.pack(fill="both")
        frame_busqueda = LabelFrame(frame_busqueda_filtro,text = f"Buscar {buscar}",fg="blue",font=(15))
        frame_busqueda.pack(side="left",expand=True,padx=5,pady=5,fill="x")
        frame_filtrar = LabelFrame(frame_busqueda_filtro,text = "Filtrar",fg="blue",font=(15))
        frame_filtrar.pack(fill="both",padx=5,pady=5)
        frame_tabla_filtro = LabelFrame(self, text="")
        frame_tabla_filtro.pack(fill="both",expand=True,padx=5,pady=5)
        self.entry = entrada(frame_busqueda,StringVar(),None,"")
        self.entry.config(width=15)
        self.entry.pack(fill="x",padx=5,pady=5)
        self.entry.config(justify="left")
        self.filtro = ttk.Combobox(frame_filtrar,values=nombre_columnas,state="readonly",font=("Times New Roman", 12))
        self.filtro.pack(padx=5,pady=5)
        self.filtro.config(width=15)
        self.filtro.current(1)
        self.frame_seleccionar = LabelFrame(self, text = "")
        self.frame_seleccionar.pack(fill="both")


        self.datos = datos
        self.treeview = TreeView(frame_tabla_filtro, nombre_columnas,ancho_columnas)
        self.treeview.pack(side="left", fill="both", pady=5, padx=5, expand=True, anchor="n")
        self.treeview.limpiar_tabla()
        self.entry.bind("<KeyRelease>", self.actualizar_tabla)
        self.filtro.bind("<<ComboboxSelected>>", self.actualizar_tabla)
        self.actualizar_tabla()
        self.boton_seleccionar = Botones(self.frame_seleccionar,"Seleccionar",self.funcion,imagen)
        self.boton_seleccionar.pack(side="left",fill="both", expand=True, pady=5, padx=5)
        self.ventana = parent
        self.boton_seleccionar.config(command=partial(self.funcion, self.treeview,self.ventana))
    def actualizar_tabla(self, event=None):
        index = self.filtro.current()
        filtro = self.entry.get()
        x = len(filtro)
        self.treeview.limpiar_tabla()
        for i, dato in enumerate(self.datos):
            lista_dato = str(dato[index]).split()
            for e_dato in lista_dato:
                if str(filtro).lower() in e_dato[0:x].lower():
                    if self.Columna_Prioridad == []:
                        self.treeview.insertar_elemento_principal(i, dato[0], dato[1:])
                    else:
                        #self.treeview.insertar_elemento_principal("", "", self.Columna_Priorida[0])
                        pass
                    break
        
        #print(f"{dato[0]}\t{self.elementos_principal[dato[0]]}")

        self.treeview.cambiar_color_fila()
    def insertar_sub_elementos(self, sub_datos):
        print(self.treeview.get_children())
    def cambiar_Datos_tabla(self, nuevos_datos):

        self.treeview.cambiar_datos(nuevos_datos)
class TreeView(ttk.Treeview):
    def __init__(self, parent, colunmas,anchos, **kwargs):

        style = ttk.Style()
        style.layout('Custom.Treeview', [
            ('Custom.Treeview.treearea', {'sticky': 'nswe'})
        ])
        #style.configure("Treeview.Heading", background="blue", foreground="#CFDBE8")
        #style.configure('Custom.Treeview', rowheight=30)
        super().__init__(parent, columns=colunmas[1:])
        self.configure(style='Custom.Treeview')

        self.column("#0", width=anchos[0],anchor="w")
        self.heading("#0", text=colunmas[0])
        for col,ancho in zip(colunmas[1:],anchos[1:]):
            self.column(col, width=ancho, anchor="w")
            self.heading(col, text=col)

        self.parent = parent
        self.elements = {}
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=vsb.set)

        self.pack(side="left",fill="both", pady=5, padx=5, expand=True, anchor="n")
        vsb.pack(side="right",fill="y",pady=5)

        self.tag_configure("fila_par", background="#f0f0ff")
        self.tag_configure("fila_impar", background="#CFDBE8",font=font.Font(family="Times New Roman",size =12))
        self.tag_configure('fila_principal', font=font.Font(family="Times New Roman",size =12))
    def insertar_elemento_principal(self, iid, codigo, nombre):
        # Crear un ID único para el elemento
        # Insertar el elemento en el TreeView
        self.insert("", "end", text=codigo, values=nombre)
        # Guardar una referencia al elemento
        self.elements[iid] = {"codigo": codigo, "nombre": nombre}
    def insertar_sub_elementos(self, iid, id_padre,codigo, datos):
        # Crear un ID único para el subelemento
        # Insertar el subelemento en el TreeView
        self.insert(id_padre, "end", text=codigo, values=datos)
        # Guardar una referencia al subelemento
    def cambiar_color_fila(self):
        for i,item in enumerate(self.get_children()):
            self.item(item, tags=("fila_principal",))
            for j,subitem in enumerate(self.get_children(item)):
                if j%2:
                    self.item(subitem, tags=("fila_par",))
            if i % 2:
                self.item(item, tags=("fila_impar",))
    def limpiar_tabla(self):
        for item in self.get_children():
            self.delete(item)
        self.elements = {}
    def cambiar_datos(self, nuevos_datos):
        # Limpiar la tabla actual
        self.limpiar_tabla()

        # Insertar los nuevos datos
        for dato in nuevos_datos:
            self.insertar_elemento_principal("", dato[0], dato[1:])
        
        # Cambiar el color de las filas si es necesario
        self.cambiar_color_fila()
        
class RoundButton(tk.Button):
    def __init__(self, parent,**kwargs):
        tk.Button.__init__(self, parent, **kwargs)
        self.config(
            padx=10,
            pady=5,
            bd=0,
            bg="white",
            font=font,
            cursor="hand2"
        )
        #self.imagen = imagen
        #self.imagen_1 = imagen_1
        # Carga la imagen y ajusta su tamaño
        imagen_path = "IMAGENES/botones/fondo_boton.png"
        imagen = Image.open(imagen_path)
        imagen = imagen.resize((self.winfo_reqwidth(), self.winfo_reqheight()))
        self.imagen = ImageTk.PhotoImage(imagen)
        # Carga la imagen y ajusta su tamaño
        imagen_path_1 = "IMAGENES/botones/fondo_boton_1.png"
        imagen_1 = Image.open(imagen_path_1)
        imagen_1 = imagen_1.resize((self.winfo_reqwidth(), self.winfo_reqheight()))
        self.imagen_1 = ImageTk.PhotoImage(imagen_1)
        # Agrega la imagen al botón
        self.config(image=self.imagen, compound=tk.CENTER)
        # Agrega el texto al botón
        # Centra el texto en la imagen
        self.config(anchor=tk.CENTER)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, event=None):
        self.config(
            image=self.imagen_1
            # 9FC4EC
            # DFEBF9
        )
    def on_leave(self, event=None):
        self.config(
            image=self.imagen
        )
class EntryPersonalizado(ttk.Entry):
    def __init__(self, *args, font=("Times New Roman", 12), bg="#ffffff", fg="#000000",titulo="si", **kwargs):
        super().__init__(*args, **kwargs)
        #self.configure(font= font.Font(family="Times", size=15))
        self.variable = tk.StringVar()
        self.config(textvariable=self.variable)

        if titulo == "si":
            self.bind("<KeyRelease>", self.actualizar_entry)
    def actualizar_entry(self,event=None):
        filtro = self.variable.get()
        self.variable.set(filtro.title())

class CenterWindow:
    def __init__(self, window):
        self.window = window
        self.center()
    def center(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('+{}+{}'.format(x, y))
    def update_center(self):
        self.center()

class GraficoBase:
    def __init__(self, frame, titulo, xlabel, ylabel, ancho=6,alto =6):
        self.frame = frame
        self.fig, self.ax = plt.subplots(figsize=(ancho,alto))  # Tamaño personalizable, por ejemplo, ancho de 6 pulgadas y altura de 4 pulgadas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid()
        
        
        self.titulo = titulo
        self.ax.set_title(self.titulo)        
        self.xlabel = xlabel
        self.ax.set_xlabel(self.xlabel)        
        self.ylabel = ylabel
        self.ax.set_ylabel(self.ylabel)        
    def limpiar_grafico(self):
        self.ax.clear()
    
    def actualizar_grafico(self):
        self.canvas.draw()
        
        self.ax.set_title(self.titulo)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.canvas.get_tk_widget().grid(sticky="nsew")
        self.fig.tight_layout()
        self.ax.figure.tight_layout()
        self.canvas.draw()
    def generar_colores(self, num_colores):
            # Obtener todos los nombres de colores CSS4
            nombres_colores = list(mcolors.CSS4_COLORS.keys())

            colores_filtrados = []
            for nombre in nombres_colores:
                # Convertir el color a RGB
                rgb = mcolors.to_rgb(mcolors.CSS4_COLORS[nombre])
                # Calcular la luminancia del color
                luminancia = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

                # Excluir colores claros (ajustar el umbral según sea necesario)
                if luminancia < 0.8:  # umbral de luminancia para colores claros
                    colores_filtrados.append(nombre)

            # Seleccionar colores de forma aleatoria
            colores = random.sample(colores_filtrados, num_colores)
            return colores
    
    def clasificar_datos(self, datos, itemCan, porcentaje):
        total_items = len(datos)
        if total_items > itemCan:
            # Ordenar los datos por cantidad en orden descendente
            datos = sorted(datos, key=lambda x: x[1], reverse=True)
            datos_clasificados =[]
            # Calcular el 10% del total de las cantidades
            total_cantidad = sum(item[1] for item in datos)

            # Inicializar la suma de cantidades para 'otros'
            cantidad_90 = 0
            cantidad_10 = 0

            # Sumar las cantidades de los items desde el Inicio hasta alcanzar el 90% del total
            for indice, item in enumerate(datos):
                
                if cantidad_90 <= total_cantidad*porcentaje:
                    datos_clasificados.append(item)
                    cantidad_90 += item[1]
                else:
                    cantidad_10 += item[1]
            datos_clasificados.append(("Otros",cantidad_10))
            return datos_clasificados
        else:
            return datos

    def activar_cuadricula(self):
        # Activar la cuadrícula en ambos ejes
        self.ax.grid(True)
        self.canvas.draw()
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

class GraficoPastel(GraficoBase):
    def __init__(self, frame,titulo="Gráfico de Pastel", xlabel="", ylabel="", ancho=6,alto =6):
        super().__init__(frame,  titulo=titulo, xlabel=xlabel, ylabel=ylabel, ancho=ancho,alto =alto)
    
    def graficar_datos(self, datos):
        tipos_pago, cantidades = zip(*datos)
        self.limpiar_grafico()
        pie = self.ax.pie(cantidades, labels=tipos_pago, autopct='%1.1f%%')
        self.ax.axis('equal')
        
        leng = [f"{tip}: {can}" for tip, can in zip(tipos_pago,cantidades)]
        self.ax.legend(pie[0], leng, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
        
        self.actualizar_grafico()

class GraficoBarras(GraficoBase):
    def __init__(self, frame,titulo = "Gráfico de Barras", xlabel ="Platos", ylabel ="Cantidad", ancho=6,alto =6):
        super().__init__(frame, titulo= titulo, xlabel =xlabel, ylabel =ylabel,ancho=ancho,alto=alto)
    
    def graficar_datos(self, datos):
        categorias, cantidades = zip(*datos)
        categorias =[self.agregar_salto_linea_frase(i,8) for i in categorias]
        self.limpiar_grafico()

        colores = self.generar_colores(len(categorias))
        bars = self.ax.bar(categorias, cantidades, color=colores)
        
        for bar, cantidad in zip(bars, cantidades):
            self.ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        cantidad, ha='center', va='bottom')
        
        self.ax.set_xticks(range(len(categorias)))
        self.ax.set_xticklabels(categorias, rotation=90)
        
        self.actualizar_grafico()

class GraficoLinea(GraficoBase):
    def __init__(self, frame, titulo = "Tiempo VS Ventas", xlabel ="Tiempo", ylabel ="Ventas", ancho=8,alto =6):
        super().__init__(frame, titulo= titulo, xlabel =xlabel, ylabel =ylabel,ancho=ancho,alto = alto)
        listaPrecio = {"Mil":10^3,
                       "Millone":10^6}
    
    def graficar_datos(self, datos_ventas):
        dias, ventas = zip(*datos_ventas)
        self.limpiar_grafico()
        
        # Graficar los datos de ventas
        maxPrecio = max(ventas)
        digitos = int(len(str(maxPrecio)) / 3)
        if digitos >= 2:
            multi = 10 ** ((digitos - 1) * 3)
        else:
            multi = 1
        
        self.ax.plot(dias, ventas, marker='o', color='b', linestyle='-', label="Ventas")
        for dia, venta in zip(dias, ventas):
            precio_formateado = "${:,.0f}".format(venta / multi)
            self.ax.text(dia, venta, precio_formateado, ha='center', va='bottom')
        
        self.ax.set_xticks(dias)
        self.ax.set_xticklabels(dias, rotation=45)
        
        self.actualizar_grafico()
        self.activar_cuadricula()
    
    def graficar_datos_2(self, datos_comparacion, etiqueta_comparacion):
            dias_comp, ventas_comp = zip(*datos_comparacion)
            maxPrecio_comp = max(ventas_comp)
            digitos_comp = int(len(str(maxPrecio_comp)) / 3)
            if digitos_comp >= 2:
                multi_comp = 10 ** ((digitos_comp - 1) * 3)
            else:
                multi_comp = 1
            
            self.ax.plot(dias_comp, ventas_comp, marker='o', color='r', linestyle='-', label=etiqueta_comparacion)
            
            
            self.actualizar_grafico()

class CheckboxCombobox(ttk.Combobox):
    def __init__(self, parent, **kwargs):

        super().__init__(parent, state="readonly", **kwargs)

        self.check_values = []
        self.bind("<<ComboboxSelected>>", self.on_select)

    def valores(self, valores):
        self.valuesOriginal = valores
        self.values = [f"☐ {valor}" for valor in valores]
        self.config(values=self.values)

    def on_select(self, event=None):

        index = self.current()
        value = self.valuesOriginal[index]
        
        if value not in self.check_values:
            self.check_values.append(value)
            self.values[index] = f"☑ {value}"
        else:
            self.check_values.remove(value)
            self.values[index] = f"☐ {value}"

        self.config(values=self.values)
        self.set(self.values[index])
    
    # Método para pasar una lista de valores ya chequeados
    def set_checked_values(self, checked_values):
        # Recorrer los valores originales y establecer los seleccionados
        for i, valor in enumerate(self.valuesOriginal):
            if valor in checked_values:  # Si el valor está en la lista chequeada
                self.check_values.append(valor)  # Agregar a la lista de seleccionados
                self.values[i] = f"☑ {valor}"  # Marcar como seleccionado
            else:
                self.values[i] = f"☐ {valor}"  # Mantener como deseleccionado
        
        self.config(values=self.values)  # Actualizar los valores en el Combobox

    def get(self):
        return ','.join(self.check_values)