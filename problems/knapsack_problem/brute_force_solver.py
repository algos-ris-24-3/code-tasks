from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)


class BruteForceSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием полного перебора.

        Генерируются все возможные варианты включения предметов в рюкзак
        с помощью чисел от 1 до 2^n - 1, представленных в бинарном виде.
        Бинарная строка длины n превращается в список bool, который
        передаётся в методы get_weight и get_cost родительского класса.
        """
        n = self.item_cnt

        best_cost = 0
        best_items: list[int] = []

        for mask in range(1, 1 << n):
            bits = format(mask, f"0{n}b")

            selected = [bit == "1" for bit in bits]

            total_weight = self.get_weight(selected)
            if total_weight > self.weight_limit:
                continue

            total_cost = self.get_cost(selected)

            if total_cost > best_cost:
                best_cost = total_cost
                best_items = [i for i, flag in enumerate(selected) if flag]

        return KnapsackSolution(cost=best_cost, items=best_items)


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
        f"Максимальная стоимость: {result.cost}, "
        f"индексы предметов: {result.items}"
    )
