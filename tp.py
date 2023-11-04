import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import community 

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

# Agregar aristas entre nodos si el puntaje de investigación es menor a 1
for i in range(len(universidades)):
    for j in range(i + 1, len(universidades)):
        puntaje1 = puntajes_investigacion[i]
        puntaje2 = puntajes_investigacion[j]
        if abs(puntaje1 - puntaje2) < 0.1:
            G.add_edge(universidades[i], universidades[j])

# Dibujar el grafo
pos = nx.spring_layout(G, seed=42, k=0.2)  # Layout para la disposición de nodos
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
plt.title("Grafo de Universidades basado en Correlación de Investigación (Puntaje < 1)")
plt.show()

def detect_communities():
    criterion = float(criterion_entry.get())
    G.clear()
    for i in range(len(universidades)):
        for j in range(i + 1, len(universidades)):
            puntaje1 = puntajes_investigacion[i]
            puntaje2 = puntajes_investigacion[j]
            if abs(puntaje1 - puntaje2) < criterion:
                G.add_edge(universidades[i], universidades[j])
    # Dibujar el grafo actualizado
    pos = nx.spring_layout(G, seed=42, k=0.2)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
    plt.title("Grafo de Universidades basado en Correlación de Investigación (Puntaje < {})".format(criterion))
    plt.show()

    communities = detect_communities_in_graph(G)
    result_text = "Comunidades detectadas:\n"
    for community_id, nodes in communities.items():
        result_text += f"Comunidad {community_id + 1}: {', '.join(nodes)}\n"
    result_textbox.delete(1.0, tk.END)  # Borrar el contenido anterior
    result_textbox.insert(tk.END, result_text)

def detect_communities_in_graph(graph):
    partition = community.best_partition(graph)
    communities = {}
    for node, community_id in partition.items():
        if community_id not in communities:
            communities[community_id] = [node]
        else:
            communities[community_id].append(node)
    return communities

# Crear la ventana principal
root = tk.Tk()
root.title("Detección de Comunidades en Universidades")

# Crear un marco para el formulario
frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10)

# Caja de texto para el criterio del puntaje de investigación
criterion_label = ttk.Label(frame, text="Criterio de Puntaje de Investigación:")
criterion_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
criterion_entry = ttk.Entry(frame)
criterion_entry.grid(column=1, row=0, padx=5, pady=5)
criterion_entry.insert(0, "1.0")  # Valor inicial por defecto

# Botón para detectar comunidades y actualizar el grafo
detect_button = ttk.Button(frame, text="Detectar Comunidades y Actualizar Grafo", command=detect_communities)
detect_button.grid(column=0, row=1, columnspan=2, padx=5, pady=10)

# Textbox para mostrar el resultado
result_textbox = tk.Text(frame, wrap=tk.WORD, width=250, height=50)
result_textbox.grid(column=0, row=2, padx=5, pady=10)

root.mainloop()

