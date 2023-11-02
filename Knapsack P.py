import random
import pulp
import psutil
import time

inicio = time.time()
process = psutil.Process()
random.seed(0) 
# Número de elementos (objetos)
num_elementos = 100  # Ejemplo: 10 elementos

# Peso máximo permitido
PESOMAX = 100  # Ejemplo: Peso máximo permitido

# Generar valores y pesos aleatorios para cada elemento
VALOR = {i: random.randint(1, 20) for i in range(1, num_elementos + 1)}
PESO = {i: random.randint(1, 10) for i in range(1, num_elementos + 1)}

# Conjunto que indica el rango para cada elemento
ELEMENTOS = range(1, num_elementos + 1)

# Crea un problema de optimización de maximización
prob = pulp.LpProblem("Knapsack", pulp.LpMaximize)

# Variable binaria que indica si el objeto es tomado o no
take = pulp.LpVariable.dicts("Take", ELEMENTOS, cat=pulp.LpBinary)

# Función objetivo que maximiza el valor total de objetos
prob += pulp.lpSum(VALOR[i] * take[i] for i in ELEMENTOS)

# Restricción de peso
prob += pulp.lpSum(PESO[i] * take[i] for i in ELEMENTOS) <= PESOMAX

# Resuelve el problema
prob.solve()

# Imprime el resultado
if pulp.LpStatus[prob.status] == "Optimal":
    print("Solución óptima encontrada:")
    for i in ELEMENTOS:
        if take[i].value() == 1:
            print(f"Elemento {i} - Valor: {VALOR[i]}, Peso: {PESO[i]}")
else:
    print("No se encontró una solución óptima.")


memory_used = process.memory_info().rss / (1024 * 1024) 
cpu_usage = psutil.cpu_percent()
termino = time.time()
tiempoEjecucion = termino - inicio
print(f"Memoria utilizada: {memory_used} MB")
print(f"Uso de CPU: {cpu_usage}%")
print("tiempo de ejecución: ", tiempoEjecucion, " segundos")