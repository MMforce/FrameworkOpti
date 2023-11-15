import random
import time
import psutil

def generar_grafo(num_ciudades, distancia_minima, distancia_maxima):
    grafo = [[0] * num_ciudades for _ in range(num_ciudades)]

    for i in range(num_ciudades):
        for j in range(i+1, num_ciudades):
            distancia = random.randint(distancia_minima, distancia_maxima)
            grafo[i][j] = distancia
            grafo[j][i] = distancia

    return grafo

def main():
    random.seed(42) 

    num_ciudades = 30
    distancia_minima = 1
    distancia_maxima = (((num_ciudades * (num_ciudades - 1)) / 2)) 

    grafo = generar_grafo(num_ciudades, distancia_minima, distancia_maxima)
    #print("Grafo:", grafo)

    ciudades_visitadas = [False] * num_ciudades
    ruta_optima = []
    ciudad_actual = 0  #Ciudad de partida

    while len(ruta_optima) < num_ciudades:
        ciudades_visitadas[ciudad_actual] = True
        ruta_optima.append(ciudad_actual)

        ciudad_mas_cercana = None
        distancia_minima = float('inf')

        for i in range(num_ciudades):
            if not ciudades_visitadas[i] and grafo[ciudad_actual][i] < distancia_minima:
                distancia_minima = grafo[ciudad_actual][i]
                ciudad_mas_cercana = i

        ciudad_actual = ciudad_mas_cercana

    ruta_optima.append(0)  #Agregar la ciudad de partida al final para completar el ciclo
    
    #Obtencion de resultados
    
    print("Ruta óptima:", ruta_optima)
    memory_used = process.memory_info().rss / (1024 * 1024) 
    cpu_usage = psutil.cpu_percent()
    termino = time.time()
    tiempoEjecucion = termino - inicio
    print('Tiempo de ejecucion es de:', tiempoEjecucion, 'segundos')
    print(f"Memoria utilizada: {memory_used} MB")
    print(f"Uso de CPU: {cpu_usage}%")

if __name__ == '__main__':
    inicio = time.time() #Inicia tiempo
    process = psutil.Process() 
    main()






