from strenum import StrEnum


class ErrorMessageTemplateEnum(StrEnum):
    """Перечисление сообщений об ошибках."""

    NOT_LIST = "{0} не являются списком"
    EMPTY_LIST = "{0} являются пустым списком"
    NOT_INT = "{0} содержат не числовое значение"
    NOT_POS = "{0} содержат нулевое или отрицательное значение"
