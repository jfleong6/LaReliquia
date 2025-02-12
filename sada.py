import sqlite3

def copiar_iconos(origen_db, destino_db, tabla, columna):
    try:
        # Conectar a la base de datos de origen
        origen_conn = sqlite3.connect(origen_db)
        origen_cursor = origen_conn.cursor()
        
        # Conectar a la base de datos de destino
        destino_conn = sqlite3.connect(destino_db)
        destino_cursor = destino_conn.cursor()
        
        # Obtener los datos de la tabla origen
        origen_cursor.execute(f"SELECT Codigo, {columna} FROM {tabla}")
        registros = origen_cursor.fetchall()
        
        # Copiar los datos a la tabla destino
        for id_categoria, icono in registros:
            destino_cursor.execute(f"""
                UPDATE {tabla} SET {columna} = ? WHERE Codigo = ?
            """, (icono, id_categoria))
        
        # Confirmar cambios
        destino_conn.commit()
        
        print("Datos copiados correctamente.")
    except sqlite3.Error as e:
        print("Error en la base de datos:", e)
    finally:
        # Cerrar conexiones
        origen_conn.close()
        destino_conn.close()

# Uso de la función
copiar_iconos("JJ.s3db", "Base de datos.s3db",  "categorias", "icono")
