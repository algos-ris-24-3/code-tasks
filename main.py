from assignment_problem.network_flow_solver import get_assignments, get_min_cost_perfect_matching


if __name__ == "__main__":
    matrix = [
        [6, 7, 8, 14, 7],
        [8, 14, 6, 9, 7],
        [14, 14, 13, 9, 11],
        [5, 12, 10, 9, 14],
        [6, 10, 8, 10, 15],
    ]
    print("Исходная матрица")
    for row in matrix:
        print(row)

    matching = get_min_cost_perfect_matching(matrix)
    
    result = get_assignments(matrix)
    print("\nРешение задачи о назначениях")
    print(f"Стоимость назначения: {result.cost}")
    print("Назначения: ")
    for assignment in result.assignments:
        print(assignment)
