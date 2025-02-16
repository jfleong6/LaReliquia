import threading
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import tkinter as tk
import requests  # Para que Tkinter pueda comunicarse con Flask

class PedidoAPI:
    def __init__(self):
        self.app = Flask(__name__, static_folder='static', template_folder='templates')
        CORS(self.app)
        self.setup_routes()

    def get_pedidos(self):
        """Devuelve pedidos de prueba o desde la base de datos."""
        return [
            {"Comanda": 6471, "Cliente": "Karol", "Total": 150000},
            {"Comanda": 6459, "Cliente": "Claudia", "Total": 97000}
        ]

    def setup_routes(self):
        """Configura las rutas del servidor Flask."""
        
        @self.app.route('/pedidos', methods=['GET'])
        def pedidos_page():
            return render_template('pedidos.html')

        @self.app.route('/api/pedidos', methods=['GET'])
        def pedidos():
            return jsonify(self.get_pedidos())

        @self.app.route('/api/orden', methods=['POST'])
        def recibir_orden():
            """Recibe una orden desde Tkinter y devuelve una respuesta."""
            data = request.json
            if not data or "comanda" not in data or "cliente" not in data:
                return jsonify({"error": "Datos incompletos"}), 400
            
            # Simulación de procesamiento (aquí podrías guardar en SQLite)
            print(f"Orden recibida: {data}")

            return jsonify({"mensaje": f"Orden {data['comanda']} procesada para {data['cliente']}"}), 200

    def run(self):
        """Ejecuta Flask en un hilo separado."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        """Método privado para iniciar Flask."""
        self.app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


class Interfaz:
    def __init__(self):
        self.ventana1 = tk.Tk()
        self.ventana1.title("Aplicación de Escritorio con Flask")
        self.ventana1.geometry("400x300")

        self.label = tk.Label(self.ventana1, text="Ingrese Orden", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry_comanda = tk.Entry(self.ventana1, width=20)
        self.entry_comanda.insert(0, "Comanda ID")  # Texto por defecto
        self.entry_comanda.pack(pady=5)

        self.entry_cliente = tk.Entry(self.ventana1, width=20)
        self.entry_cliente.insert(0, "Nombre Cliente")
        self.entry_cliente.pack(pady=5)

        self.boton_enviar = tk.Button(self.ventana1, text="Enviar Orden", command=self.enviar_orden)
        self.boton_enviar.pack(pady=10)

        self.label_respuesta = tk.Label(self.ventana1, text="", font=("Arial", 12))
        self.label_respuesta.pack(pady=10)

    def enviar_orden(self):
        """Envía la orden al servidor Flask"""
        comanda = self.entry_comanda.get()
        cliente = self.entry_cliente.get()

        if not comanda.isdigit():
            self.label_respuesta.config(text="Comanda debe ser un número", fg="red")
            return

        orden = {"comanda": int(comanda), "cliente": cliente}

        try:
            response = requests.post("http://127.0.0.1:5000/api/orden", json=orden)
            respuesta = response.json()
            self.label_respuesta.config(text=respuesta.get("mensaje", "Error"), fg="green")
        except Exception as e:
            self.label_respuesta.config(text="Error al conectar con Flask", fg="red")

# Ejecutar Flask en un hilo separado y luego iniciar la interfaz gráfica
if __name__ == '__main__':
    pedidoApi = PedidoAPI()
    pedidoApi.run()  # Inicia Flask en un hilo separado

    aplicacion1 = Interfaz()
    aplicacion1.ventana1.mainloop()  # Mantiene Tkinter funcionando
