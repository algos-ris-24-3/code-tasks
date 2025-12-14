from problems.knapsack_problem.brute_force_solver import BruteForceSolver

"""В файле расположен пример использования класса BruteForceSolver.
Сам класс BruteForceSolver, который необходимо реализовать, расположен 
в problems/knapsack_problem/brute_force_solver.py
"""


def main():
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке полным перебором\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BruteForceSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )


if __name__ == "__main__":
    main()
