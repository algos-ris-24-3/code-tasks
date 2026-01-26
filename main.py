from matching.bipartite_graph import BipartiteGraph
from matching.max_matching import get_max_matching


if __name__ == "__main__":
    print("Исходный двудольный граф")
    bipartite_graph = BipartiteGraph({
        0: [0, 1],
        1: [0, 4],
        2: [1, 2, 3],
        3: [1, 2, 4],
        4: [0, 4],
    })
    print(bipartite_graph)

    print("Полученное паросочетание")
    print(get_max_matching(bipartite_graph))
