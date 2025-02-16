from tkinter import Tk, Canvas, Frame, Scrollbar, Entry

def scroll_pixels(canvas, delta_pixels):
    # Obtener las coordenadas actuales del scroll en fracción (0 a 1)
    current_scroll = canvas.yview()[0]
    # Determinar la altura total desplazable
    scroll_region_height = canvas.bbox("all")[3] - canvas.winfo_height()
    # Convertir los píxeles en fracción y aplicar el desplazamiento
    fraction = delta_pixels / scroll_region_height if scroll_region_height > 0 else 0
    canvas.yview_moveto(current_scroll + fraction)

root = Tk()

canvas = Canvas(root, width=300, height=200)
scrollbar = Scrollbar(root, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Contenido del canvas
frame = Frame(canvas)
for i in range(50):
    label = Entry(frame, width=300, bg=f"#{hex(100 + i*3)[2:]}FF{hex(200 - i*3)[2:]}")
    label.pack(fill="both", expand=True)

canvas.create_window((0, 0), window=frame, anchor="nw")
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Vincular el scroll con el canvas
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Prueba del desplazamiento por píxeles
root.bind("<Up>", lambda e: scroll_pixels(canvas, -10))  # Mover 10 píxeles hacia arriba
root.bind("<Down>", lambda e: scroll_pixels(canvas, 10))  # Mover 10 píxeles hacia abajo

root.mainloop()
