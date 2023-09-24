import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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

# Agregar aristas entre nodos si el puntaje de investigación es menor a 10
for i in range(len(universidades)):
    for j in range(i + 1, len(universidades)):
        puntaje1 = puntajes_investigacion[i]
        puntaje2 = puntajes_investigacion[j]
        if abs(puntaje1 - puntaje2) < 1:
            G.add_edge(universidades[i], universidades[j])

# Dibujar el grafo
pos = nx.spring_layout(G, seed=42, k=0.2)  # Layout para la disposición de nodos
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
plt.title("Grafo de Universidades basado en Correlación de Investigación (Puntaje < 10)")
plt.show()
