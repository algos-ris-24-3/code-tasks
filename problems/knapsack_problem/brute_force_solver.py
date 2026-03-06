from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)
from itertools import combinations


class BruteForceSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """
        Решает задачу о рюкзаке с использованием полного перебора.

        :return: максимально возможная общая стоимость и список индексов выбранных предметов
        :rtype: KnapsackSolution
        """
        best_cost: int = 0
        best_selected = [False] * self.item_cnt

        for number in range(1, 2**self.item_cnt):
            selected = [bool(int(char)) for char in format(number, self._mask)]
            current_cost = self.get_cost(selected)
            if current_cost > best_cost:
                best_cost = current_cost
                best_selected = selected

        return KnapsackSolution(
            cost=best_cost,
            items=[idx for idx, is_selected in enumerate(best_selected) if is_selected],
        )


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BruteForceSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
