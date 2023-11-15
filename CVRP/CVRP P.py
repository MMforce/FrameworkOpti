import pulp
import random
import time
import psutil

inicio = time.time()
process = psutil.Process()
#Definición de los datos del problema de manera aleatoria
random.seed(0)  #Para repetir experimento
num_nodos = 30  #Número de nodos, puedes cambiarlo
nodos = list(range(1, num_nodos + 1))
capacidad = 20
demanda = {i: random.randint(1, 5) for i in nodos}
distancia = {i: {j: random.randint(1, 10) for j in nodos} for i in nodos}

#Creación del problema de optimización
prob = pulp.LpProblem("CVRP", pulp.LpMinimize)

#Variables de decisión
x = pulp.LpVariable.dicts("x", [(i, j) for i in nodos for j in nodos], cat=pulp.LpBinary)
u = pulp.LpVariable.dicts("u", nodos, lowBound=0)

#Función objetivo: Minimizar la distancia total
prob += pulp.lpSum(distancia[i][j] * x[(i, j)] for i in nodos for j in nodos)

#Restricciones
for i in nodos:
    prob += pulp.lpSum(x[(i, j)] for j in nodos if j != i) == 1  # Cada nodo se visita exactamente una vez
    prob += pulp.lpSum(demanda[j] * x[(j, i)] for j in nodos if j != i) <= u[i]  # Capacidad de los vehículos
    prob += u[i] <= capacidad  # Capacidad máxima de los vehículos

#Evitar subrutas
for i in nodos:
    for j in nodos:
        if i != j and i != 1 and j != 1:
            prob += u[i] - u[j] + capacidad * x[(i, j)] <= capacidad - demanda[j]


#Resolver el problema
prob.solve()

memory_used = process.memory_info().rss / (1024 * 1024) 
cpu_usage = psutil.cpu_percent()
termino = time.time()
tiempoEjecucion = termino - inicio
print(f"Memoria utilizada: {memory_used} MB")
print(f"Uso de CPU: {cpu_usage}%")
print("tiempo de ejecución: ", tiempoEjecucion, " segundos")

