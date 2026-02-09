from problems.shortest_path_problem.floyd_warshall import get_shortest_path


if __name__ == "__main__":
    matrix = [[0, None, None], [1, 0, None], [None, 1, 0]]
    src = 2
    trg = 0

    print("Исходная матрица")
    for row in matrix:
        print(row)

    result = get_shortest_path(matrix, src, trg)
    print(f"\nКратчайшее расстояние между вершинами {src} и {trg} составляет:")
    print(result.distance)
    print("Путь:")
    print(result.path)
