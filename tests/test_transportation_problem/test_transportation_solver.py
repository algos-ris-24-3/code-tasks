import unittest

from transportation_problem.transportation_solver import (
    TransportationProblemSolver,
    SUPPLY_ERR_MSG,
    DEMAND_ERR_MSG,
    COST_ERR_MSG,
    BALANCE_ERR_MSG,
)


class TestTransportationProblem(unittest.TestCase):
    """Набор тестов для проверки решения транспортной задачи."""

    def __check_transport_result(self, supply, demand, result):
        """Проверяет корректность полученной матрицы перевозок"""
        transport_matrix = result.transport_matrix

        # Проверяем размеры
        self.assertEqual(len(supply), len(transport_matrix))
        self.assertEqual(len(demand), len(transport_matrix[0]))

        # Проверяем выполнение ограничений по поставкам
        for i in range(len(supply)):
            self.assertEqual(supply[i], sum(transport_matrix[i]))

        # Проверяем выполнение ограничений по спросу
        for j in range(len(demand)):
            self.assertEqual(
                demand[j],
                sum(transport_matrix[i][j] for i in range(len(supply))),
            )

    def __check_cost(self, transport_matrix, cost_matrix, expected_cost):
        """Проверяет корректность вычисленной стоимости"""
        total_cost = 0
        for i in range(len(transport_matrix)):
            for j in range(len(transport_matrix[0])):
                total_cost += transport_matrix[i][j] * cost_matrix[i][j]
        self.assertEqual(expected_cost, total_cost)

    def test_simple_case(self):
        """Проверяет решение простой транспортной задачи"""
        supply = [5, 4, 3]
        demand = [7, 5]
        cost_matrix = [
            [30, 20],
            [25, 15],
            [40, 50],
        ]

        solver = TransportationProblemSolver(supply, demand, cost_matrix)
        result = solver.result

        self.__check_transport_result(supply, demand, result)

        expected_cost = 320
        self.assertEqual(expected_cost, result.min_cost)
        self.__check_cost(result.transport_matrix, cost_matrix, expected_cost)

    def test_single_factory_single_warehouse(self):
        """Проверяет случай 1 завод — 1 склад"""
        supply = [10]
        demand = [10]
        cost_matrix = [[5]]

        solver = TransportationProblemSolver(supply, demand, cost_matrix)
        result = solver.result

        self.assertEqual([[10]], result.transport_matrix)
        self.assertEqual(50, result.min_cost)

    def test_none_supply(self):
        """Проверяет выброс исключения при None в supply"""
        self.assertRaisesRegex(
            ValueError,
            SUPPLY_ERR_MSG,
            TransportationProblemSolver,
            None,
            [1],
            [[1]],
        )

    def test_none_demand(self):
        """Проверяет выброс исключения при None в demand"""
        self.assertRaisesRegex(
            ValueError,
            DEMAND_ERR_MSG,
            TransportationProblemSolver,
            [1],
            None,
            [[1]],
        )

    def test_none_cost_matrix(self):
        """Проверяет выброс исключения при None в cost_matrix"""
        self.assertRaisesRegex(
            ValueError,
            COST_ERR_MSG,
            TransportationProblemSolver,
            [1],
            [1],
            None,
        )

    def test_empty_supply(self):
        """Проверяет выброс исключения при пустом списке supply"""
        self.assertRaisesRegex(
            ValueError,
            SUPPLY_ERR_MSG,
            TransportationProblemSolver,
            [],
            [1],
            [[1]],
        )

    def test_empty_demand(self):
        """Проверяет выброс исключения при пустом списке demand"""
        self.assertRaisesRegex(
            ValueError,
            DEMAND_ERR_MSG,
            TransportationProblemSolver,
            [1],
            [],
            [[1]],
        )

    def test_incorrect_cost_matrix_size(self):
        """Проверяет выброс исключения при неправильной размерности матрицы"""
        supply = [1, 2]
        demand = [1]
        cost_matrix = [[1, 2]]  

        self.assertRaisesRegex(
            ValueError,
            COST_ERR_MSG,
            TransportationProblemSolver,
            supply,
            demand,
            cost_matrix,
        )

    def test_negative_cost(self):
        """Проверяет выброс исключения при отрицательной стоимости"""
        supply = [1]
        demand = [1]
        cost_matrix = [[-5]]

        self.assertRaisesRegex(
            ValueError,
            COST_ERR_MSG,
            TransportationProblemSolver,
            supply,
            demand,
            cost_matrix,
        )

    def test_unbalanced_problem(self):
        """Проверяет выброс исключения при несбалансированной задаче"""
        supply = [5]
        demand = [3]
        cost_matrix = [[1]]

        self.assertRaisesRegex(
            ValueError,
            BALANCE_ERR_MSG,
            TransportationProblemSolver,
            supply,
            demand,
            cost_matrix,
        )

    def test_zero_costs(self):
        """Проверка нулевой стоимости"""
        supply = [5, 5]
        demand = [5, 5]

        cost_matrix = [
            [0, 1],
            [1, 0],
        ]

        solver = TransportationProblemSolver(supply, demand, cost_matrix)
        result = solver.result

        self.__check_transport_result(supply, demand, result)

        self.assertEqual(0, result.min_cost)

    def test_input_not_modified(self):
        """Класс не портит исходные данные в процессе решения задачи"""
        supply = [5, 4]
        demand = [6, 3]
        cost_matrix = [
            [1, 2],
            [3, 4],
        ]

        supply_copy = supply.copy()
        demand_copy = demand.copy()
        cost_copy = [row.copy() for row in cost_matrix]

        solver = TransportationProblemSolver(supply, demand, cost_matrix)
        _ = solver.result

        self.assertEqual(supply_copy, supply)
        self.assertEqual(demand_copy, demand)
        self.assertEqual(cost_copy, cost_matrix)


if __name__ == "__main__":
    unittest.main()