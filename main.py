from generators.permutation_generator import generate_permutations
from problems.tsp_problem.brute_force_tsp_solver import BruteForceTspSolver


def main():
    print('Пример генерации перестановок')
    items = [1, 2, 3]
    print(generate_permutations(items))

    print("Пример решения задачи коммивояжёра\n\nМатрица расстояний:")
    matrix = [
        [None, 12.0, 9.0, 9.0, 12.0],
        [9.0, None, 8.0, 19.0, 15.0],
        [7.0, 1.0, None, 17.0, 11.0],
        [5.0, 9.0, 12.0, None, 16.0],
        [14.0, 6.0, 12.0, 22.0, None],
    ]
    for row in matrix:
        print(row)

    solver = BruteForceTspSolver(matrix)
    result = solver.get_tsp_solution()
    print(f"Минимальное расстояние: {result.distance}, " f"Маршрут: {result.path}")