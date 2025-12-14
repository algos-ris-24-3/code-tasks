from strenum import StrEnum


class ErrorMessageEnum(StrEnum):
    """Перечисление сообщений об ошибках."""

    LENGTHS_NOT_EQUAL = "Списки весов и стоимости разной длины"
    NOT_INT_WEIGHT_LIMIT = "Ограничение вместимости рюкзака не является целым " "числом"
    NOT_POS_WEIGHT_LIMIT = "Ограничение вместимости рюкзака меньше единицы"
    LESS_WEIGHT_LIMIT = (
        "Ограничение вместимости рюкзака меньше чем " "минимальный вес предмета"
    )
