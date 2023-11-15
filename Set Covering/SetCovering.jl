using Pkg
#Pkg.add("JuMP")
#Pkg.add("GLPK")
using JuMP
using GLPK
using Random

#Función para resolver el problema y medir el tiempo de ejecución
function resolver_tiempo(num_ciudades)
    num_conjuntos = 20  #Cantidad de subconjuntos (modificable)
    
    N = 1:num_ciudades
    M = 1:num_conjuntos
    
    #Costo asociado a cada conjunto (parámetro C)
    C = Dict(j => rand(1:10) for j in M)
    
    #Matriz de asignación binaria aleatoria (parámetro a)
    a = Dict((i, j) => rand(0:1) for i in N, j in M)
    
    #Crear el modelo de optimización
    model = Model(optimizer_with_attributes(GLPK.Optimizer, "msg_lev" => GLPK.GLP_MSG_OFF))
    
    #Variables de decisión binarias
    @variable(model, X[j = M], Bin)
    
    #Función objetivo
    @objective(model, Min, sum(C[j] * X[j] for j in M))
    
    #Restricciones de cobertura
    for i in N
        @constraint(model, sum(a[i, j] * X[j] for j in M) >= 1)
    end
    
    #Resolver el problema y medir el tiempo
    tiempo = @elapsed optimize!(model)
    
    return tiempo, objective_value(model)
end

#Vectores para almacenar los tiempos y costos mínimos
tiempos = Float64[]
costos_minimos = Float64[]

#Ejecutar para diferentes valores de num_ciudades
for num_ciudades in 10:10:100
    tiempo, costo_minimo = resolver_tiempo(num_ciudades)
    push!(tiempos, tiempo)
    push!(costos_minimos, costo_minimo)
    println("Para $num_ciudades ciudades - Tiempo: $tiempo segundos - Costo mínimo: $costo_minimo")
end

#Imprime resultados finales
println("Tiempos: ", tiempos)
println("Costos mínimos: ", costos_minimos)
