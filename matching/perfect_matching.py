from matching.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from collections import deque

from matching.errors.perfect_matching_error import PerfectMatchingError


def get_perfect_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит совершенное паросочетание в двудольном графе с долями равной мощности
    с помощью чередующегося дерева и метода «волны» (BFS по фронтам).
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)

    matching = BipartiteGraphMatching(bipartite_graph.order)

    if bipartite_graph.order == 0:
        return matching

    def augment(root_left: int) -> bool:
        visited_left = [False] * bipartite_graph.order
        visited_right = [False] * bipartite_graph.order
        pred_right = [-1] * bipartite_graph.order
        pred_left = [-1] * bipartite_graph.order

        q = deque([root_left])
        visited_left[root_left] = True
        free_right = -1

        while q and free_right == -1:
            l = q.popleft()
            matched_r = matching.get_right_match(l)

            for r in bipartite_graph.right_neighbors(l):
                if r == matched_r:
                    continue
                if visited_right[r]:
                    continue

                visited_right[r] = True
                pred_right[r] = l

                if not matching.is_right_covered(r):
                    free_right = r
                    break

                l2 = matching.get_left_match(r)
                if l2 != -1 and not visited_left[l2]:
                    visited_left[l2] = True
                    pred_left[l2] = r
                    q.append(l2)

        if free_right == -1:
            return False

        path_edges = []
        r = free_right
        while True:
            l = pred_right[r]
            path_edges.append((l, r))
            if l == root_left:
                break
            r_prev = pred_left[l]
            path_edges.append((l, r_prev))
            r = r_prev

        path_edges.reverse()
        to_add = path_edges[0::2]
        to_remove = path_edges[1::2]

        for l, r in to_remove:
            matching.remove_edge(l, r)
        for l, r in to_add:
            matching.add_edge(l, r)

        return True

    while not matching.is_perfect:
        root = -1
        for i in range(bipartite_graph.order):
            if not matching.is_left_covered(i):
                root = i
                break

        if root == -1:
            break

        if not augment(root):
            raise PerfectMatchingError("Совершенное паросочетание не найдено")

    return matching
