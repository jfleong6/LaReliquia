import sqlite3
import tempfile
import os

def Hotel():
    conn = sqlite3.connect('hotel.s3db')
    cursor = conn.cursor()

    # Crear tabla para huéspedes
    cursor.execute('''CREATE TABLE IF NOT EXISTS huespedes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        cedula TEXT,
                        habitacion TEXT,
                        fecha_ingreso TEXT,
                        fecha_salida TEXT,
                        estado TEXT
                    )''')

    # Crear tabla para habitaciones
    cursor.execute('''CREATE TABLE IF NOT EXISTS habitaciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Habitación TEXT,
                        Capacidad TEXT,
                        Cama_doble TEXT,
                        Cama_sencilla TEXT,
                        Camarote TEXT,
                        Tv TEXT,
                        Arie_acondicionado TEXT,
                        Ventilador  TEXT,
                        Estado BOOLEAN
                    )''')

    # Crear tabla para reservas
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_huesped INTEGER,
                        id_habitacion INTEGER,
                        fecha_reserva TEXT,
                        fecha_entrada TEXT,
                        fecha_salida TEXT,
                        FOREIGN KEY(id_huesped) REFERENCES huespedes(id),
                        FOREIGN KEY(id_habitacion) REFERENCES habitaciones(id)
                    )''')

    # Crear tabla para pagos
    cursor.execute('''CREATE TABLE IF NOT EXISTS pagos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_huesped INTEGER,
                        metodo_pago TEXT,
                        precio REAL,
                        fecha_pago TEXT,
                        FOREIGN KEY(id_huesped) REFERENCES huespedes(id)
                    )''')

    # Crear tabla para combos (restaurante)
    cursor.execute('''CREATE TABLE IF NOT EXISTS servicio_huesped (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_huesped INTEGER,
                        servicio TEXT,
                        fecha TEXT,
                        FOREIGN KEY(id_huesped) REFERENCES huespedes(id),
                        FOREIGN KEY(servicio) REFERENCES servicios(descripcion)
                    )''')

    # Crear tabla para servicios
    cursor.execute('''CREATE TABLE IF NOT EXISTS servicios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descripcion TEXT,
                        precio REAL,
                        imagen imagen BLOB
                    )''')
    
    # Crear tabla para servicios compuestos
    cursor.execute('''CREATE TABLE IF NOT EXISTS servicios_compuesta (
                        id_servicio INTEGER,
                        descripcion TEXT,
                        FOREIGN KEY(id_servicio) REFERENCES servicios(id)
                    )''')
    
    # Crear tabla para libro de huéspedes
    cursor.execute('''CREATE TABLE IF NOT EXISTS libro_huesped (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        fecha_ingreso TEXT,
                        fecha_salida TEXT
                    )''')

    conn.commit()
    conn.close()
def Restaurante():
    conn = sqlite3.connect('Base de datos.s3db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "Articulos" (
                "Codigo"	INTEGER NOT NULL,
                "Descripcion"	TEXT NOT NULL,
                "Cantidad"	INTEGER,
                "Gramos"	INTEGER,
                "Prioridad"	INTEGER,
                PRIMARY KEY("Codigo" AUTOINCREMENT)
            );""")


    cursor.execute("""CREATE TABLE IF NOT EXISTS "ArticulosCategorias" (
                "Reg"	INTEGER NOT NULL,
                "Codigo"	INTEGER NOT NULL,
                "Categoria"	TEXT NOT NULL,
                "Descripcion"	TEXT NOT NULL,
                "Valor"	TEXT NOT NULL,
                PRIMARY KEY("Reg" AUTOINCREMENT)
            );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Categorias" (
            "Codigo"	NVARCHAR(4) NOT NULL,
            "Descripcion"	TEXT NOT NULL,
            "Ordenar"	INTEGER,
            "icono"  imagen BLOB 
        );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Cierre_Dia" (
                "Comanda"	INTEGER NOT NULL,
                "Fecha"	DATE,
                "Pedidos"	TEXT NOT NULL,
                "SubTotal"	INTEGER NOT NULL,
                "Bar"	INTEGER,
                "Artesanias"	INTEGER,
                "Cafe"	INTEGER,
                "Tota"	INTEGER,
                "Efectivo"	INTEGER,
                "Transferencia"	INTEGER,
                PRIMARY KEY("Comanda" AUTOINCREMENT)
            );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Clientes" (
                "Codigo"	NVARCHAR(4) NOT NULL UNIQUE,
                "Descripcion"	TEXT NOT NULL UNIQUE,
                "abreviatura"	TEXT
            );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Datos" (
        "nombre"	TEXT NOT NULL,
        "descripcion"	TEXT NOT NULL
    );""")
    
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS "MediosPagos" (
            "Codigo"	NVARCHAR(4) NOT NULL UNIQUE,
            "Descripcion"	TEXT NOT NULL,
            "Abreviacion"	INTEGER
    );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Meseros" (
            "Codigo"	NVARCHAR(4) NOT NULL UNIQUE,
            "Nombre"	TEXT NOT NULL,
            "Usuario"	TEXT,
            "Pin"	INTEGER NOT NULL UNIQUE,
            "Activo"	BOOLEAN NOT NULL,
            "Permisos"	INTEGER NOT NULL
    );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "PagosTransferencias" (
                "Reg"	INTEGER NOT NULL,
                "Fecha"	DATE NOT NULL,
                "Comanda"	INTEGER NOT NULL,
                "Valor"	INTEGER NOT NULL,
                PRIMARY KEY("Reg" AUTOINCREMENT)
            );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Pedido" (
            "Comanda"	INTEGER NOT NULL,
            "Fecha"	DATE NOT NULL,
            "Mesero"	TEXT NOT NULL,
            "Mesa"	TEXT,
            "Hora"	TEXT,
            "TipoCliente"	TEXT,
            "cliente"	TEXT,
            "Total"	INTEGER,
            "TipoPago"	TEXT,
            "observaciones"	TEXT,
            "Activo"	INTEGER NOT NULL,
            PRIMARY KEY("Comanda" AUTOINCREMENT)
            );""")
    
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS "RegEntrada" (
            "Reg"	INTEGER NOT NULL,
            "Fecha"	DATE NOT NULL,
            "Codigo"	INTEGER NOT NULL,
            "Descripcion"	TEXT NOT NULL,
            "Cant"	INTEGER NOT NULL,
            PRIMARY KEY("Reg")
            );""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS "RegistroPedidos" (
            "Comanda"	INTEGER NOT NULL,
            "Fecha"	DATE NOT NULL,
            "CodigoArticulo"	INTEGER NOT NULL,
            "DescripcionArticulo"	TEXT NOT NULL,
            "CodigoCategoria"	TEXT NOT NULL,
            "DescripcionCategoria"	TEXT NOT NULL,
            "Cantidad"	INTEGER NOT NULL,
            "Precio_unitario"	INTEGER NOT NULL,
            "Precio_Total"	INTEGER NOT NULL
            );""")
    
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS "Usuarios" (
                "codigo"	INTEGER NOT NULL,
                "usuario"	TEXT NOT NULL,
                "nombre"	TEXT NOT NULL,
                "pass"	TEXT NOT NULL,
                "tipoUsuario"	INTEGER,
                PRIMARY KEY("codigo" AUTOINCREMENT)
            );""")
    cursor.execute("select *from Datos")
    result = cursor.fetchall()
    if len(result) ==0:
        datos_empresa = [
            ("Empresa", "Centro Vacacional La Reliquia"),
            ("Correo", "hotellareliquia@gmail.com"),
            ("Celular", "3118200458"),
            ("Nit", "90000001"),
            ("Direccion", ""),
            ("Ciudad","Pauna"),
            ("Departamento","Boyaca"),
            ("Tipos Usuario", "ADMINISTRADOR,RECEPCION,RESTAURANTE"),
            ("Clasificacion", "125 gramos,250 gramos,500 gramos,Otros"),
            ("Prioridad", "1,2,3")]
        query = f"INSERT INTO Datos (nombre, descripcion) VALUES (?, ?)"
        cursor.executemany(query, datos_empresa)
    conn.commit()
    conn.close()

    ruta_temporal = tempfile.gettempdir()
    ruta_temporal = os.path.join(ruta_temporal, 'GrupoJJ\\Base de datos.s3db')
    conn = sqlite3.connect(ruta_temporal)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "DatosTemp" (
        "nombre"	TEXT NOT NULL,
        "descripcion"	TEXT NOT NULL
    );""")
    cursor.execute("select *from DatosTemp")
    result = cursor.fetchall()
    if len(result) ==0:
        datos_temp = [
            ("Fondo", "white"),
            ("Fondo menus", ""),
            ("Color de letra", "#007bff"),
            ("Tipo de letra", "Times New Roman"),
            ("Color categoria", "#7D71D8"),
            ("TamCategoria", "11"),
            ("TamArticulos", "13"),
            ("TamTotal", "11"),
            ("En mesa", "#29d884"),
            ("En espera", "#fdef42"),
            ("Por finish", "#808080"),
            ("Color sub boton", "#64ADFC"),
            ("Color sub boton_1", "#8D64FC"),
            ("cierre de dia", "80mm Series Printer"),
            ("reportes", "80mm Series Printer"),
            ("cocina", "80mm Series Printer"),
            ("recibo-caja", "80mm Series Printer"),
            ("recepcion", "\\\\192.168.42.38\\POS-58"),
            ("Lector barra", "COM4")]
        query = f"INSERT INTO DatosTemp (nombre, descripcion) VALUES (?, ?)"
        cursor.executemany(query, datos_temp)
    
    conn.commit()
    conn.close()
