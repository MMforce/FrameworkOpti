import random
import pulp
import time
import psutil

# Parámetros
inicio = time.time()
process = psutil.Process()
random.seed(42)  # Semilla para replicar experimento
num_ciudades = 100  # Cantidad de ciudades (modificable)
num_conjuntos = 20  # Cantidad de subconjuntos (modificable)

N = range(1, num_ciudades + 1)
M = range(1, num_conjuntos + 1)

# Costo asociado a cada conjunto (parametro C)
C = {j: random.randint(1, 10) for j in M}

# Matriz de asignación binaria aleatoria (parametro a)
a = {(i, j): random.randint(0, 1) for i in N for j in M}

# Crear el problema de optimización
prob = pulp.LpProblem("SetCoveringProblem", pulp.LpMinimize)

# Variables de decisión binarias
X = {j: pulp.LpVariable("X%d" % j, cat=pulp.LpBinary) for j in M}

# Función objetivo
prob += sum(C[j] * X[j] for j in M), "Cost"

# Restricciones de cobertura
for i in N:
    prob += sum(a[i, j] * X[j] for j in M) >= 1, "Covering_%d" % i

# Resolver el problema
prob.solve()

# Imprimir resultados

print("Estado:", pulp.LpStatus[prob.status])
print("Costo mínimo:", pulp.value(prob.objective))
print("Asignación de conjuntos:")
for j in M:
    if X[j].varValue == 1:
        print("Conjunto", j)

memory_used = process.memory_info().rss / (1024 * 1024) 
cpu_usage = psutil.cpu_percent()
termino = time.time()
tiempoEjecucion = termino - inicio
print('Tiempo de ejecucion es de:', tiempoEjecucion, 'segundos')
print(f"Memoria utilizada: {memory_used} MB")
print(f"Uso de CPU: {cpu_usage}%")