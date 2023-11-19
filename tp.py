import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, Scale, Button, Listbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cargar el archivo CSV
archivo_csv = 'universidades.csv'
df = pd.read_csv(archivo_csv)

# Extraer los nombres de las universidades y los puntajes de investigación
universidades = df.iloc[:, 0].tolist()  # Primera columna (nombres de universidades)
puntajes_investigacion = df.iloc[:, 1].tolist()  # Segunda columna (puntajes de investigación)

# Crear el grafo con NetworkX
G = nx.Graph()

# Agregar nodos al grafo (nombres de universidades)
for universidad in universidades:
    G.add_node(universidad)

# Crear la interfaz de usuario
root = tk.Tk()
root.title("Distancia entre Universidades")

# Información del trabajo
info_trabajo = """
CC194 - Complejidad Algoritmica
Trabajo Final
Seccion WS5D
Profesor: Robert Zubieta Cárdenas
|Analisis de Red de Colaboración entre universidades|

Integrantes:
Miguel Huarcaya Chavez u202116207
Velasquez Chambi Ruben u202117342
Chipoco Mejia Jorge u202210236
"""

# Función para iniciar el programa
def empezar_programa():
    # Destruir el menú inicial
    menu_inicial.destroy()
    
    # Crear el frame principal
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0)
    
    label_universidad1 = ttk.Label(frame, text="Universidad 1:")
    label_universidad1.grid(column=0, row=0)
    
    combo_universidad1 = ttk.Combobox(frame, values=universidades)
    combo_universidad1.grid(column=1, row=0)
    
    label_universidad2 = ttk.Label(frame, text="Universidad 2:")
    label_universidad2.grid(column=0, row=1)
    
    combo_universidad2 = ttk.Combobox(frame, values=universidades)
    combo_universidad2.grid(column=1, row=1)
    
    # Agregar un Scale para el criterio de diferencia
    label_criterio = ttk.Label(frame, text="Criterio de Diferencia:")
    label_criterio.grid(column=0, row=2)
    
    scale_criterio = Scale(frame, from_=0, to=10, orient="horizontal")
    scale_criterio.set(3)  # Valor por defecto
    scale_criterio.grid(column=1, row=2)
    
    # Crear objeto Figure y Axes de matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(column=0, row=4, columnspan=2)
    
    # Lista de universidades y puntajes
    lista_universidades = Listbox(frame, selectmode=tk.SINGLE, height=50, width=50)  # Ajusta el ancho a 40
    lista_universidades.grid(column=2, row=0, rowspan=5, padx=10)
    
    # Función para llenar la lista de universidades y puntajes
    def llenar_lista():
        lista_universidades.delete(0, tk.END)  # Limpiar la lista

        # Obtener las universidades del grafo actual
        universidades_grafo = G.nodes

        for universidad in universidades_grafo:
            if universidad in G.nodes:
                puntaje = puntajes_investigacion[universidades.index(universidad)]
                lista_universidades.insert(tk.END, f"{universidad}: {puntaje}")

    # Función para dibujar el grafo
    def dibujar_grafo():
        ax.clear()
        pos = nx.spring_layout(G, seed=42, k=0.2)
        labels = {universidad: f"{universidad}\n{puntajes_investigacion[universidades.index(universidad)]}" for universidad in G.nodes}
        nx.draw(G, pos, ax=ax, with_labels=False, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='black')
        ax.set_title("Grafo de Universidades basado en Correlación de Investigación (Puntaje < 1)")
        llenar_lista()  # Llenar la lista de universidades
        canvas.draw()

    # Función para dibujar el grafo seleccionado
    def dibujar_grafo_seleccionado():
        ax.clear()
        universidad1 = combo_universidad1.get()
        universidad2 = combo_universidad2.get()

        # Obtener el criterio de diferencia desde el Scale
        criterio_diferencia = scale_criterio.get()

        # Crear un nuevo grafo solo con las dos universidades seleccionadas y sus aristas
        selected_nodes = nx.shortest_path(G, source=universidad1, target=universidad2, weight=f'w<{criterio_diferencia}')
        selected_graph = G.subgraph(selected_nodes)

        pos = nx.spring_layout(selected_graph, seed=42, k=0.2)
        labels = {universidad: f"{universidad}\n{puntajes_investigacion[universidades.index(universidad)]}" for universidad in selected_graph.nodes}
        nx.draw(selected_graph, pos, ax=ax, with_labels=False, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
        nx.draw_networkx_labels(selected_graph, pos, labels=labels, font_size=8, font_color='black')
        ax.set_title(f"Grafo entre {universidad1} y {universidad2}")

        # Llenar la lista de universidades después de dibujar el grafo
        llenar_lista()

        canvas.draw()
        
    # Función para actualizar el grafo según el criterio de diferencia
    def actualizar_grafo():
        ax.clear()

        # Obtener el criterio de diferencia desde el Scale
        criterio_diferencia = scale_criterio.get()

        # Limpiar todas las aristas anteriores
        G.remove_edges_from(list(G.edges))

        # Agregar aristas al grafo con el nuevo criterio de diferencia
        for i in range(len(universidades)):
            for j in range(i + 1, len(universidades)):
                puntaje1 = puntajes_investigacion[i]
                puntaje2 = puntajes_investigacion[j]
                if abs(puntaje1 - puntaje2) < criterio_diferencia:
                    G.add_edge(universidades[i], universidades[j], w=abs(puntaje1 - puntaje2))

        # Dibujar el nuevo grafo
        pos = nx.spring_layout(G, seed=42, k=0.2)
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=100, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', width=0.5)
        ax.set_title(f"Grafo actualizado (Criterio: < {criterio_diferencia})")
        llenar_lista()  # Llenar la lista de universidades
        canvas.draw()
    
    # Función para salir del programa
    def salir_programa():
        root.destroy()
    
    # Función para calcular la distancia entre dos universidades utilizando BFS
    def calcular_distancia():
        universidad1 = combo_universidad1.get()
        universidad2 = combo_universidad2.get()

        if universidad1 == universidad2:
            resultado.set("Las universidades son iguales")
        else:
            # Obtener el criterio de diferencia desde el Scale
            criterio_diferencia = scale_criterio.get()

            # Calcular la distancia
            distancia = nx.shortest_path_length(G, source=universidad1, target=universidad2, weight=f'w<{criterio_diferencia}')
            resultado.set(f"Distancia entre {universidad1} y {universidad2}: {distancia} saltos")
            dibujar_grafo_seleccionado()

    # Botón para calcular la distancia
    boton_calcular = ttk.Button(frame, text="Calcular Distancia", command=calcular_distancia)
    boton_calcular.grid(column=0, row=3, columnspan=2, pady=10)

    # Botón para actualizar el grafo
    boton_actualizar_grafo = Button(frame, text="Actualizar Grafo", command=actualizar_grafo, height=2, width=15)
    boton_actualizar_grafo.grid(column=0, row=5, columnspan=2)
    
    # Botón para salir del programa
    boton_salir = ttk.Button(frame, text="Salir", command=salir_programa, width=20, padding=(10, 10))
    boton_salir.grid(column=0, row=7, pady=10)

    # Etiqueta para mostrar el resultado
    resultado = tk.StringVar()
    label_resultado = ttk.Label(frame, textvariable=resultado)
    label_resultado.grid(column=0, row=6, columnspan=2)

    # Llenar las opciones de los Combobox con las universidades
    combo_universidad1['values'] = universidades
    combo_universidad2['values'] = universidades
    
    combo_universidad1.config(width=35)  # Ajusta el ancho a 35
    combo_universidad2.config(width=35)  # Ajusta el ancho a 35

    # Iniciar la interfaz gráfica
    dibujar_grafo()

# Crear el menú inicial
menu_inicial = tk.Toplevel(root)
menu_inicial.title("Menú Inicial")

# Etiqueta con la información del trabajo
label_info_trabajo = ttk.Label(menu_inicial, text=info_trabajo, wraplength=500, font=("Arial", 12), justify="center")
label_info_trabajo.place(relx=0.5, rely=0.5, anchor="center")


# Botón para empezar el programa
boton_empezar = ttk.Button(menu_inicial, text="Empezar", command=empezar_programa, width=20, padding=(10, 10))
boton_empezar.place(relx=0.5, rely=0.8, anchor="center")


# Ajustar el tamaño de la ventana del menú inicial
menu_inicial.geometry("600x600")

# Centrar la ventana del menú inicial en la pantalla
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
menu_inicial.geometry(f"+{x}+{y}")

# Iniciar el bucle principal de la aplicación
root.mainloop()