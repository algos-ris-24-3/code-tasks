from network_flow.data_types import NetworkCutData, NetworkVerticesData
from network_flow.network_validator import NetworkValidator

CAPACITY_MATRIX_NAME = "Таблица пропускных способностей"

class NetworkCutsCalculator:
    @staticmethod
    def get_network_cuts(capacity_matrix) -> list[NetworkCutData]:
        """
        Находит все возможные разрезы сети и вычисляет их пропускную способность.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        :return: Список разрезов сети с их пропускной способностью.
        :rtype: list[NetworkCutData]
        """
        NetworkValidator.validate_matrix(capacity_matrix, CAPACITY_MATRIX_NAME)
        vertices = NetworkCutsCalculator.split_vertices_by_types(capacity_matrix)
        NetworkValidator.validate_vertices(vertices, CAPACITY_MATRIX_NAME)

        source_idx = vertices.sources[0]
        sink_idx = vertices.sinks[0]
        transit_idxs = vertices.transits

        transit_cnt = len(transit_idxs)
        format_mask = "{0:0" + str(transit_cnt) + "b}"

        cuts = []
        ...

        return cuts

    @staticmethod
    def get_cut_named_str(cut: NetworkCutData, names: list[str]) -> str:
        """
        Форматирует разрез сети в виде строки с именами вершин.

        :param cut: Данные о разрезе сети.
        :type cut: NetworkCutData
        :param names: Список имен вершин графа.
        :type names: list[str]
        :return: Форматированное строковое представление разреза сети.
        :rtype: str
        """
        named_source_vertices = [names[idx] for idx in cut.source_set]
        named_sink_vertices = [names[idx] for idx in cut.sink_set]
        return (
            f"capacity: {cut.capacity} {named_source_vertices} -> {named_sink_vertices}"
        )

    @staticmethod
    def _get_cut_capacity(source_vertices, sink_vertices, matrix):
        ...
    
    @staticmethod
    def split_vertices_by_types(matrix) -> NetworkVerticesData:
        """
        Разделяет вершины сети на три категории: источники, стоки и транзитные вершины.

        :param matrix: Квадратная матрица пропускных способностей графа.
        :type matrix: list[list[int]]
        :return: Данные о вершинах сети, содержащие источники, стоки и транзиты.
        :rtype: NetworkVerticesData
        """
        sources = []
        ...
        sinks = []
        ...
        transits = []
        ...

        return NetworkVerticesData(sources, sinks, transits)


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
