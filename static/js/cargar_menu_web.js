const SERVER_IP = window.location.hostname;
const API_URL = `http://${SERVER_IP}:5000/api/menu_web`;

async function cargarMenu() {
    try {
        let response = await fetch(API_URL);
        let data = await response.json();

        const tabsContainer = document.querySelector(".tabs");
        const contentContainer = document.querySelector(".pedidos-container");

        // Obtener nombres de las categorías
        const categorias = Object.keys(data);

        categorias.forEach((categoria, index) => {
            // Crear pestañas
            const tab = document.createElement("div");
            tab.classList.add("tab");
            if (index === 0) tab.classList.add("active-tab"); // Activa el primero
            tab.textContent = categoria;
            tab.setAttribute("onclick", `openTab(event, '${categoria}')`);
            tabsContainer.appendChild(tab);

            // Crear contenedor de platos para cada categoría
            const div = document.createElement("div");
            div.id = categoria;
            div.classList.add("tab-content");
            if (index === 0) div.classList.add("active"); // Mostrar el primero

            // Obtener los platos de la categoría
            const platos = data[categoria].Platos;
            let platosHtml = `<div class="platos">`; // ✅ Corrección del error aquí
            for (const plato in platos) {
                platosHtml += `<div class="plato-item">
                                    <button class="boton_menos">-</button>
                                    <button class="boton_plato">${plato}</button>
                                    <button class="boton_mas">+</button>
                                </div>`;
            }
            platosHtml += "</div>";

            div.innerHTML = platosHtml;
            contentContainer.appendChild(div);
        });

    } catch (error) {
        console.error("❌ Error al cargar el menú:", error);
    }
}


// Cargar el menú cuando la página se inicie
document.addEventListener("DOMContentLoaded", cargarMenu);
