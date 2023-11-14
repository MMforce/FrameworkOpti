using Pkg
Pkg.add("JuMP")
Pkg.add("GLPK")

using JuMP
using GLPK
using Random

# Parámetros
Random.seed!(42)  # Semilla para replicar experimento
num_ciudades = 100  # Cantidad de ciudades (modificable)
num_conjuntos = 20  # Cantidad de subconjuntos (modificable)

N = 1:num_ciudades
M = 1:num_conjuntos

# Costo asociado a cada conjunto (parámetro C)
C = Dict(j => rand(1:10) for j in M)

# Matriz de asignación binaria aleatoria (parámetro a)
a = Dict((i, j) => rand(0:1) for i in N, j in M)

# Crear el modelo de optimización
model = Model(optimizer_with_attributes(GLPK.Optimizer, "msg_lev" => GLPK.GLP_MSG_OFF))

# Variables de decisión binarias
@variable(model, X[j = M], Bin)

# Función objetivo
@objective(model, Min, sum(C[j] * X[j] for j in M))

# Restricciones de cobertura
for i in N
    @constraint(model, sum(a[i, j] * X[j] for j in M) >= 1)
end

# Resolver el problema
optimize!(model)

# Imprimir resultados
println("Estado:", termination_status(model))
println("Costo mínimo:", objective_value(model))
