from conexion_base import ConexionBase
from datetime import datetime, timedelta
import random

def insertar_datos_prueba():
    # Inicializar la conexión
    db = ConexionBase("tienda.db")
    
    # Insertar clientes de prueba
    clientes = [
        {"nombre": "Juan Pérez", "telefono": "3001234567", "email": "juan@email.com"},
        {"nombre": "María López", "telefono": "3109876543", "email": "maria@email.com"},
        {"nombre": "Carlos Rodríguez", "telefono": "3202345678", "email": "carlos@email.com"},
        {"nombre": "Ana Martínez", "telefono": "3153456789", "email": "ana@email.com"},
        {"nombre": "Pedro González", "telefono": "3184567890", "email": "pedro@email.com"},
        {"nombre": "Laura Torres", "telefono": "3135678901", "email": "laura@email.com"},
        {"nombre": "Diego Ramírez", "telefono": "3146789012", "email": "diego@email.com"},
        {"nombre": "Sofía Castro", "telefono": "3167890123", "email": "sofia@email.com"},
        {"nombre": "Luis Morales", "telefono": "3178901234", "email": "luis@email.com"},
        {"nombre": "Carmen Ortiz", "telefono": "3189012345", "email": "carmen@email.com"},
        {"nombre": "Roberto Jiménez", "telefono": "3157894561", "email": "roberto@email.com"},
        {"nombre": "Patricia Ruiz", "telefono": "3168529637", "email": "patricia@email.com"},
        {"nombre": "Fernando Silva", "telefono": "3179514268", "email": "fernando@email.com"},
        {"nombre": "Andrea Vargas", "telefono": "3183692581", "email": "andrea@email.com"},
        {"nombre": "Miguel Ángel Díaz", "telefono": "3192581473", "email": "miguel@email.com"}
    ]
    
    for cliente in clientes:
        db.insertar("clientes", cliente)
    
    # Obtener datos necesarios
    productos = db.seleccionar("productos")
    vendedores = db.seleccionar("usuarios")
    clientes_ids = range(1, len(clientes) + 1)
    
    # Calcular fechas para generar datos desde el año pasado hasta hoy
    fecha_actual = datetime.now()
    fecha_inicio = datetime(fecha_actual.year - 1, 1, 1)  # 1 de enero del año pasado
    dias_totales = (fecha_actual - fecha_inicio).days

    # Patrones de ventas por mes (factor multiplicador)
    patrones_mensuales = {
        1: 0.8,   # Enero (ventas más bajas post-navidad)
        2: 0.7,   # Febrero
        3: 0.9,   # Marzo
        4: 1.0,   # Abril
        5: 1.1,   # Mayo
        6: 1.0,   # Junio
        7: 1.2,   # Julio (mitad de año)
        8: 0.9,   # Agosto
        9: 1.0,   # Septiembre
        10: 1.1,  # Octubre
        11: 1.3,  # Noviembre (black friday)
        12: 1.5   # Diciembre (navidad)
    }

    # Generar ventas para cada día
    for dia in range(dias_totales):
        fecha_venta = fecha_inicio + timedelta(days=dia)
        fecha = fecha_venta.strftime("%Y-%m-%d %H:%M:%S")
        
        # Ajustar número de ventas según el mes
        factor_mes = patrones_mensuales[fecha_venta.month]
        num_ventas_base = random.randint(2, 6)  # Base de ventas diarias
        num_ventas = int(num_ventas_base * factor_mes)
        
        # Generar ventas para el día
        for _ in range(num_ventas):
            # Crear venta
            vendedor = random.choice(vendedores)
            cliente_id = random.choice(clientes_ids)
            
            # Insertar la venta
            venta = {
                "vendedor_id": vendedor[0],
                "cliente_id": cliente_id,
                "fecha": fecha,
                "total": 0
            }
            db.insertar("ventas", venta)
            
            # Obtener el ID de la última venta
            ultima_venta = db.ejecutar_personalizado("SELECT MAX(id) FROM ventas")[0][0]
            
            # Generar detalles de la venta
            total_venta = 0
            num_productos = random.randint(1, 8)  # Aumentamos el máximo de productos por venta
            productos_seleccionados = random.sample(productos, num_productos)
            
            for producto in productos_seleccionados:
                # Variar cantidad según el tipo de producto
                if producto[6] in ['Tecnología', 'Muebles']:  # Categorías de alto valor
                    cantidad = random.randint(1, 2)
                else:  # Categorías de menor valor
                    cantidad = random.randint(1, 5)
                
                precio_unitario = producto[4]
                
                # Aplicar descuentos aleatorios en fechas especiales
                if fecha_venta.month == 11 and random.random() < 0.3:  # Black Friday
                    precio_unitario *= 0.8  # 20% descuento
                elif fecha_venta.month == 12 and random.random() < 0.2:  # Navidad
                    precio_unitario *= 0.9  # 10% descuento
                
                detalle_venta = {
                    "venta_id": ultima_venta,
                    "producto_id": producto[0],
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario
                }
                db.insertar("detalles_ventas", detalle_venta)
                
                total_venta += cantidad * precio_unitario
                
                # Actualizar stock y generar reposición si es necesario
                stock_actual = producto[5] - cantidad
                if stock_actual < 5:  # Punto de reorden
                    # Registrar entrada de productos
                    cantidad_reposicion = random.randint(10, 30)
                    registro_entrada = {
                        "producto_id": producto[0],
                        "cantidad": cantidad_reposicion,
                        "fecha": fecha,
                        "usuario": vendedor[0],
                        "observacion": "Reposición automática por bajo stock"
                    }
                    db.insertar("registro_entradas", registro_entrada)
                    stock_actual += cantidad_reposicion
                
                db.actualizar("productos", {"stock": stock_actual}, "id = ?", (producto[0],))
            
            # Actualizar el total de la venta
            db.actualizar("ventas", {"total": total_venta}, "id = ?", (ultima_venta,))
            
            # Insertar pago
            # Distribuir métodos de pago según tendencias
            metodos_pago_dist = ['Efectivo'] * 4 + ['Tarjeta'] * 4 + ['Transferencia'] * 2
            pago = {
                "venta_id": ultima_venta,
                "metodo_pago": random.choice(metodos_pago_dist),
                "valor": total_venta
            }
            db.insertar("pagos_venta", pago)
            
            # Registrar modificaciones ocasionales
            if random.random() < 0.1:  # 10% de probabilidad
                registro_mod = {
                    "id_producto": random.choice(productos)[0],
                    "id_usuario": vendedor[0],
                    "fecha_hora": fecha,
                    "detalle": random.choice([
                        "Actualización de precio",
                        "Corrección de inventario",
                        "Ajuste de descripción",
                        "Verificación de stock",
                        "Cambio de categoría"
                    ])
                }
                db.insertar("registro_modificaciones", registro_mod)

if __name__ == "__main__":
    try:
        insertar_datos_prueba()
        print("Datos de prueba insertados exitosamente")
    except Exception as e:
        print(f"Error al insertar datos de prueba: {e}")