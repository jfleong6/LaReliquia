import sqlite3
from datetime import datetime
def cambiar_formato_fecha_individual():
    try:
        cambiarFechaPedidosReg()
        cambiarFechaPagosQR()
        print("listo")
    
    except sqlite3.Error as e:
        print(f"Error al cambiar el formato de fecha: {e}")
        conn.rollback()
    
    finally:
        # Cerrar conexión
        conn.close()
def cambiarFechaPedidosReg():
    # Obtener todos los registros de la tabla original
        cursor.execute("SELECT * FROM Pedido")
        rows = cursor.fetchall()

        # Actualizar cada registro individualmente
        for row in rows:
            fecha_original = row[1]
            if fecha_original is not None:
                # Convertimos la cadena de texto a un objeto datetime

                fecha_datetime = datetime.strptime(fecha_original, '%d-%m-%Y')               
                # Ahora podemos formatear la fecha como deseemos
                fecha_nueva = fecha_datetime.strftime('%Y-%m-%d')
                cursor.execute(f"UPDATE Pedido SET Fecha = ? WHERE Comanda = ?;", (fecha_nueva, row[0]))
                cursor.execute(f"UPDATE RegistroPedidos SET Fecha = ? WHERE Comanda = ?;", (fecha_nueva, row[0]))
        conn.commit()
def cambiarFechaPagosQR():
    cursor.execute("SELECT * FROM PagosTransferencias")
    rows = cursor.fetchall()
    for row in rows:
        fecha_original = row[1]
        
        if fecha_original is not None:
            # Convertimos la cadena de texto a un objeto datetime
            fecha_datetime = datetime.strptime(fecha_original, '%d-%m-%Y')
            # Ahora podemos formatear la fecha como deseemos
            fecha_nueva = fecha_datetime.strftime('%Y-%m-%d')
            cursor.execute(f"UPDATE PagosTransferencias SET Fecha = ? WHERE Reg = ?;", (fecha_nueva, row[0]))
    conn.commit()

def copiarTabla(nombre_tabla_origen, nombre_tabla_destino):

    # Obtener la estructura de la tabla origen
    cursor.execute(f"PRAGMA table_info({nombre_tabla_origen})")
    estructura = cursor.fetchall()
    columnas = ", ".join([f'"{col[1]}" {col[2]}' for col in estructura])

    # Crear la tabla destino con la misma estructura
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {nombre_tabla_destino} ({columnas})")

    # Copiar los datos de la tabla origen a la tabla destino
    cursor.execute(f"INSERT INTO {nombre_tabla_destino} SELECT * FROM {nombre_tabla_origen}")

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()


db_file_path = "Base de datos.s3db"
conn = sqlite3.connect(db_file_path)

# Conexión a la base de datos
cursor = conn.cursor()
#cambiar_formato_fecha_individual()
copiarTabla("Datos","DatosTemp")

