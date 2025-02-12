function loadPage(page) {
    fetch(page)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar la página: ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById("page_pedidos").innerHTML = html;
        })
        .catch(error => {
            console.error("Error cargando la página:", error);
        });
}
