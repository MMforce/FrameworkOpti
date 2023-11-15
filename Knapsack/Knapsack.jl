using Pkg

# Asegúrate de tener las librerías necesarias instaladas
#Pkg.add("JuMP")
#Pkg.add("GLPK")

using JuMP
using GLPK
using Printf

# Esta función resuelve el problema Knapsack y devuelve el tiempo de ejecución
function resolver_knapsack(num_elementos)
    PESOMAX = 100
    VALOR = Dict(i => rand(1:20) for i in 1:num_elementos)
    PESO = Dict(i => rand(1:10) for i in 1:num_elementos)
    ELEMENTOS = 1:num_elementos

    model = Model(optimizer_with_attributes(GLPK.Optimizer))
    @variable(model, take[ELEMENTOS], binary=true)
    @objective(model, Max, sum(VALOR[i] * take[i] for i in ELEMENTOS))
    @constraint(model, sum(PESO[i] * take[i] for i in ELEMENTOS) <= PESOMAX)

    time = @elapsed optimize!(model)
    return time
end

# Almacena los tiempos para diferentes números de elementos
tiempos = Dict()

for num_elementos in 10:10:100
    tiempo_ejecucion = resolver_knapsack(num_elementos)
    tiempos[num_elementos] = tiempo_ejecucion
end

# Imprime los tiempos almacenados
for (num_elementos, tiempo) in tiempos
    
    println("Elementos: $num_elementos - Tiempo: $tiempo segundos")
end
