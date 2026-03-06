import heapq
from collections import namedtuple

from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

KnapsackItem = namedtuple("KnapsackItem", ["weight", "cost", "price", "source_idx"])
BranchNode = namedtuple("BranchNode", ["level", "taken", "bound"])


class BranchAndBoundSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием метода ветвей и границ."""
        items = [
            KnapsackItem(weight, cost, cost / weight, idx)
            for idx, (weight, cost) in enumerate(zip(self.weights, self.costs))
        ]
        items.sort(key=lambda x: x.price, reverse=True)

        pq = []
        initial_bound = self._get_bound(0, [], items)
        root = BranchNode(level=0, taken=[], bound=initial_bound)

        heapq.heappush(pq, (-root.bound, -root.level, root))

        max_cost = 0
        best_items = []

        while pq:
            neg_bound, _, node = heapq.heappop(pq)
            current_bound = -neg_bound

            if current_bound <= max_cost:
                break

            if node.level >= len(items):
                current_cost = sum(self.costs[idx] for idx in node.taken)
                if current_cost > max_cost:
                    max_cost = current_cost
                    best_items = node.taken
                continue

            next_item = items[node.level]

            taken_with = node.taken + [next_item.source_idx]
            bound_with = self._get_bound(node.level + 1, taken_with, items)
            node_with = BranchNode(
                level=node.level + 1, taken=taken_with, bound=bound_with
            )

            if bound_with > 0:
                node_with = BranchNode(
                    level=node.level + 1, taken=taken_with, bound=bound_with
                )
                heapq.heappush(pq, (-node_with.bound, -node_with.level, node_with))

            bound_without = self._get_bound(node.level + 1, node.taken, items)
            if bound_without > 0:
                node_without = BranchNode(
                    level=node.level + 1, taken=node.taken, bound=bound_without
                )
                heapq.heappush(
                    pq, (-node_without.bound, -node_without.level, node_without)
                )

        return KnapsackSolution(cost=max_cost, items=best_items)

    def _get_bound(self, level, taken, items):
        """
        Расчитывает оценку перспективности текущего предмета.
        """
        current_weight = sum(self.weights[i] for i in taken)
        current_cost = sum(self.costs[i] for i in taken)

        if current_weight > self.weight_limit:
            return 0

        if level >= len(items):
            return current_cost

        next_item = items[level]

        bound = current_cost + (self.weight_limit - current_weight) * next_item.price

        return bound


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BranchAndBoundSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
