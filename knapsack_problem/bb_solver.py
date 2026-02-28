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
        
        items_amount = self.item_cnt

        best_option = 0

        best_taken = [False] * items_amount

        taken = [False] * items_amount

        first_bound = self._get_bound(-1, taken, items)

        root = BranchNode(-1, taken[:], first_bound)

        heap = [(-first_bound, root)]
        
        while len(heap) > 0:
            minus_bound, node = heapq.heappop(heap)

            bound = -minus_bound
            level = node.level
            path = node.taken

            if bound <= best_option:
                continue

            next_level = level + 1

            if next_level >= items_amount:
                value = self.get_cost(path)

                if value > best_option:
                    best_option = value

                    best_taken = path[:]

                continue

            item = items[next_level]

            is_taken = path[:]

            item_index = item.source_idx

            is_taken[item_index] = True

            if self.get_weight(is_taken) <= self.weight_limit:
                new_value = self.get_cost(is_taken)

                if new_value > best_option:
                    best_option = new_value

                    best_taken = is_taken[:]

                new_bound = self._get_bound(next_level, is_taken, items)

                if new_bound > best_option:
                    new_node = BranchNode(next_level, is_taken, new_bound)

                    heapq.heappush(heap, (-new_bound, new_node))

            not_taken = path[:]

            not_taken_bound = self._get_bound(next_level, path, items)

            if not_taken_bound > best_option:
                not_taken_node = BranchNode(next_level, not_taken, not_taken_bound)

                heapq.heappush(heap, (-not_taken_bound, not_taken_node))

        best_items = [index for index, take in enumerate(best_taken) if take]

        best_items.sort()

        return KnapsackSolution(best_option, best_items)

    def _get_bound(self, level, taken, items):
        weight = self.get_weight(taken)
        value = self.get_cost(taken)

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