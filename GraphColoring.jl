import Random

mutable struct Grafo
    adjList::Vector{Vector{Int}}
end

function Grafo(edges, n)
    adjList = Vector{Vector{Int}}(undef, n)
    for i in 1:n
        adjList[i] = []
    end

    for (src, dest) in edges
        push!(adjList[src], dest)
        push!(adjList[dest], src)
    end

    return Grafo(adjList)
end

function colorGrafo(grafo::Grafo, n)
    resultado = Dict{Int, Int}()

    for u in 1:n
        asignacion = Set(get(resultado, i, nothing) for i in grafo.adjList[u] if haskey(resultado, i))
        color = 1
        for c in asignacion
            if color != c
                break
            end
            color += 1
        end
        resultado[u] = color
    end

    for v in 1:n
        println("Color asignado al vértice $v es $(resultado[v])")
    end
end

function main()
    Random.seed!(123)

    aristas = Tuple{Int, Int}[]
    num_vertices = 16  # Número total de vertices

    colores = [i for i in 0:num_vertices-1]

    num_bordes = div(num_vertices * (num_vertices - 1), 2)  # Número total de bordes

    for _ in 1:num_bordes
        src = rand(1:num_vertices)
        dest = rand(1:num_vertices)
        push!(aristas, (src, dest))
    end

    n = num_vertices

    grafo = Grafo(aristas, n)
    colorGrafo(grafo, n)
end

main()
