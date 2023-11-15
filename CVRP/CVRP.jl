using Pkg
#Pkg.add("JuMP")
#Pkg.add("GLPK")
#Pkg.add("Cbc")
using JuMP
using GLPK
using Cbc
using Random

# Función para ejecutar el modelo y almacenar datos
function ejecutar_modelo(num_nodos, resultados)
    # Definición de los datos del problema de manera aleatoria
    Random.seed!(0)  # Para repetir el experimento
    nodos = 1:num_nodos
    capacidad = 20
    demanda = Dict(i => rand(1:5) for i in nodos)
    distancia = Dict(i => Dict(j => rand(1:10) for j in nodos) for i in nodos)

    # Creación del modelo de optimización
    model = Model(optimizer_with_attributes(GLPK.Optimizer))

    # Variables de decisión
    @variable(model, x[i in nodos, j in nodos], Bin)
    @variable(model, u[i in nodos] >= 0)

    # Función objetivo: Minimizar la distancia total
    @objective(model, Min, sum(distancia[i][j] * x[i, j] for i in nodos, j in nodos))

    # Restricciones
    for i in nodos
        @constraint(model, sum(x[i, j] for j in nodos if j != i) == 1)  # Cada nodo se visita exactamente una vez
        @constraint(model, sum(demanda[j] * x[j, i] for j in nodos if j != i) <= u[i])  # Capacidad de los vehículos
        @constraint(model, u[i] <= capacidad)  # Capacidad máxima de los vehículos
    end

    # Evitar subrutas
    for i in nodos
        for j in nodos
            if i != j && i != 1 && j != 1
                @constraint(model, u[i] - u[j] + capacidad * x[i, j] <= capacidad - demanda[j])
            end
        end
    end

    # Medir el tiempo y la RAM
    tiempo_inicio = time()
    ram_inicio = Sys.total_memory()

    # Resolver el problema
    optimize!(model)

    # Medir el tiempo y la RAM al final
    tiempo_fin = time() - tiempo_inicio
    ram_fin = Sys.total_memory() - ram_inicio

    # Almacenar resultados
    push!(resultados, (num_nodos = num_nodos, tiempo = tiempo_fin, ram = ram_fin))

    # Mostrar la solución
    if termination_status(model) == MOI.OPTIMAL
        #println("Distancia total mínima:", objective_value(model))
        for i in nodos
            for j in nodos
                if value(x[i, j]) > 0.5
                    #println("Vehículo ", i, " va al nodo ", j)
                end
            end
        end
        #println("Tiempo de ejecución: ", tiempo_fin, " segundos")
        #println("RAM utilizada: ", ram_fin / 2^20, " MB")  # Convertir a megabytes
    else
        println("El problema no tiene solución óptima.")
    end
end

# Almacenar resultados en una lista
resultados = []

# Ejecutar el modelo para diferentes valores de num_nodos
for num_nodos in 3:30
    #println("\nEjecutando modelo con ", num_nodos, " nodos.")
    ejecutar_modelo(num_nodos, resultados)
end

# Imprimir resultados ordenados
println("\nResultados:")
for resultado in resultados
    println("Nodos: ", resultado.num_nodos, ", Tiempo: ", resultado.tiempo, " segundos, RAM: ", resultado.ram / 2^20, " MB")
end
