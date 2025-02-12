from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
import os
import tempfile

ruta_temporal = tempfile.gettempdir()

def cocina(Datos,Orden):
    width, height = 80 * mm, 297 * mm  # Ancho de 80 mm y altura ajustada a A4
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\cocina\\factura-{Orden['Comanda']}.pdf")
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
    datosOrdinarios =[[f"{Datos['Empresa']}","","",""],
                      ["","","","",""],
                      ["Fecha:",f"{Orden['Fecha']}","Comanda:",f"{Orden['Comanda']}"],
                      ["Hora:",f"{Orden['Hora']}","Mesero:",f"{Orden['Mesero']}"],
                      ["Cliente:",f"{Orden['cliente']}","",""]]
    estilosProductos = [('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
                        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 13),
                        ('SPAN', (0, 0), (1, 0))]
    # Crear datos para la tabla (ejemplo)
    data = [['CANT', "","CATEGORIA",'PRECIO']]
    j = 1
    for Cant,Cat,Pago,item in zip(Orden["cantidad"],Orden["categoria"],Orden["pagos"],enumerate(Orden["pagos"])):
        estilosProductos.append(('FONTNAME', (0, j), (-1, j), 'Times-Bold'))
        estilosProductos.append(('LINEBELOW', (0, j-1), (-1, j-1), 1, colors.black))
        #estilosProductos.append(('FONTSIZE', (0, j), (-1, j), 13))  
        data.append([Cant,"",Cat,'$ {:,}'.format(int(Pago))])
        for Subcant, Desc in zip(Orden["SubCant"][item[0]],Orden["descripcion"][item[0]]):
            data.append(["",Subcant,Desc,""])
            j+=1
        j+=1
    
    total_width = margen_derecho - margen_izquierdo
    cant_width = total_width * 0.1
    subcant_width = cant_width
    categoria_width = total_width * 0.5
    precio_width = total_width * 0.3

    # Estilo de la tabla
    style = TableStyle(estilosProductos,hAlign='LEFT')
    
    style1 = TableStyle([('ALIGN', (0, 0), (-1, 1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                        ('SPAN', (0, 0), (-1, 0)),
                        ('SPAN', (0, 1), (-1, 1)),
                        ('FONTSIZE', (0, 1), (-1, 1), 8),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTSIZE', (0, 0), (-1, 0), 15),
                        ('ALIGN', (0, 2), (-1, -1), 'LEFT'),
                        ('FONTNAME', (2, 0), (2, -1), 'Times-Bold'),
                        ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
                        ('FONTSIZE', (1, 4), (1, 4), 13),
                        ('FONTSIZE', (-1,2), (-1, 2), 13),
                        ('FONTNAME', (-1, 2), (-1, 2), 'Times-Bold')])
    # Crear tabla con anchos de columnas
    tabla = Table(data,colWidths=[cant_width, subcant_width, categoria_width,  precio_width],hAlign='LEFT')
    tabla.setStyle(style)
    
    
    tabla1 = Table(datosOrdinarios)
    tabla1.setStyle(style1)
    # Dibujar la tabla en el PDF
    tabla1.wrapOn(c, total_width, margen_superior)
    tabla1.drawOn(c, margen_izquierdo, margen_superior-tabla1._height)
    # Dibujar la tabla en el PDF
    tabla.wrapOn(c, total_width, margen_superior-tabla1._height)
    tabla.drawOn(c, margen_izquierdo,margen_superior-tabla1._height - tabla._height-5)
    # Ajustar el tamaño de las celdas para que el texto se ajuste automáticamente


    c.save()