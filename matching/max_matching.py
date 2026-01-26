from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum
from collections import deque


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

    ...
    
    return matching


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
