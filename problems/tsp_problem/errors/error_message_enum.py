from strenum import StrEnum


class ErrorMessageEnum(StrEnum):
    """Перечисление сообщений об ошибках."""

    WRONG_MATRIX = (
        "Таблица расстояний не является прямоугольной матрицей с "
        "числовыми значениями"
    )
    NEG_VALUE = "Расстояние не может быть отрицательным"
