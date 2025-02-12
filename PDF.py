#import pdfkit
import os
import sqlite3
from datetime import datetime
import win32print

import win32api
import tempfile
import time
import os
import tempfile
import facturaCocina
import ReciboCaja
# Obtener la ruta temporal del sistema
ruta_temporal = tempfile.gettempdir()
#import aspose.words as aw
def run_query(query,parameters = ()):
        with sqlite3.connect("Base de datos.s3db") as conect:
            cursor = conect.cursor()
            cursor.execute(query,parameters)
            result = cursor.fetchall()
            conect.commit()
            return result

def crearPDF(Datos,Orden):
    #facturaCocina.cocina(Datos,Orden)
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\cocina\\factura-{Orden['Comanda']}.txt")
    with open(ruta,"w") as file:
        #file.write("<div class='logo-container'><img style='height: 30px;' src='LOGO.png'/></div>")
        #file.write("<img  src = 'LOGO.png' width='80' height='80'>")
        file.write(f"{Datos['Empresa']}\n")
        file.write(f"{Orden['Fecha']}|")
        file.write(f"N° ")
        file.write(f"{Orden['Comanda']}\n")
        file.write(f"{Orden['Hora']}")
        file.write(f"|Mesero: ")
        file.write(f"{Orden['Mesero']}\n")
        file.write(f"Cliente: ")
        file.write(f"{Orden['cliente']}\n")
        file.write("-----------------------\n")
        for Cant,Cat,Pago,item in zip(Orden["cantidad"],Orden["categoria"],Orden["pagos"],enumerate(Orden["pagos"])):
             file.write(f"{Cant}")
             file.write(f"  {Cat}")
             file.write(f"  {'$ {:,}'.format(int(Pago))}\n")
             for Subcant, Desc in zip(Orden["SubCant"][item[0]],Orden["descripcion"][item[0]]):
                 file.write(f"   {Subcant}")
                 file.write(f" {Desc}\n")
        file.write("-----------------------\n")
        file.write(f"{Orden['TipoPago']}")
        file.write(f"  Total: ")
        file.write(f"{'$ {:,}'.format(int(Orden['Total']))}\n")
        if Orden['observaciones'] != '':
            file.write("-----------------------\n")
            file.write(f"Observaciones\n")
            file.write(f"{Orden['observaciones']}\n")
        file.write("-----------------------\n")
        file.write("Cocina")
        file.close()
    imprimir_archivo(ruta,Datos["cocina"])    
    #os.startfile("factura.txt","print")

def imprimir_archivo(archivo, nombre_impresora):
    impresora_original = None
    try:
        # Guardar la impresora predeterminada original para restaurarla más tarde
        impresora_original = win32print.GetDefaultPrinter()

        # Buscar la impresora por nombre
        impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL + win32print.PRINTER_ENUM_CONNECTIONS, None, 1)
        impresora_encontrada = next((printer for printer in impresoras if nombre_impresora.lower() in printer[2].lower()), None)
        
        if impresora_encontrada:
            nombre_impresora_encontrada = impresora_encontrada[2]
            win32print.SetDefaultPrinter(nombre_impresora_encontrada)
            win32api.ShellExecute(0, "print", archivo, None, ".", 0)
        else:
            print("No se encontró la impresora. Imprimiendo en la predeterminada.")
            win32api.ShellExecute(0, "print", archivo, None, ".", 0)

    except Exception as e:
        print("Error al imprimir:", str(e))
    finally:
        if impresora_original:
            win32print.SetDefaultPrinter(impresora_original)  # Restaurar la impresora original

def Recepcion(Datos,Orden):

    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\recepcion\\recepcion-{Orden['Comanda']}.txt") 
    with open(ruta,"w") as file:
        #file.write("<div class='logo-container'><img style='height: 30px;' src='LOGO.png'/></div>")
        #file.write("<img  src = 'LOGO.png' width='80' height='80'>")
        file.write(f"{Datos['Empresa']}\n")
        file.write(f"{datetime.now().time().strftime("%I:%M %p")}\n")
        file.write(f"{Orden['Fecha']}\n")
        file.write(f"N° ")
        file.write(f"{Orden['Comanda']}\n")
        file.write(f"Mesero: ")
        file.write(f"{Orden['Mesero']}\n")
        file.write(f"Cliente: ")
        file.write(f"{Orden['cliente']}\n")
        for Cant,Cat,Pago,item in zip(Orden["cantidad"],Orden["categoria"],Orden["pagos"],enumerate(Orden["pagos"])):
             file.write("---------------\n")   
             file.write(f"{Cant}")
             file.write(f"  {Cat}\n")
             for Subcant, Desc in zip(Orden["SubCant"][item[0]],Orden["descripcion"][item[0]]):
                 file.write(f"   {Subcant}")
                 file.write(f" {Desc}\n")
        file.write(f"{Orden['TipoPago']} Recepción\n")
        file.write(f"Total: ")
        file.write(f"{'$ {:,}'.format(int(Orden['Total']))}\n")
        file.write("---------------\n")
        
        file.close()
    imprimir_archivo(ruta,Datos["recepcion"])

def CrearReporte(Datos, reporteParcial):
        ruta = os.path.join(ruta_temporal, f"GrupoJJ\\reportes")
        # Obtener la lista de archivos en la carpeta
        archivos = os.listdir(ruta)

        # Filtrar los archivos de reporte y determinar el número máximo
        archivos_reporte = [archivo for archivo in archivos if archivo.startswith('reporte')]
        if archivos_reporte:
                numeros = [int(archivo.split('_')[1].split('.')[0]) for archivo in archivos_reporte]
                siguiente_numero = max(numeros) + 1
        else:
                siguiente_numero = 1
        ruta = f"{ruta}\\reporte_{siguiente_numero}.txt"
        with open(ruta,"w") as file:
                lista = {1: "En Espera",2:"En mesa"}
                total = 0
                for Estado in reporteParcial:
                    if Estado in lista:
                        for categoria in reporteParcial[Estado]:
                            file.write(f"{categoria}\n")
                            totalC = 0
                            for plato in reporteParcial[Estado][categoria]:
                                total = int(reporteParcial[Estado][categoria][plato])+ total
                                totalC = int(reporteParcial[Estado][categoria][plato])+ totalC
                                file.write(f"*{plato}: {reporteParcial[Estado][categoria][plato]}\n")
                            file.write(f"SubTotal: {totalC}")
                            file.write("\n-----------------------\n")
                file.write(f"Total: {total}")
                file.close()
                #os.startfile("reporte parcial.txt","print")
                imprimir_archivo(ruta,Datos["reportes"])

def CrearCierreDia(Comandas,Fecha,Datos,consecutivo,otras,transferencia):
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\cierre de dia\\Cierre {consecutivo+1}.txt")
    with open(ruta,"w") as file:
        listaotros = ["Bar","Artesanias","Cafe"]
        #file.write("<div class='logo-container'><img style='height: 30px;' src='LOGO.png'/></div>")
        #file.write("<img  src = 'LOGO.png' width='80' height='80'>")
        file.write(f"{Datos['Empresa']}\n")
        file.write(f"Fecha: ")
        file.write(f"{Fecha}")
        file.write(f"  N° {consecutivo+1}\n")
        file.write(f"Cliente:")
        file.write(f"Restaurante\n")
        file.write(f"Ped")
        file.write(f"\tMesero")
        file.write(f"\tValor\n")
        Numero = ''
        Total = 0
        parametro = []
        for Pedido in Comandas:
            trans =run_query(f"select sum(Valor) from PagosTransferencias where Comanda = '{Pedido[0]}'")
            icono = "#"
            if trans[0][0] != None:
                icono = "*"
            Numero= Numero + f"{Pedido[0]}/"
            run_query(f"UPDATE Pedido SET 'Activo' = '5' WHERE Comanda = '{Pedido[0]}'")
            Total = Total + int(Pedido[7])
            file.write(f"{icono}{Pedido[0]}")
            file.write(f"¬{Pedido[2]}")
            file.write(f"¬{'$ {:,}'.format(int(Pedido[7]))}\n")
        file.write("-----------------------\n")
        file.write("SubTotal:")
        file.write(f" {'$ {:,}'.format(int(Total))}\n")
        parametro.append(Numero)
        parametro.append(Total)
        for otro,lista in zip(otras,listaotros):
            try:
                x =int(otro)
                if x>0:
                    file.write(f"{lista}: {'$ {:,}'.format(int(otro))}\n")
                    Total = Total + int(otro)
                    parametro.append(int(otro))
            except:
                parametro.append(0)
        file.write("TOTAL:")
        file.write(f" {'$ {:,}'.format(int(Total))}\n")
        efectivo = Total-transferencia
        file.write("-----------------------\n")
        if efectivo >0:
            file.write("Efectivo:")
            file.write(f" {'$ {:,}'.format(int(efectivo))}\n")
        if transferencia >0:
            file.write("Transferencia:")
            file.write(f" {'$ {:,}'.format(int(transferencia))}\n")
        parametro.append(Total)
        parametro.append(efectivo)
        parametro.append(transferencia)
        file.close()

        imprimir_archivo(ruta,Datos["cierre de dia"])
        #os.startfile("cierre de dia.txt","print")
    return parametro

def reciboCaja(Datos,Orden,Ref):
    ReciboCaja.crearPDFReciboCaja(Datos,Orden,Ref)
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\recibo-caja\\recibo-caja-{Ref}.pdf")   
    imprimir_archivo(ruta,Datos["recibo-caja"])  
    print("Vamos bien")

def verificar_carpetas():
    ruta_temporal = tempfile.gettempdir()

    carpetas_a_verificar = [
        (ruta_temporal, 'GrupoJJ'),
        (os.path.join(ruta_temporal, 'GrupoJJ'), 'cierre de dia'),
        (os.path.join(ruta_temporal, 'GrupoJJ'), 'cocina'),
        (os.path.join(ruta_temporal, 'GrupoJJ'), 'recepcion'),
        (os.path.join(ruta_temporal, 'GrupoJJ'), 'recibo-caja'),
        (os.path.join(ruta_temporal, 'GrupoJJ'), 'reportes')
    ]

    for ruta, nombre_carpeta in carpetas_a_verificar:
        ruta_completa = os.path.join(ruta, nombre_carpeta)
        if not os.path.exists(ruta_completa):
            os.makedirs(ruta_completa)
            print(f'Se ha creado la carpeta {ruta_completa}')

verificar_carpetas()

