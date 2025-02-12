from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os
import tempfile
# Obtener la ruta temporal del sistema
ruta_temporal = tempfile.gettempdir()
def crearPDF(Datos, Orden):
    
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\cocina\\factura-{Orden['Comanda']}.pdf")
    #ruta = f"C:\\Users\\User\\AppData\\Local\\Temp\\GrupoJJ\\cocina\\factura-{Orden['Comanda']}.pdf"
    width, height = 80 * mm, 297 * mm  # Ancho de 80 mm y altura ajustada a A4

    c = canvas.Canvas(ruta, pagesize=(width, height))
    # Establecer el título y la información en el PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, Datos['Empresa'])
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Fecha: {Orden['Fecha']} | N° {Orden['Comanda']}")
    c.drawString(100, 710, f"Hora: {Orden['Hora']} | Mesero: {Orden['Mesero']}")
    c.drawString(100, 690, f"Cliente: {Orden['cliente']}")
    c.drawString(100, 670, "-----------------------")

    # Escribir los detalles de la orden en el PDF
    y_pos = 650
    for Cant, Cat, Pago, item in zip(Orden["cantidad"], Orden["categoria"], Orden["pagos"], enumerate(Orden["pagos"])):
        c.drawString(100, y_pos, f"{Cant}  {Cat}  {'$ {:,}'.format(int(Pago))}")
        y_pos -= 20
        for Subcant, Desc in zip(Orden["SubCant"][item[0]], Orden["descripcion"][item[0]]):
            c.drawString(120, y_pos, f"{Subcant} {Desc}")
            y_pos -= 20

    c.drawString(100, y_pos, "-----------------------")
    y_pos -= 20

    # Escribir el total y las observaciones si las hay
    c.drawString(100, y_pos, f"{Orden['TipoPago']}  Total: {'$ {:,}'.format(int(Orden['Total']))}")
    y_pos -= 20
    if Orden['observaciones'] != '':
        c.drawString(100, y_pos, "-----------------------")
        y_pos -= 20
        c.drawString(100, y_pos, "Observaciones")
        y_pos
    c.save()
    print("lista")
