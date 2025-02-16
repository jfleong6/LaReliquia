import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd
from conexion_base import ConexionBase
from tkcalendar import DateEntry
from CTkMessagebox import CTkMessagebox
import os

class GestorReportes(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Gestor de Reportes")
        self.geometry("800x600")
        self.db = ConexionBase("tienda.db")
        
        # Crear el directorio de reportes si no existe
        if not os.path.exists("reportes"):
            os.makedirs("reportes")
            
        self._crear_widgets()
        
    def _crear_widgets(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(self.frame_principal, 
                            text="Generación de Reportes",
                            font=("Helvetica", 20, "bold"))
        titulo.pack(pady=10)
        
        # Frame de filtros
        self.frame_filtros = ctk.CTkFrame(self.frame_principal)
        self.frame_filtros.pack(fill="x", padx=10, pady=5)
        
        # Selector de tipo de reporte
        self.tipo_reporte = ctk.CTkComboBox(
            self.frame_filtros,
            values=[
                "Ventas por Período",
                "Inventario Actual",
                "Productos Más Vendidos",
                "Ventas por Cliente",
                "Movimientos de Inventario",
                "Resumen de Pagos"
            ]
        )
        self.tipo_reporte.pack(side="left", padx=5)
        
        # Frame de fechas
        self.frame_fechas = ctk.CTkFrame(self.frame_filtros)
        self.frame_fechas.pack(side="left", padx=5)
        
        # Fecha inicial
        ctk.CTkLabel(self.frame_fechas, text="Desde:").pack(side="left")
        self.fecha_inicio = DateEntry(self.frame_fechas, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.fecha_inicio.pack(side="left", padx=5)
        
        # Fecha final
        ctk.CTkLabel(self.frame_fechas, text="Hasta:").pack(side="left")
        self.fecha_fin = DateEntry(self.frame_fechas, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
        self.fecha_fin.pack(side="left", padx=5)
        
        # Botón generar
        self.btn_generar = ctk.CTkButton(
            self.frame_filtros,
            text="Generar Reporte",
            command=self.generar_reporte
        )
        self.btn_generar.pack(side="left", padx=5)
        
        # Frame para la vista previa
        self.frame_preview = ctk.CTkFrame(self.frame_principal)
        self.frame_preview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview para la vista previa
        self.tree = ttk.Treeview(self.frame_preview)
        self.tree.pack(fill="both", expand=True, pady=5)
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(self.frame_preview, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def generar_reporte(self):
        tipo = self.tipo_reporte.get()
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()
        
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if tipo == "Ventas por Período":
            self._reporte_ventas_periodo(fecha_inicio, fecha_fin)
        elif tipo == "Inventario Actual":
            self._reporte_inventario()
        elif tipo == "Productos Más Vendidos":
            self._reporte_productos_vendidos(fecha_inicio, fecha_fin)
        elif tipo == "Ventas por Cliente":
            self._reporte_ventas_cliente(fecha_inicio, fecha_fin)
        elif tipo == "Movimientos de Inventario":
            self._reporte_movimientos_inventario(fecha_inicio, fecha_fin)
        elif tipo == "Resumen de Pagos":
            self._reporte_pagos(fecha_inicio, fecha_fin)
            
    def _reporte_ventas_periodo(self, fecha_inicio, fecha_fin):
        consulta = """
        SELECT v.id, v.fecha, c.nombre as cliente, v.total,
        GROUP_CONCAT(p.nombre || ' (x' || dv.cantidad || ')') as productos
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN detalles_ventas dv ON v.id = dv.venta_id
        JOIN productos p ON dv.producto_id = p.id
        WHERE v.fecha BETWEEN ? AND ?
        GROUP BY v.id
        """
        resultados = self.db.ejecutar_personalizado(consulta, (fecha_inicio.strftime('%Y-%m-%d'), 
                                                             fecha_fin.strftime('%Y-%m-%d')))
        
        self.tree["columns"] = ("id", "fecha", "cliente", "total", "productos")
        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("total", text="Total")
        self.tree.heading("productos", text="Productos")
        
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        self._exportar_excel("Ventas_por_periodo", resultados)
        
    def _reporte_inventario(self):
        consulta = """
        SELECT p.codigo, p.nombre, p.stock, p.precio, p.categoria
        FROM productos p
        ORDER BY p.categoria, p.nombre
        """
        resultados = self.db.ejecutar_personalizado(consulta)
        
        self.tree["columns"] = ("codigo", "nombre", "stock", "precio", "categoria")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("categoria", text="Categoría")
        
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        self._exportar_excel("Inventario_actual", resultados)
        
    def _reporte_productos_vendidos(self, fecha_inicio, fecha_fin):
        consulta = """
        SELECT p.nombre, SUM(dv.cantidad) as cantidad_vendida,
        SUM(dv.cantidad * dv.precio_unitario) as total_ventas
        FROM detalles_ventas dv
        JOIN productos p ON dv.producto_id = p.id
        JOIN ventas v ON dv.venta_id = v.id
        WHERE v.fecha BETWEEN ? AND ?
        GROUP BY p.id
        ORDER BY cantidad_vendida DESC
        """
        resultados = self.db.ejecutar_personalizado(consulta, (fecha_inicio.strftime('%Y-%m-%d'),
                                                             fecha_fin.strftime('%Y-%m-%d')))
        
        self.tree["columns"] = ("producto", "cantidad", "total")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad Vendida")
        self.tree.heading("total", text="Total Ventas")
        
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        self._exportar_excel("Productos_mas_vendidos", resultados)
        
    def _exportar_excel(self, nombre_archivo, datos):
        if not datos:
            CTkMessagebox(title="Error", message="No hay datos para exportar")
            return
            
        try:
            df = pd.DataFrame(datos)
            ruta_archivo = f"reportes/{nombre_archivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(ruta_archivo, index=False)
            CTkMessagebox(title="Éxito", 
                         message=f"Reporte exportado exitosamente a {ruta_archivo}")
        except Exception as e:
            CTkMessagebox(title="Error",
                         message=f"Error al exportar el reporte: {str(e)}")
            
    def _reporte_ventas_cliente(self, fecha_inicio, fecha_fin):
        consulta = """
        SELECT c.nombre, COUNT(v.id) as num_compras,
        SUM(v.total) as total_compras
        FROM clientes c
        JOIN ventas v ON c.id = v.cliente_id
        WHERE v.fecha BETWEEN ? AND ?
        GROUP BY c.id
        ORDER BY total_compras DESC
        """
        resultados = self.db.ejecutar_personalizado(consulta, (fecha_inicio.strftime('%Y-%m-%d'),
                                                             fecha_fin.strftime('%Y-%m-%d')))
        
        self.tree["columns"] = ("cliente", "compras", "total")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("compras", text="Número de Compras")
        self.tree.heading("total", text="Total Comprado")
        
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        self._exportar_excel("Ventas_por_cliente", resultados)
        
    def _reporte_movimientos_inventario(self, fecha_inicio, fecha_fin):
        consulta = """
        SELECT p.nombre, re.cantidad, re.fecha, re.usuario, re.observacion
        FROM registro_entradas re
        JOIN productos p ON re.producto_id = p.id
        WHERE re.fecha BETWEEN ? AND ?
        ORDER BY re.fecha DESC
        """
        resultados = self.db.ejecutar_personalizado(consulta, (fecha_inicio.strftime('%Y-%m-%d'),
                                                             fecha_fin.strftime('%Y-%m-%d')))
        
        self.tree["columns"] = ("producto", "cantidad", "fecha", "usuario", "observacion")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("observacion", text="Observación")
        
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        self._exportar_excel("Movimientos_inventario", resultados)
        
    def _reporte_pagos(self, fecha_inicio, fecha_fin):
        consulta = """
        SELECT v.fecha, c.nombre as cliente, pv.metodo_pago,
        pv.valor, v.total
        FROM pagos_venta pv
        JOIN ventas v ON pv.venta_id = v.id
        JOIN clientes c ON v.cliente_id = c.id
        WHERE v.fecha BETWEEN ? AND ?
        ORDER BY v.fecha DESC
        """
        resultados = self.db.ejecutar_personalizado(consulta, (fecha_inicio.strftime('%Y-%m-%d'),
                                                             fecha_fin.strftime('%Y-%m-%d')))
        
        self.tree["columns"] = ("fecha", "cliente", "metodo", "valor", "total")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("metodo", text="Método de Pago")
        self.tree.heading("valor", text="Valor Pagado")
        self.tree.heading("total", text="Total Venta")
        
        for row in resultados:
            self.tree.insert("", "end", values=row)
            
        self._exportar_excel("Resumen_pagos", resultados)
root = ctk.CTk()
report_manager = GestorReportes()
root.mainloop()