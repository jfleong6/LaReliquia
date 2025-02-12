// Cargar la librería Socket.IO dinámicamente si no está disponible
if (typeof io === 'undefined') {
    let script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.js";
    script.onload = () => conectarSocket();
    document.head.appendChild(script);
} else {
    conectarSocket();
}

function conectarSocket() {
    const SERVER_IP = window.location.hostname;
    const socket = io(`http://${SERVER_IP}:5000`);

    socket.on('actualizar_pedidos', () => {
        console.log("📢 Se ha actualizado la lista de pedidos, recargando...");

        location.reload();
    });
}



async function iniciarPedidos() {
    try {
        const SERVER_IP = window.location.hostname;
        const API_URL = `http://${SERVER_IP}:5000/api/pedidos`;
        let response = await fetch(API_URL);
        let data = await response.json();

        Object.values(data).reverse().forEach(pedido => {
            const pedidoObj = new Pedido(pedido);
            pedidoObj.render();
        });

    } catch (error) {
        console.error("Error al obtener los pedidos:", error);
    }
    openTab("","en_espera")

    
}

document.addEventListener("DOMContentLoaded", iniciarPedidos);


async function imprimir(id, accion) {
    const SERVER_IP = window.location.hostname;
    const API_URL = `http://${SERVER_IP}:5000/api/imprimir`;

    try {
        let response = await fetch(API_URL, {
            method: "POST", // Enviar como POST
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: id, tipo: accion }) // Enviar ID y Acción en JSON
        });

        let data = await response.json();
        console.log(data.mensaje);
        alert(`✔️ ${data.mensaje}`);
    } catch (error) {
        console.error("❌ Error al enviar la impresión:", error);
        alert("❌ Error al enviar la impresión");
    }
}

