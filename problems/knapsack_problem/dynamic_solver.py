from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)


class DynamicSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """
        Решает задачу о рюкзаке с использованием метода динамического программирования.

        :return: максимально возможная общая стоимость и список индексов выбранных предметов
        :rtype: KnapsackSolution
        """
        n = self.item_cnt 
        W = self.weight_limit
        
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            weight_i = self.weights[i - 1]
            cost_i = self.costs[i - 1]
            
            for w in range(0, W + 1):
                if weight_i <= w:
                    dp[i][w] = max(dp[i - 1][w], cost_i + dp[i - 1][w - weight_i])
                else:
                    dp[i][w] = dp[i - 1][w]
        
        max_cost = dp[n][W]
        
        selected_items = []
        w = W
        
        for i in range(n, 0, -1):

            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(i - 1)
                w -= self.weights[i - 1]
        
        selected_items.reverse()
        
        return KnapsackSolution(cost=max_cost, items=selected_items)


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = DynamicSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
