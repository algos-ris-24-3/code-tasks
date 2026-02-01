from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum


def get_max_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит максимальное по мощности паросочетание в двудольном графе с долями равной мощности.

    Алгоритм начинает с пустого паросочетания и последовательно ищет увеличивающие 
    (чередующиеся) пути относительно текущего паросочетания. Каждый найденный путь 
    используется для увеличения мощности паросочетания на единицу. Процесс завершается, 
    когда увеличивающих путей больше не существует — в этот момент паросочетание 
    становится максимальным (по теореме Бержа).

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий максимальное паросочетание.
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)
    
    matching = BipartiteGraphMatching(bipartite_graph.order)

    while True:
        chain = alternating_chain_search(bipartite_graph, matching, bipartite_graph.order)

        if chain == None:
            break

        increase_matching(matching, chain)
    
    return matching

def alternating_chain_search(graph, match, size):
    left_side = [-1] * size

    right_side = [-1] * size

    vertices = deque()

    for left in range(size):
        if not match.is_left_covered(left):
            left_side[left] = -2
            vertices.append(left)

    while len(vertices) > 0:
        current_left = vertices.popleft()

        for right in graph.right_neighbors(current_left):
            if right_side[right] == -1:
                right_side[right] = current_left

                if not match.is_right_covered(right):
                    return left_side, right_side, right
                
                left_vertex = match.get_left_match(right)

                if left_side[left_vertex] == -1:
                    left_side[left_vertex] = right
                    vertices.append(left_vertex)

    return None

def increase_matching(match, alternating_chain):
    left_side, right_side, last_right = alternating_chain

    right_vertex = last_right

    while True:
        left_vertex = right_side[right_vertex]

        if match.is_left_covered(left_vertex):
            old_right = match.get_right_match(left_vertex)

            match.remove_edge(left_vertex, old_right)

        match.add_edge(left_vertex, right_vertex)

        if left_side[left_vertex] == -2:
            break

        right_vertex = left_side[left_vertex]

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
