from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
import os
import tempfile

ruta_temporal = tempfile.gettempdir()

def crearPDF():
    width, height = 80 * mm, 297 * mm  # Ancho de 80 mm y altura ajustada a A4
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\cocina\\factura-1.pdf")
    c = canvas.Canvas(ruta, pagesize=(width, height))

    # Establecer tamaño de letra y margen
    c.setFont("Helvetica", 12)
    margen_izquierdo = 5 
    margen_derecho = width - 5
    margen_superior = height - 10
    margen_inferior = 10
    y_pos = margen_superior - 10

    # Función para dibujar texto con márgenes
    def dibujar_texto(texto, x, y):
        c.drawString(x, y, texto)

    # Función para dibujar líneas separadoras
    def dibujar_linea(x1, y1, x2, y2):
        c.line(x1, y1, x2, y2)
    #Crear datos para la tabla
    datosOrdinarios =[["Centro Vacacional\n la Recreacional","","",""] ,
                      ["Fecha:","01/01/2024","Comanda:","9999"],
                      ["Hora:","7:35 pm","Mesero:","Fredy"],
                      ["Cliente:","Cabaña 1","",""]]
    # Crear datos para la tabla (ejemplo)
    data = [['CANT', "","CATEGORIA",'PRECIO'],
            ['5', "", 'Desayunos', '$ 50.000'],
            ["", '1', 'Tamal', ""],
            ["", '2', 'Carne En bistek\n con tomate', ""],

            ["3", '', 'Americano', '$ 24.000'],
            ["", '1', 'Revueltos', ""],
            ["", '1', 'Pericos', ""],
            ["", '1', 'Rancheros', ""]]
    # Establecer el título y la información en el PDF
   
    # Calcular anchos de columnas proporcionalmente
    total_width = margen_derecho - margen_izquierdo
    cant_width = total_width * 0.1
    subcant_width = cant_width
    categoria_width = total_width * 0.5
    precio_width = total_width * 0.3

    # Estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
                        ('BACKGROUND', (0, 4), (-1, 4), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('SPAN', (0, 0), (1, 0))])
    
    style1 = TableStyle([('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                        ('SPAN', (0, 0), (-1, 0)),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTSIZE', (0, 0), (-1, 0), 15),
                        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
                        ('FONTNAME', (2, 0), (2, -1), 'Times-Bold'),
                        ('FONTSIZE', (1, 3), (1, 3), 13),
                        ('FONTSIZE', (-1, 1), (-1, 1), 13),
                        ('FONTNAME', (-1, 1), (-1, 1), 'Times-Bold')])
    # Crear tabla con anchos de columnas
    tabla = Table(data,colWidths=[cant_width, subcant_width, categoria_width,  precio_width])
    tabla.setStyle(style)
    tabla1 = Table(datosOrdinarios)
    tabla1.setStyle(style1)
    # Dibujar la tabla en el PDF
    tabla1.wrapOn(c, total_width, margen_superior)
    tabla1.drawOn(c, margen_izquierdo, margen_superior-tabla1._height)
    # Dibujar la tabla en el PDF
    tabla.wrapOn(c, total_width, margen_superior-tabla1._height)
    tabla.drawOn(c, margen_izquierdo,margen_superior-tabla1._height - tabla._height-5)

    c.save()


crearPDF()
