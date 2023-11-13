using Random

function generar_grafo(num_ciudades, distancia_minima, distancia_maxima)
    grafo = zeros(Int, num_ciudades, num_ciudades)

    for i in 1:num_ciudades
        for j in i+1:num_ciudades
            distancia = rand(distancia_minima:distancia_maxima)
            grafo[i, j] = distancia
            grafo[j, i] = distancia
        end
    end

    return grafo
end

function tsp()
    Random.seed!(42)  # Fijar la semilla para realizar el mismo experimento

    num_ciudades = 30
    distancia_minima = 1
    distancia_maxima = Int((num_ciudades * (num_ciudades - 1)) / 2)

    grafo = generar_grafo(num_ciudades, distancia_minima, distancia_maxima)

    ciudades_visitadas = falses(num_ciudades)
    ruta_optima = Int[]

    ciudad_actual = 1  # Ciudad de partida

    while length(ruta_optima) < num_ciudades
        ciudades_visitadas[ciudad_actual] = true
        push!(ruta_optima, ciudad_actual)

        ciudad_mas_cercana = nothing
        distancia_minima = Inf

        for i in 1:num_ciudades
            if !ciudades_visitadas[i] && grafo[ciudad_actual, i] < distancia_minima
                distancia_minima = grafo[ciudad_actual, i]
                ciudad_mas_cercana = i
            end
        end

        ciudad_actual = ciudad_mas_cercana
    end

    push!(ruta_optima, 1)  # Agregar la ciudad de partida al final para completar el ciclo
    println("Ruta óptima:", ruta_optima) #se indica la ruta optima
end

tsp()
