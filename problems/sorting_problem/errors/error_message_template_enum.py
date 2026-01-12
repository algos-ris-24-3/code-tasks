from strenum import StrEnum


class ErrorMessageTemplateEnum(StrEnum):
    """Перечисление шаблонов сообщений об ошибках."""

    ERR_INCOMPARABLE_EMBEDDED_TYPES = (
        "Переданы несравнимые экземпляры классов '{}' и '{}'"
    )
