using Pkg
Pkg.add("JuMP")
Pkg.add("GLPK")
Pkg.add("Cbc")

using JuMP
using GLPK
using Cbc
using Random

# Definición de los datos del problema de manera aleatoria
Random.seed!(0)  # Para repetir el experimento
num_nodos = 30  # Número de nodos, puedes cambiarlo
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

# Resolver el problema
optimize!(model)

# Mostrar la solución
if termination_status(model) == MOI.OPTIMAL
    println("Distancia total mínima:", objective_value(model))
    for i in nodos
        for j in nodos
            if value(x[i, j]) > 0.5
                println("Vehículo ", i, " va al nodo ", j)
            end
        end
    end
else
    println("El problema no tiene solución óptima.")
end
