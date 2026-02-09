from network_flow.data_types import NetworkVerticesData
from network_flow.error_message_enum import ErrorMessageEnum


class NetworkValidator:
    @staticmethod
    def validate_matrix(matrix: list[list[int]], matrix_name: str) -> None:
        """
        Проверяет, что входная матрица корректна:
        - Матрица должна быть квадратной.
        - Все значения должны быть неотрицательными числами.
        - Должен быть ровно один источник и один сток.

        :param matrix: Квадратная матрица.
        :type matrix: list[list[int]]
        :raises ValueError: Если матрица не соответствует требованиям.
        """

        if (
            not matrix
            or not isinstance(matrix, list)
            or not matrix[0]
            or not isinstance(matrix[0], list)
        ):
            raise ValueError(f"{matrix_name}: {ErrorMessageEnum.MATRIX_ERR_MSG}")
        row_cnt = len(matrix[0])
        if row_cnt < 2:
            raise ValueError(f"{matrix_name}: {ErrorMessageEnum.LESS_THAN_2_ERR_MSG}")
        for row in matrix:
            if len(row) != row_cnt:
                raise ValueError(f"{matrix_name}: {ErrorMessageEnum.MATRIX_ERR_MSG}")
            for value in row:
                if not isinstance(value, int) or value < 0:
                    raise ValueError(
                        f"{matrix_name}: {ErrorMessageEnum.MATRIX_ERR_MSG}"
                    )

    @staticmethod
    def validate_vertices(vertices: NetworkVerticesData, matrix_name: str) -> None:
        """
        Проверяет, что структура сети корректна:
        - Должен быть ровно один источник и один сток.

        :param vertices: Данные о вершинах сети.
        :type matrix: NetworkVerticesData
        :raises ValueError: Если структура сети не соответствует требованиям.
        """

        if len(vertices.sources) != 1:
            raise ValueError(f"{matrix_name}: {ErrorMessageEnum.SOURCE_ERR_MSG}")
        if len(vertices.sinks) != 1:
            raise ValueError(f"{matrix_name}: {ErrorMessageEnum.SINK_ERR_MSG}")
