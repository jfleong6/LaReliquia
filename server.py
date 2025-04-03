from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO  # Importamos Flask-SocketIO
import threading
import asyncio


class PedidoAPI:
    def __init__(self, app_principal):
        self.app = Flask(__name__, static_folder='static', template_folder='templates')
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")  # Agregar soporte para WebSockets
        self.app_principal = app_principal          # Instancia de la aplicación
        self.setup_routes()

    def get_pedidos(self):
        """Obtiene los pedidos desde la aplicación principal"""
        return self.app_principal.enviar_pedidos_web()
    
    def get_menu_web(self):
        """Obtiene los pedidos desde la aplicación principal
        menu_web =self.app_principal.enviar_categorias_platos_web()
        for categoria in menu_web:
            print(f"{categoria.center(20," ")}:\tCodigo: {menu_web[categoria]["Codigo"]}")
        """
        return self.app_principal.enviar_categorias_platos_web()

    def setup_routes(self):
        """Configura las rutas del servidor Flask."""
        
        @self.app.route('/pedidos', methods=['GET'])
        def pedidos_page():
            return render_template('pedidos.html')
        @self.app.route('/nuevo_pedido', methods=['GET'])
        def nuevo_pedido_page():
            return render_template('nuevo_pedido.html')

        @self.app.route('/api/pedidos', methods=['GET'])
        def pedidos():
            return jsonify(self.get_pedidos())
        
        @self.app.route('/api/menu_web', methods=['GET'])
        def menu_web():
            
            return jsonify(self.get_menu_web())

        @self.app.route('/api/actualizar_pedidos', methods=['POST'])
        def actualizar_pedidos():
            """Recibe una actualización de pedidos y notifica a todas las páginas abiertas."""
            self.socketio.emit('actualizar_pedidos')  # Notifica a todos los clientes
            return jsonify({"mensaje": "Pedidos actualizados"}), 200
        
        @self.app.route('/api/imprimir', methods=['POST'])
        def imprimir_pedido():
            """Recibe un ID y un tipo de impresión ('Cocina' o 'Recepción') y lo imprime en consola"""
            data = request.json  # Recibe los datos en formato JSON

            # Verificar que los parámetros requeridos estén presentes
            if "id" not in data or "tipo" not in data:
                return jsonify({"error": "Faltan parámetros 'id' y 'tipo'"}), 400

            pedido_id = data["id"]
            tipo_impresion = data["tipo"]

            # Simulación de impresión
            print(f"🖨️ Imprimiendo pedido #{pedido_id} para {tipo_impresion}...")
            self.app_principal.imprimir_desde_web(pedido_id,tipo_impresion)

            return jsonify({"mensaje": f"Pedido {pedido_id} enviado a impresión para {tipo_impresion}"}), 200         

    def run(self):
        """Ejecuta Flask con soporte para WebSockets en un hilo separado."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        """Método privado para iniciar Flask con SocketIO."""
        self.socketio.run(self.app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Si este script se ejecuta directamente, iniciar el servidor
if __name__ == '__main__':
    api = PedidoAPI()
    api.run()
