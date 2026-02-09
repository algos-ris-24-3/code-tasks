from network_flow.network_cuts_calculator import NetworkCutsCalculator


if __name__ == "__main__":
    vertex_names = ["s", "a", "b", "c", "d", "t"]
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 1, 5, 0, 0, 0],  # s
        [0, 0, 0, 4, 0, 0],  # a
        [0, 1, 0, 3, 7, 0],  # b
        [0, 0, 0, 0, 8, 3],  # c
        [0, 0, 0, 0, 0, 12],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример расчета пропускной способности всех разрезов сети:")
    cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
    cuts.sort(
        key=lambda cut: (
            len(cut.source_set),
            "".join([str(item) for item in cut.source_set]),
        )
    )

    for cut in cuts:
        print(NetworkCutsCalculator.get_cut_named_str(cut, vertex_names))
