import random
import time
import psutil
import gurobipy as gp
from gurobipy import GRB

def generar_grafo(num_ciudades, distancia_minima, distancia_maxima):
    grafo = [[0] * num_ciudades for _ in range(num_ciudades)]

    for i in range(num_ciudades):
        for j in range(i+1, num_ciudades):
            distancia = random.randint(distancia_minima, distancia_maxima)
            grafo[i][j] = distancia
            grafo[j][i] = distancia

    return grafo

def resolver_tsp(num_ciudades, grafo):
    try:
        #Crear modelo
        modelo = gp.Model("TSP")

        #Crear variables binarias para representar si se visita cada ciudad
        visitar = {}
        for i in range(num_ciudades):
            for j in range(num_ciudades):
                if i != j:
                    visitar[i, j] = modelo.addVar(vtype=GRB.BINARY, name=f"visitar_{i}_{j}")

        #Función objetivo: minimizar la distancia total
        modelo.setObjective(gp.quicksum(grafo[i][j] * visitar[i, j] for i in range(num_ciudades) for j in range(num_ciudades) if i != j), GRB.MINIMIZE)

        #Restricciones: cada ciudad debe ser visitada exactamente una vez
        for i in range(num_ciudades):
            modelo.addConstr(gp.quicksum(visitar[i, j] for j in range(num_ciudades) if i != j) == 1)

        #Restricciones: no se pueden hacer subciclos
        subciclo = {}
        for i in range(num_ciudades):
            for j in range(num_ciudades):
                if i != j:
                    subciclo[i, j] = modelo.addVar(vtype=GRB.CONTINUOUS, lb=2.0, ub=num_ciudades, name=f"subciclo_{i}_{j}")

        for i in range(num_ciudades):
            for j in range(num_ciudades):
                if i != j:
                    modelo.addConstr(subciclo[i, j] >= visitar[i, j] + 1 - (num_ciudades - 1) * (1 - visitar[i, j]))

        #Resolver el modelo
        modelo.optimize()

        if modelo.status == GRB.OPTIMAL:
            ruta_optima = [0]
            ciudad_actual = 0
            while True:
                for j in range(num_ciudades):
                    if j != ciudad_actual and visitar[ciudad_actual, j].X == 1:
                        ruta_optima.append(j)
                        ciudad_actual = j
                        break
                if ciudad_actual == 0:
                    break

            return ruta_optima

    except gp.GurobiError as e:
        print(f"Error de Gurobi: {e}")
        return None

def main():
    num_ciudades = 10
    distancia_minima = 1
    distancia_maxima = (((num_ciudades * (num_ciudades - 1)) / 2)) 

    grafo = generar_grafo(num_ciudades, distancia_minima, distancia_maxima)
    ruta_optima = resolver_tsp(num_ciudades, grafo)

    #En caso de obtener ruta optima, se obtienen datos de estudio
    if ruta_optima:
        memory_used = process.memory_info().rss / (1024 * 1024) 
        cpu_usage = psutil.cpu_percent()
        termino = time.time()
        tiempoEjecucion = termino - inicio
        print("Ruta óptima:", ruta_optima)
        print('Tiempo de ejecucion es de:', tiempoEjecucion, 'segundos')
        print(f"Memoria utilizada: {memory_used} MB")
        print(f"Uso de CPU: {cpu_usage}%")

    else:
        print("No se logró encontrar ruta óptima")

if __name__ == '__main__':
    inicio = time.time()
    process = psutil.Process()
    main()
