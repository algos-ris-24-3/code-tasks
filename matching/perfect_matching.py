from matching.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from collections import deque

from matching.errors.perfect_matching_error import PerfectMatchingError


def get_perfect_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит совершенное паросочетание в двудольном графе с долями равной мощности.

    Алгоритм последовательно ищет увеличивающие (чередующиеся) пути относительно текущего
    паросочетания, начиная с пустого. Каждый найденный путь используется для увеличения
    мощности паросочетания на единицу. Процесс продолжается, пока существуют непокрытые
    вершины в левой доле и найдены увеличивающие пути.

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий совершенное паросочетание.
    :raises PerfectMatchingError: Если совершенное паросочетание не существует в данном графе.
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
    print(get_perfect_matching(bipartite_graph))
