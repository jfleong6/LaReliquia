import tkinter as tk
from tkinter import ttk

class MiAplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview con ítems numerados automáticamente")
        
        # Crear un Treeview con dos columnas: la primera es implícita (#0), la segunda es definida ("nombre")
        self.tree = ttk.Treeview(root, columns=("nombre"), show="headings")
        
        # Definir las cabeceras de las columnas
        self.tree.heading("#1", text="Ítem")    # Primera columna (automática)
        self.tree.heading("nombre", text="Nombre")  # Segunda columna ("nombre")
        
        # Mostrar el Treeview
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Contador de ítems
        self.item_counter = 1

        # Botón para agregar ítems
        btn_agregar = tk.Button(root, text="Agregar ítem", command=self.agregar_item)
        btn_agregar.pack(pady=10)

        # Botón para eliminar el ítem seleccionado
        btn_eliminar = tk.Button(root, text="Eliminar ítem seleccionado", command=self.eliminar_item)
        btn_eliminar.pack(pady=10)

    def agregar_item(self):
        # Código único para cada ítem
        iid = f"item_{self.item_counter}"
        # Insertar el ítem en el Treeview
        self.tree.insert("", "end", iid=iid, values=(self.item_counter, f"Nombre {self.item_counter}"))
        # Incrementar el contador
        self.item_counter += 1

    def eliminar_item(self):
        # Obtener el ítem seleccionado
        seleccionado = self.tree.selection()
        if seleccionado:
            # Eliminar el ítem del Treeview
            self.tree.delete(seleccionado)
            print(f"Ítem {seleccionado} eliminado")

# Crear la ventana principal
root = tk.Tk()

# Iniciar la aplicación
app = MiAplicacion(root)

# Ejecutar la ventana principal
root.mainloop()
