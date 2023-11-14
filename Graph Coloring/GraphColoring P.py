import time
import random
import psutil

class Grafo:
    def __init__(self, edges, n):
        self.adjList = [[] for _ in range(n)]

        # agrega bordes al grafo no dirigido
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.adjList[dest].append(src)


# Función para asignar colores a los vértices de un grafo
def colorGrafo(grafo, n):

    # realiza un seguimiento del color asignado a cada vértice
    resultado = {}

    # asigna un color a los vértices uno por uno
    for u in range(n):

        # verifica los colores de los vértices adyacentes de `u` y los almacena en un conjunto
        asignacion = set([resultado.get(i) for i in grafo.adjList[u] if i in resultado])

        # comprueba el primer color libre
        color = 1
        for c in asignacion:
            if color != c:
                break
            color = color + 1

        # asigna al vértice u el primer color disponible
        resultado[u] = color

    for v in range(n):
        print(f'Color asignado al vértice {v} es {colores[resultado[v]]}')


if __name__ == '__main__':
    inicio = time.time()
    process = psutil.Process()

    # Fijar una semilla para generar números aleatorios consistentes
    seed_value = 123
    random.seed(seed_value)

    # Lista de aristas de grafo según el diagrama anterior
    aristas = []

    # Generar vertices de manera aleatoria
    num_vertices = 16 # Número total de vertices

    colores = []
    for i in range(0, num_vertices-1):
        colores.append(i)
    
    num_bordes = int(((num_vertices * (num_vertices - 1))/2) ) # Número total de bordes

    for _ in range(num_bordes):
        src = random.randint(0, num_vertices - 1)
        dest = random.randint(0, num_vertices - 1)
        aristas.append((src, dest))

    # número total de nodos en el grafo
    n = num_vertices
    
    # construye un grafo a partir de los bordes dados
    grafo = Grafo(aristas, n)

    # Grafo de color usando el algoritmo greedy
    colorGrafo(grafo, n)


termino = time.time()
tiempoEjecucion = termino - inicio
memory_used = process.memory_info().rss / (1024 * 1024) 
cpu_usage = psutil.cpu_percent()
print('Tiempo de ejecucion es de:', tiempoEjecucion, 'segundos')
print(f"Memoria utilizada: {memory_used} MB")
print(f"Uso de CPU: {cpu_usage}%")
#print("La cantidad de vertices son: ", vert)