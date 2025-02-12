from datetime import datetime, timedelta

# Obtener la fecha actual
fecha_actual = datetime.now().date()

# Sumar días a la fecha actual
dias_a_sumar = 5  # Por ejemplo, sumar 5 días
nueva_fecha = fecha_actual + timedelta(days=dias_a_sumar)

# Mostrar la nueva fecha
print("Fecha actual:", fecha_actual)
print("Nueva fecha después de sumar", dias_a_sumar, "días:", nueva_fecha)
