import heapq
from collections import namedtuple

from knapsack_problem.knapsack_abs_solver import (
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
        
        n = len(items)

        best_cost = 0
        best_taken = [False] * n

        pq = []

        start_taken = [False] * n
        start_bound = self._get_bound(0, start_taken, items)

        start_node = BranchNode(0, start_taken, start_bound)

        heapq.heappush(pq, (-start_node.bound, start_node))

        while pq:

            _, node = heapq.heappop(pq)

            if node.bound <= best_cost:
                continue

            level = node.level

            if level >= n:
                continue

            taken_with = node.taken.copy()
            taken_with[level] = True

            weight = 0
            cost = 0

            for i in range(level + 1):
                if taken_with[i]:
                    weight += items[i].weight
                    cost += items[i].cost

            if weight <= self.weight_limit:
                if cost > best_cost:
                    best_cost = cost
                    best_taken = taken_with.copy()

                bound = self._get_bound(level + 1, taken_with, items)

                if bound > best_cost:
                    heapq.heappush(pq,(-bound, BranchNode(level + 1, taken_with, bound)))

            taken_without = node.taken.copy()
            taken_without[level] = False

            bound = self._get_bound(level + 1, taken_without, items)

            if bound > best_cost:
                heapq.heappush(pq,(-bound, BranchNode(level + 1, taken_without, bound)))

        result_items = []

        for i, take in enumerate(best_taken):
            if take:
                result_items.append(items[i].source_idx)

        result_items.sort()

        return KnapsackSolution(best_cost, result_items)

    def _get_bound(self, level, taken, items):
        """Вычисляет верхнюю границу стоимости (fractional knapsack)."""

        total_weight = 0
        total_cost = 0

        for i in range(level):
            if taken[i]:
                total_weight += items[i].weight
                total_cost += items[i].cost

        if total_weight > self.weight_limit:
            return 0

        if level < len(items):
            total_cost += items[level].price * (self.weight_limit - total_weight)

        return total_cost


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