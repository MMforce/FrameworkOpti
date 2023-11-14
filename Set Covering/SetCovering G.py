import random
import gurobipy as gp
from gurobipy import GRB
import time
import psutil

# Parámetros
inicio = time.time()
process = psutil.Process()
random.seed(42)  # Semilla para replicar experimento
num_ciudades = 100 # Cantidad de ciudades (modificable)
num_conjuntos = 10  # Cantidad de subconjuntos (modificable)

N = range(1, num_ciudades + 1)
M = range(1, num_conjuntos + 1)

# Costo asociado a cada conjunto (parametro C)
C = {j: random.randint(1, 10) for j in M}

# Matriz de asignación binaria aleatoria (parametro a)
a = {(i, j): random.randint(0, 1) for i in N for j in M}

# Crear el modelo
model = gp.Model("SetCoveringProblem")

# Variables de decisión binarias
X = model.addVars(M, vtype=GRB.BINARY, name="X")

# Función objetivo
model.setObjective(sum(C[j] * X[j] for j in M), GRB.MINIMIZE)

# Restricciones de cobertura
for i in N:
    model.addConstr(sum(a[i, j] * X[j] for j in M) >= 1, f"Covering_{i}")

# Resolver el modelo
model.optimize()

# Imprimir resultados
print("Costo mínimo:", model.objVal)
memory_used = process.memory_info().rss / (1024 * 1024)
cpu_usage = psutil.cpu_percent()
termino = time.time()
tiempoEjecucion = termino - inicio
print('Tiempo de ejecucion es de:', tiempoEjecucion, 'segundos')
print(f"Memoria utilizada: {memory_used} MB")
print(f"Uso de CPU: {cpu_usage}%")
