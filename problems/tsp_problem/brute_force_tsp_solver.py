from math import inf
from problems.tsp_problem.tsp_abs_solver import (
    AbstractTspSolver,
    TspSolution,
)
from generators.permutation_generator import generate_permutations


class BruteForceTspSolver(AbstractTspSolver):
    def get_tsp_solution(self) -> TspSolution:
        dist_matrix = self._dist_matrix

        if self.order == 1:
            return TspSolution(0, [0])

        inner_cities = list(range(1, self.order))
        permutations = generate_permutations(inner_cities)

        best_distance = inf
        best_path: list[int] = []

        for perm in permutations:
            path = [0] + perm + [0]

            has_none = False
            for i in range(1, len(path)):
                src = path[i - 1]
                trg = path[i]
                if dist_matrix[src][trg] is None:
                    has_none = True
                    break
            if has_none:
                continue

            distance = self.get_distance(dist_matrix, path)

            if distance < best_distance:
                best_distance = distance
                best_path = path

        if not best_path:
            return TspSolution(None, [])

        return TspSolution(best_distance, best_path)


if __name__ == "__main__":
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
    print(f"Минимальное расстояние: {result.distance}, Маршрут: {result.path}")
