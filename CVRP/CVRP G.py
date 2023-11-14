import random
import time
import gurobipy as gp
import psutil
from gurobipy import GRB

#varialbe que mide tiempo de inicio
inicio = time.time()
process = psutil.Process()

# Definición de los datos del problema de manera aleatoria
random.seed(0)  # Para repetir experimento
num_nodos = 6 # Número de nodos que puede ser modificado
nodos = list(range(1, num_nodos + 1))
capacidad = 20
demanda = {i: random.randint(1, 5) for i in nodos}
distancia = {i: {j: random.randint(1, 10) for j in nodos} for i in nodos}

# Creación del modelo
modelo = gp.Model("CVRP")

# Variables de decisión
x = {}
for i in nodos:
    for j in nodos:
        if i != j:
            x[i, j] = modelo.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}')

u = modelo.addVars(nodos, lb=0, name='u')

# Función objetivo: Minimizar la distancia total
modelo.setObjective(gp.quicksum(distancia[i][j] * x[i, j] for i in nodos for j in nodos if i != j), GRB.MINIMIZE)

# Restricciones
for i in nodos:
    modelo.addConstr(gp.quicksum(x[i, j] for j in nodos if j != i) == 1, name=f'visita_unica_{i}')
    modelo.addConstr(gp.quicksum(demanda[j] * x[j, i] for j in nodos if j != i) <= u[i], name=f'capacidad_{i}')
    modelo.addConstr(u[i] <= capacidad, name=f'capacidad_maxima_{i}')

# Evitar subrutas
for i in nodos:
    for j in nodos:
        if i != j and i != 1 and j != 1:
            modelo.addConstr(u[i] - u[j] + capacidad * x[i, j] <= capacidad - demanda[j], name=f'evitar_subrutas_{i}_{j}')

# Optimizar el modelo
modelo.optimize()

# Liberar recursos
modelo.dispose()
memory_used = process.memory_info().rss / (1024 * 1024) 
cpu_usage = psutil.cpu_percent()
termino = time.time()
tiempoEjecucion = termino - inicio
print(f"Memoria utilizada: {memory_used} MB")
print(f"Uso de CPU: {cpu_usage}%")
print("tiempo de ejecución: ", tiempoEjecucion, " segundos")
