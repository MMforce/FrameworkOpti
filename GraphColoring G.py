import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import random
import time
import psutil

# Limitación de 20 nodos
def solve_graph_coloring(graph):
    
    # Crear el modelo
    model = gp.Model('graph_coloring')

    # Variables de decisión
    nodes = list(graph.nodes())
    num_colors = len(nodes)
    colors = range(num_colors)
    x = model.addVars(nodes, colors, vtype=GRB.BINARY, name='x')

    # Restricción: cada nodo tiene exactamente un color asignado
    model.addConstrs((x.sum(node, '*') == 1 for node in nodes), name='assign_one_color')

    # Restricción: dos nodos adyacentes no pueden tener el mismo color
    model.addConstrs((x[node1, color] + x[node2, color] <= 1
                     for node1, node2 in graph.edges() for color in colors), name='different_colors')

    # Función objetivo: minimizar el número de colores utilizados
    model.setObjective(x.sum(), GRB.MINIMIZE)

    # Resolver el modelo
    model.optimize()

    # Obtener la solución
    if model.status == GRB.OPTIMAL:
        solution = {}
        for node in nodes:
            for color in colors:
                if x[node, color].x > 0.5:
                    solution[node] = color
                    break
        return solution
    else:
        return None

# Función base
if __name__ == '__main__':
    inicio = time.time()
    # Establecer la semilla aleatoria (replicar modelo)
    process = psutil.Process()
    random.seed(42)

    # Generan arcos aleatorios, utilizando como referencia el número de vértices
    numero_vertices = 3
    numero_arcos = int((numero_vertices - 1) * numero_vertices / 2)
    graph = nx.gnm_random_graph(numero_vertices, numero_arcos)


    # Resolver el problema de coloración de grafos
    solution = solve_graph_coloring(graph)

    # Calcular el tiempo de ejecución
    termino = time.time()
    tiempoEjecucion = termino - inicio

    # Imprimir el grafo, la solución y el tiempo de ejecución
    print('Arcos:', graph.edges())
    memory_used = process.memory_info().rss / (1024 * 1024) 
    cpu_usage = psutil.cpu_percent()
    print(f"Memoria utilizada: {memory_used} MB")
    print(f"Uso de CPU: {cpu_usage}%")
    print('Solución:', solution)
    print('Tiempo de ejecución:', tiempoEjecucion, 'segundos')
    
