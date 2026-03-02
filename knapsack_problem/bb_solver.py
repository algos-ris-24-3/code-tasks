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
        best_items = []
        heap = []
        counter = 0
        init_bound = self._get_bound(0, 0, 0, items)
        init_node = (0, 0, 0, [])
        heapq.heappush(heap, (-init_bound, counter, init_node))
        counter += 1
        while heap:
            neg_bound, _, node = heapq.heappop(heap)
            level, cost, weight, selected = node
            if -neg_bound <= best_cost:
                continue
            if level == n:
                if cost > best_cost:
                    best_cost = cost
                    best_items = selected[:]
                continue
            notake_bound = self._get_bound(level + 1, cost, weight, items)
            if notake_bound > best_cost:
                notake_node = (level + 1, cost, weight, selected[:])
                heapq.heappush(heap, (-notake_bound, counter, notake_node))
                counter += 1
            item = items[level]
            if weight + item.weight <= self.weight_limit:
                new_cost = cost + item.cost
                new_weight = weight + item.weight
                new_selected = selected[:] + [item.source_idx]
                take_bound = self._get_bound(level + 1, new_cost, new_weight, items)
                if take_bound > best_cost:
                    take_node = (level + 1, new_cost, new_weight, new_selected)
                    heapq.heappush(heap, (-take_bound, counter, take_node))
                    counter += 1
        best_items.sort()
        return KnapsackSolution(cost=best_cost, items=best_items)

    def _get_bound(self, level, cur_cost, cur_weight, items) -> float:
        bound = cur_cost
        remaining_capacity = self.weight_limit - cur_weight
        i = level
        while i < len(items) and remaining_capacity > 0:
            if items[i].weight <= remaining_capacity:
                bound += items[i].cost
                remaining_capacity -= items[i].weight
            else:
                bound += items[i].price * remaining_capacity
                remaining_capacity = 0
            i += 1
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
