import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cargar el archivo CSV
archivo_csv = 'universidades.csv'
df = pd.read_csv(archivo_csv)

# Extraer los nombres de las universidades y los puntajes de investigación
universidades = df.iloc[:, 0]  # Primera columna (nombres de universidades)
puntajes_investigacion = df.iloc[:, 1]  # Segunda columna (puntajes de investigación)

# Crear el grafo con NetworkX
G = nx.Graph()

# Agregar nodos al grafo (nombres de universidades)
for universidad in universidades:
    G.add_node(universidad)

# Agregar aristas entre nodos 
for i in range(len(universidades)):
    for j in range(i + 1, len(universidades)):
        puntaje1 = puntajes_investigacion[i]
        puntaje2 = puntajes_investigacion[j]
        if abs(puntaje1 - puntaje2) < 3:
            G.add_edge(universidades[i], universidades[j])

# Función para dibujar el grafo
def dibujar_grafo():
    pos = nx.spring_layout(G, seed=42, k=0.2)  # Layout para la disposición de nodos
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
    plt.title("Grafo de Universidades basado en Correlación de Investigación (Puntaje < 1)")
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(column=0, row=4, columnspan=2)

# Función para calcular la distancia entre dos universidades utilizando BFS
def calcular_distancia():
    universidad1 = combo_universidad1.get()
    universidad2 = combo_universidad2.get()
    
    if universidad1 == universidad2:
        resultado.set("Las universidades son iguales")
    else:
        distancia = nx.shortest_path_length(G, source=universidad1, target=universidad2)
        resultado.set(f"Distancia entre {universidad1} y {universidad2}: {distancia} saltos")

# Crear la interfaz de usuario
root = tk.Tk()
root.title("Distancia entre Universidades")

frame = ttk.Frame(root)
frame.grid(column=0, row=0)

label_universidad1 = ttk.Label(frame, text="Universidad 1:")
label_universidad1.grid(column=0, row=0)
combo_universidad1 = ttk.Combobox(frame, values=list(universidades))
combo_universidad1.grid(column=1, row=0)

label_universidad2 = ttk.Label(frame, text="Universidad 2:")
label_universidad2.grid(column=0, row=1)
combo_universidad2 = ttk.Combobox(frame, values=list(universidades))
combo_universidad2.grid(column=1, row=1)

boton_calcular = ttk.Button(frame, text="Calcular Distancia", command=calcular_distancia)
boton_calcular.grid(column=0, row=2, columnspan=2)

resultado = tk.StringVar()
label_resultado = ttk.Label(frame, textvariable=resultado)
label_resultado.grid(column=0, row=3, columnspan=2)

# Llamar a la función para dibujar el grafo
dibujar_grafo()

root.mainloop()
