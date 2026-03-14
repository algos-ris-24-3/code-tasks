from problems.knapsack_problem.genetic_solver import GeneticSolver

if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}\n")

    solver = GeneticSolver(weights, costs, weight_limit)

    for run in range(1, 4):
        print(f"Запуск {run} (поколения {(run-1)*10+1}-{run*10})")
        result = solver.get_knapsack(epoch_cnt=10, verbose=True)
        print(f"\nЛучший результат: стоимость = {result.cost}, предметы={result.items}\n")