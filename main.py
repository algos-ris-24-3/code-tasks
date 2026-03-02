
from network_flow.min_cost_flow_calculator import MinCostFlowCalculator
from transportation_problem.transportation_solver import TransportationProblemSolver

if __name__ == "__main__":
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    cost_matrix = [
        # s a  b  c  d  t
        [0, 3, 2, 4, 0, 0],  # s
        [0, 0, 0, 4, 5, 0],  # a
        [0, 2, 0, 2, 0, 0],  # b
        [0, 0, 0, 0, 2, 0],  # c
        [0, 0, 0, 0, 0, 1],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока минимальной стоимости:")
    calculator = MinCostFlowCalculator(capacity_matrix, cost_matrix)
    print("Величина максимального потока:", calculator._max_flow)
    print("Стоимость потока:", calculator._min_cost)
    print("Матрица локальных потоков")
    for row in calculator._flow_matrix:
        print(row)
        
    print("Пример решения транспортной задачи:")
    print("="*50)

    supply = [5, 4, 3] 
    demand = [7, 5] 
    cost_matrix = [
        [30, 20],  
        [25, 15],  
        [40, 50],  
    ]

    print("Мощности заводов:", supply)
    print("Ёмкости складов:", demand)
    print("Матрица стоимостей:")
    for row in cost_matrix:
        print(" ", row)

    solver = TransportationProblemSolver(supply, demand, cost_matrix)
    result = solver.result

    print("\nМатрица перевозок:")
    for i, row in enumerate(result.transport_matrix):
        print(f"  Завод {i+1}: {row}")
    print("Минимальная стоимость:", result.min_cost)