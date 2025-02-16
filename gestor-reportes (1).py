import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SalesReportWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Reporte de Ventas")
        self.window.geometry("1000x600")
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        
        # Create main metrics cards
        self.create_metric_cards()
        
        # Create charts frame
        self.create_charts_frame()
        
        # Create products table
        self.create_products_table()
        
    def create_metric_cards(self):
        # Frame for metric cards
        metrics_frame = ctk.CTkFrame(self.window)
        metrics_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        metrics_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Sales Card
        sales_card = ctk.CTkFrame(metrics_frame, fg_color="#1E90FF")
        sales_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(sales_card, text="Ventas", font=("Arial", 20, "bold"), 
                    text_color="white").pack(pady=5)
        ctk.CTkLabel(sales_card, text="$1,500,000", font=("Arial", 24, "bold"), 
                    text_color="white").pack(pady=5)
        
        # Profit Card
        profit_card = ctk.CTkFrame(metrics_frame, fg_color="#FF1493")
        profit_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(profit_card, text="Utilidad", font=("Arial", 20, "bold"), 
                    text_color="white").pack(pady=5)
        ctk.CTkLabel(profit_card, text="$750,000", font=("Arial", 24, "bold"), 
                    text_color="white").pack(pady=5)
        
        # Expenses Card
        expenses_card = ctk.CTkFrame(metrics_frame, fg_color="#FF8C00")
        expenses_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(expenses_card, text="Gastos", font=("Arial", 20, "bold"), 
                    text_color="white").pack(pady=5)
        ctk.CTkLabel(expenses_card, text="$250,000", font=("Arial", 24, "bold"), 
                    text_color="white").pack(pady=5)
        
    def create_charts_frame(self):
        charts_frame = ctk.CTkFrame(self.window)
        charts_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0,20), sticky="nsew")
        
        # Create payment types donut chart
        fig_donut = Figure(figsize=(5,4))
        ax_donut = fig_donut.add_subplot(111)
        
        # Sample data for donut chart
        payment_types = ['Efectivo', 'Transferencia', 'CXC']
        values = [45, 35, 20]
        colors = ['#87CEEB', '#FFA07A', '#98FB98']
        
        ax_donut.pie(values, labels=payment_types, colors=colors, autopct='%1.1f%%',
                    wedgeprops=dict(width=0.5))
        ax_donut.set_title('Tipos de pagos')
        
        canvas_donut = FigureCanvasTkAgg(fig_donut, master=charts_frame)
        canvas_donut.draw()
        canvas_donut.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        
        # Create bar chart
        fig_bar = Figure(figsize=(6,4))
        ax_bar = fig_bar.add_subplot(111)
        
        # Sample data for bar chart
        categories = ['Categoria 1']
        series_data = [4.3, 2.4, 2.0, 4.3, 2.4]
        x = range(len(categories))
        
        bar_width = 0.15
        for i, data in enumerate(series_data):
            ax_bar.bar([xi + i*bar_width for xi in x], [data], width=bar_width,
                      label=f'Serie {i+1}')
        
        ax_bar.set_xticks([xi + bar_width*2 for xi in x])
        ax_bar.set_xticklabels(categories)
        ax_bar.legend()
        
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=charts_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
        
    def create_products_table(self):
        table_frame = ctk.CTkFrame(self.window)
        table_frame.grid(row=1, column=2, padx=20, pady=(0,20), sticky="nsew")
        
        # Table header
        ctk.CTkLabel(table_frame, text="Top 10 productos más vendidos",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Table headers
        headers_frame = ctk.CTkFrame(table_frame)
        headers_frame.pack(fill="x", padx=10)
        
        ctk.CTkLabel(headers_frame, text="Id", width=50).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(headers_frame, text="Producto", width=150).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(headers_frame, text="Cant", width=50).grid(row=0, column=2, padx=5)
        
        # Sample data rows
        for i in range(10):
            row_frame = ctk.CTkFrame(table_frame)
            row_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(row_frame, text=str(i+1), width=50).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(row_frame, text=f"Producto {i+1}", width=150).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(row_frame, text=str((10-i)*10), width=50).grid(row=0, column=2, padx=5)
# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = SalesReportWindow(root)
    root.mainloop()
