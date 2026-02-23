from enum import StrEnum


class ErrorMessageEnum(StrEnum):
    """Перечисление сообщений об ошибках."""

    WRONG_MATRIX = "Таблица затрат не является квадратной матрицей с неотрицательными числовыми значениями"