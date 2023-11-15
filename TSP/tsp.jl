using Random
using Printf

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

function tsp(num_ciudades)
    Random.seed!(42)  #Fijar la semilla para realizar el mismo experimento

    distancia_minima = 1
    distancia_maxima = Int((num_ciudades * (num_ciudades - 1)) / 2)

    grafo = generar_grafo(num_ciudades, distancia_minima, distancia_maxima)

    ciudades_visitadas = falses(num_ciudades)
    ruta_optima = Int[]

    ciudad_actual = 1  #Ciudad de partida

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

    push!(ruta_optima, 1)  #Agregar la ciudad de partida al final para completar el ciclo
    
    return ruta_optima
end

#Almacenar datos en listas
tiempos_ejecucion = Float64[]
ram_utilizada_mb = Float64[]

#Medir el tiempo de ejecución para diferentes números de ciudades
for num_ciudades in 3:30
    #println("Número de ciudades:", num_ciudades)
    
    #Medir el tiempo de ejecución
    tiempo = @elapsed begin
        tsp(num_ciudades)
    end
    push!(tiempos_ejecucion, tiempo)
    
    #Medir la RAM utilizada
    #ram = Sys.free_memory() / 1024^2
    #push!(ram_utilizada_mb, ram)
end

#Imprimir la lista con los datos resultantes
println("Tiempos de ejecución (segundos):")
for tiempo in tiempos_ejecucion
    @printf("%.6f\n", tiempo)
end
#println("RAM utilizada (MB):", ram_utilizada_mb)
