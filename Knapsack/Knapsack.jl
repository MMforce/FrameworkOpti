using Pkg
Pkg.add("JuMP")
Pkg.add("GLPK")

using JuMP
using GLPK

# Número de elementos (objetos)
num_elementos = 100

# Peso máximo permitido
PESOMAX = 100

# Generar valores y pesos aleatorios para cada elemento
VALOR = Dict(i => rand(1:20) for i in 1:num_elementos)
PESO = Dict(i => rand(1:10) for i in 1:num_elementos)

# Conjunto que indica el rango para cada elemento
ELEMENTOS = 1:num_elementos

# Crear un modelo de optimización
model = Model(optimizer_with_attributes(GLPK.Optimizer))

# Variable binaria que indica si el objeto es tomado o no
@variable(model, take[ELEMENTOS], binary=true)

# Función objetivo que maximiza el valor total de objetos
@objective(model, Max, sum(VALOR[i] * take[i] for i in ELEMENTOS))

# Restricción de peso
@constraint(model, sum(PESO[i] * take[i] for i in ELEMENTOS) <= PESOMAX)

# Resolver el problema
optimize!(model)

# Imprimir el resultado
if termination_status(model) == MOI.OPTIMAL
    println("Solución óptima encontrada:")
    for i in ELEMENTOS
        if value(take[i]) == 1
            println("Elemento $i - Valor: $(VALOR[i]), Peso: $(PESO[i])")
        end
    end
else
    println("No se encontró una solución óptima.")
end
