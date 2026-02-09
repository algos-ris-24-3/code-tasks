from strenum import StrEnum


class ErrorMessageEnum(StrEnum):
    """Перечисление сообщений об ошибках приложения."""

    MATRIX_ERR_MSG = "Таблица не является квадратной матрицей с неотрицательными числовыми значениями"
    LESS_THAN_2_ERR_MSG = "В сети должно быть не менее 2 вершин"
    SOURCE_ERR_MSG = "В сети должен быть один исток"
    SINK_ERR_MSG = "В сети должен быть один сток"
