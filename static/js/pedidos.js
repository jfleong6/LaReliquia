class Pedido {
    constructor(data) {
      this.comanda = data.Comanda;
      this.fecha = data.Fecha;
      this.mesero = data.Mesero;
      this.mesa = data.Mesa;
      this.hora = data.hora;
      this.tipoCliente = data.TipoCliente;
      this.cliente = data.cliente;
      this.cantidad = data.cantidad;
      this.categoria = data.categoria;
      this.subCant = data.SubCant;
      this.descripcion = data.descripcion;
      this.pagos = data.pagos;
      this.total = data.Total;
      this.tipoPago = data.TipoPago;
      this.activo = data.Activo;
    }
  
    obtenerColorEstado() {
      switch (this.activo) {
          case 2:
              return { estado: 'en_mesa', color: 'green' }; // Pedido en mesa
          case 1:
              return { estado: 'en_espera', color: '#fdef42' }; // Pedido en espera
          case 0:
              return { estado: 'por_finalizar', color: 'grey' }; // Pedido por pagar
          default:
              return { estado: 'desconocido', color: 'white' };
      }
  }
  
  
  render() {

    const { estado, color } = this.obtenerColorEstado();
    const pedidoDiv = document.createElement('div');
    pedidoDiv.classList.add('pedido');

    pedidoDiv.innerHTML = `
        <div class = "titulo_y_boton">
          <h2 class='titulo_comanda'>${this.comanda} </h2>
          <a href ="#" class = "boton_mas menu-trigger" onclick="mostrarMenu(event, this)">㊂</a>
        </div>
        <ul id="menu-flotante" class="menu">
            <li onclick="accion(${this.comanda},'Cocina')">Imprimir Cocina</li>
            <li onclick="accion(${this.comanda},'Recepcion')">Imprimir Recepcion</li>
        </ul>
        
        <p><strong>${this.tipoCliente}</strong> ${this.cliente ? this.cliente : ''}</p>
        <p><strong>Mesa:</strong> ${this.mesa}</p>

        ${this.generarDetallePedido()}
        <p><strong>${this.mesero}</strong></p>
        <p><strong>${this.tipoPago}</strong></p>
        <p><strong>TOTAL $ ${this.total.toLocaleString()}</p>`;

    // Aplicar color al título de la comanda
    const titulo = pedidoDiv.querySelector(".titulo_comanda");
    if (titulo) {
        titulo.style.backgroundColor = color;
    }

    // Ubicar el pedido en el div correspondiente al estado
    const contenedorEstado = document.getElementById(estado);
    
    if (contenedorEstado) {
        contenedorEstado.appendChild(pedidoDiv);
        
    } else {
        console.log(`No se encontró un contenedor para el estado: ${estado}`);
    }

    return pedidoDiv;
  }

  
    generarDetallePedido() {
      return this.categoria.map((cat, i) => {
        let items = this.descripcion[i].map((desc, j) => `<div class = 'descripcion'><p>${this.subCant[i][j]} ${desc}</p></div>`).join('');
        return `<div class='categoria'><p><strong>${this.cantidad[i]}</p><p>${cat}</p></strong></div>${items}`
      }).join('');
    }
  }
function openTab(event, tabName) {
  console.log(tabName)
  let contents = document.querySelectorAll(".tab-content");
  let tabs = document.querySelectorAll(".tab");

  contents.forEach(content => content.classList.remove("active"));
  tabs.forEach(tab => tab.classList.remove("active-tab"));

  document.getElementById(tabName).classList.add("active");
  event.currentTarget.classList.add("active-tab");
}
7
function mostrarMenu(event, elemento) {
  console.log("hola");
  event.preventDefault(); // Evita que el enlace navegue

  const pedidoDiv = elemento.closest('.pedido'); // Encuentra el contenedor del pedido
  const menu = pedidoDiv.querySelector(".menu"); // Busca el menú dentro del pedido

  if (menu) {
      const rect = elemento.getBoundingClientRect();
      const menuWidth = 150; // Ancho estimado del menú
      const menuHeight = menu.offsetHeight || 100; // Altura estimada

      let left = rect.left + window.scrollX;
      let top = rect.bottom + window.scrollY;

      // 📌 Evitar que el menú se salga por el lado derecho
      if (left + menuWidth > window.innerWidth) {
          left = window.innerWidth - menuWidth - 10; // Ajustar al borde derecho
      }

      // 📌 Evitar que el menú se salga por la parte inferior
      if (top + menuHeight > window.innerHeight) {
          top = rect.top + window.scrollY - menuHeight; // Mostrar arriba del botón
      }

      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
      menu.style.display = "block";
  }
}

// 📌 Cerrar cualquier menú al hacer clic fuera
document.addEventListener("click", function (event) {
  document.querySelectorAll(".menu").forEach(menu => {
      if (!menu.contains(event.target) && !event.target.classList.contains("menu-trigger")) {
          menu.style.display = "none";
      }
  });
});


function accion(id, opcion) {
  imprimir(id,opcion)
  document.getElementById("menu-flotante").style.display = "none";
}