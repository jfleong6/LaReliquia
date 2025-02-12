import sqlite3
import datetime
import CrearTablas
from tkinter import messagebox
# Clase para el Hotel
class Hotel:
    def __init__(self):
        self.baseDatosHotel = "hotel.s3db"
        CrearTablas.Hotel()  # Crear tablas si no existen
        self.total_huespedes = 0
        self.huespedes_activos = {}       
        # Al inicializar la clase, cargamos los huéspedes activos
        self.cargar_huespedes_activos()
        self.cargar_habitaciones()
        self.cargar_servicios()

    def cargar_huespedes_activos(self):
        # Consultar todos los huéspedes cuyo estado sea 'activo'
        huespedes = self.run_query('''SELECT id, nombre, cedula, habitacion, fecha_ingreso, fecha_salida 
                                      FROM huespedes WHERE estado = 'activo' ''')
        
        # Guardar los huéspedes activos en el diccionario
        for huesped in huespedes:
            id_huesped = huesped[0]
            nombre = huesped[1]
            cedula = huesped[2]
            habitacion = huesped[3]
            fecha_ingreso = huesped[4]
            fecha_salida = huesped[5]
            
            self.huespedes_activos[id_huesped] = {
                'nombre': nombre,
                'cedula': cedula,
                'habitacion': habitacion,
                'fecha_ingreso': fecha_ingreso,
                'fecha_salida': fecha_salida
            }
        
        # Totalizamos el número de huéspedes activos
        self.total_huespedes = len(self.huespedes_activos)

    def obtener_huespedes_activos(self):
        # Esto devolvería los huéspedes ordenados por habitación o algún otro criterio
        return sorted(self.huespedes_activos.items(), key=lambda x: x[1]['habitacion'])

    def nuevo_huesped(self, nombre, cedula, habitacion, fecha_ingreso, fecha_salida, estado='activo'):
        # Asegúrate de que la consulta considera las columnas correctas de la tabla huespedes
        query = '''INSERT INTO huespedes (nombre, cedula, habitacion, fecha_ingreso, fecha_salida, estado)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        self.run_query(query, (nombre, cedula, habitacion, fecha_ingreso, fecha_salida, estado))
        self.total_huespedes += 1

    def agregar_combo(self, id_huesped, tipo_combo):
        fecha = datetime.datetime.now().strftime('%Y-%m-%d')
        query = '''INSERT INTO servicio_huesped (id_huesped, servicio, fecha) 
                   VALUES (?, ?, ?)'''
        self.run_query(query, (id_huesped, tipo_combo, fecha))
        self.total_combos[tipo_combo] += 1
    
    def registrar_pago(self, id_huesped, metodo_pago, monto):
        fecha = datetime.datetime.now().strftime('%Y-%m-%d')
        query = '''INSERT INTO pagos (id_huesped, metodo_pago, precio, fecha_pago) 
                   VALUES (?, ?, ?, ?)'''
        self.run_query(query, (id_huesped, metodo_pago, monto, fecha))
        
        if metodo_pago == 'Efectivo':
            self.registro_dinero['Efectivo'] += monto
        else:
            if metodo_pago not in self.registro_dinero['Bancos']:
                self.registro_dinero['Bancos'][metodo_pago] = 0
            self.registro_dinero['Bancos'][metodo_pago] += monto

    def generar_reporte_diario(self):
        fecha_hoy = datetime.datetime.now().strftime('%Y-%m-%d')
        
        pagos = self.run_query('''SELECT COUNT(*), SUM(precio) FROM pagos WHERE fecha_pago = ?''', (fecha_hoy,))
        
        reporte = f"Reporte del día {fecha_hoy}:\n"
        reporte += f"Total de pagos: {pagos[0][0]}\n"
        reporte += f"Total de dinero recibido: {pagos[0][1]:.2f} USD\n"
    
    def nueva_habitacion(self, datos):
        parametros = []
        for key in datos:
            parametros.append(datos[key].get())
        query = '''INSERT INTO habitaciones VALUES (Null, ?, ?, ?, ?, ?, ?, ?, ?, True)'''
        self.run_query(query, parametros)
        messagebox.showinfo("Guardar", f"Habitación guardada con éxito.")
    
    def editar_habitacion(self, id, datos):
        for key in datos:
            self.run_query(f"UPDATE habitaciones SET '{key}' = '{datos[key].get()}' WHERE id =='{id}'")
        self.cargar_habitaciones()

    def cargar_habitaciones(self):
        self.habitaciones = [i[0] for i in self.run_query('''SELECT Habitación FROM habitaciones''')]
        
    def cargar_servicios(self):
        self.servicios = [descripcion for descripcion in self.run_query("SELECT id,descripcion,precio FROM servicios")]
        self.servicios_rest = [descripcion for descripcion in self.run_query_rest("SELECT Descripcion FROM Categorias")]
        self.sub_servicios = self.run_query('''SELECT * FROM servicios_compuesta''')
        self.dic_servicios = {}
        self.dic_servicios_id = {}
        for i in self.servicios:
            self.dic_servicios[i[1]] = i[2]
            self.dic_servicios_id[i[0]] = i[1]
        for i in self.servicios_rest:
            self.dic_servicios[i[0]] = ""
        
    def nuevo_servicio(self, datos):
        parametros = (datos["servicio"].get(), datos["precio"].get(), datos["imagen"])
        try:
            self.run_query("INSERT INTO servicios VALUES (NULL, ?, ? , ?)", parametros)
            self.cargar_servicios()            
        except Exception as e:  # Captura cualquier excepción
            # Mostrar un mensaje de error más específico
            messagebox.showerror("Guardar", f"Error al guardar servicio: {str(e)}")
            return

    def nuevos_servicios_compuestos(self,id,valores):
        lista = ([id, i] for i in valores)
        try:
            query = f"INSERT INTO servicios_compuesta VALUES ( ? , ?)"
            self.run_query_many(query,lista)
            self.cargar_servicios()
        except Exception as e:  # Captura cualquier excepción
            # Mostrar un mensaje de error más específico
            messagebox.showerror("Guardar", f"Error al guardar servicio:\n{str(e)}")
            return

    def editar_servicio(self, id, datos):
        self.run_query("UPDATE servicios SET descripcion = ?, precio = ?, imagen = ? WHERE id = ?",(datos["descripcion"].get(),datos["precio"].get(),datos["imagen"], id))

        self.cargar_habitaciones()

    def eliminar_servicios_compuestos(self, id):
        self.run_query(f"DELETE FROM servicios_compuesta WHERE id_servicio = {id}")

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.baseDatosHotel) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            result = cursor.fetchall()
            conn.commit()
        return result
    
    def run_query_many(self,query,parameters = ()):
        with sqlite3.connect(self.baseDatosHotel) as conect:
            cursor = conect.cursor()
            cursor.executemany(query,parameters)
            result = cursor.fetchall()
            conect.commit()
            return result
    
    def run_query_rest(self, query, parameters=()):
        base = "Base de datos.s3db"
        with sqlite3.connect(base) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            result = cursor.fetchall()
            conn.commit()
        return result
