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
        
        items_amount = len(items)

        best_option = 0

        best_items = []

        first_bound = self._get_bound(-1, [], items)

        heap = [(-first_bound, -1, 0, 0, [])]
        
        while len(heap) > 0:
            minus_bound, level, weight, value, path = heapq.heappop(heap)

            bound = -minus_bound

            if bound <= best_option:
                continue

            next_level = level + 1

            if next_level >= items_amount:
                if value > best_option:
                    best_option = value

                    best_items = path
                continue

            item = items[next_level]

            if weight + item.weight <= self.weight_limit:
                new_weight = weight + item.weight

                new_value = value + item.cost

                new_item_index = [item.source_idx]
                
                new_path = path + new_item_index

                if new_value > best_option:
                    best_option = new_value

                    best_items = new_path

                new_bound = self._get_bound(next_level, new_path, items)

                if new_bound > best_option:
                    heapq.heappush(heap, (-new_bound, next_level, new_weight, new_value, new_path))

            not_taken_bound = self._get_bound(next_level, path, items)

            if not_taken_bound > best_option:
                heapq.heappush(heap, (-not_taken_bound, next_level, weight, value, path))

        best_items.sort()

        return KnapsackSolution(cost = best_option, items = best_items)

    def _get_bound(self, level, taken, items):
        weight = 0
        value = 0

        for item in items:
            item_index = item.source_idx

            if item_index in taken:
                weight += item.weight

                value += item.cost

        if weight > self.weight_limit:
            return 0
        
        bound = value

        available_space = self.weight_limit - weight

        for item_index in range(level + 1, len(items)):
            item = items[item_index]

            if item.weight <= available_space:
                bound += item.cost

                available_space -= item.weight
            else:
                bound += item.price * available_space

                break
        
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