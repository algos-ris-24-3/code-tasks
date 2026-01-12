from schedules.constants import (
    SCHEDULE_ITEM_DOWNTIME_STR_TEMPL,
    SCHEDULE_ITEM_STR_TEMPL,
)
from schedules.errors import ErrorMessages, ScheduleItemError
from schedules.task import Task


class ScheduleItem:
    """Класс представляет собой элемент расписания, включает в себя задачу,
    выполняющуюся в течение некоторого времени.

    Properties
    ----------
    task_name(self) -> str:
        Возвращает название выполняемой задачи или downtime если указан
        признак простоя.

    is_downtime(self) -> bool:
        Возвращает значение признака простоя.

    start(self) -> float:
        Возвращает момент начала выполнения задачи.

    duration(self) -> float:
        Возвращает продолжительность выполнения задачи.

    end(self) -> float:
        Возвращает момент окончания выполнения задачи.
    """

    def __init__(
        self,
        task: Task | None,
        start: float,
        duration: float,
    ):
        """Метод инициализации объекта класса.

        :param task: Выполняемая задача или None если элемент представляет простой в расписании.
        :param start: Начало выполнения задачи.
        :param duration: Продолжительность выполнения задачи.
        :raise ScheduleArgumentException: Если не указана задача и признак
            простоя, если указаны некорректные значения начала и
            продолжительности выполнения задачи.
        """
        ScheduleItem.__validate_params(task, start, duration)
        self.__task = task
        self.__start = start
        self.__duration = duration

    @property
    def task_name(self) -> str:
        """Возвращает название выполняемой задачи или downtime если указан
        признак простоя."""
        return "downtime" if self.is_downtime else self.__task.name

    @property
    def is_downtime(self) -> bool:
        """Возвращает значение признака простоя."""
        return self.__task is None

    @property
    def start(self) -> float:
        """Возвращает момент начала выполнения задачи."""
        return self.__start

    @property
    def duration(self) -> float:
        """Возвращает продолжительность выполнения задачи."""
        return self.__duration

    @property
    def end(self) -> float:
        """Возвращает момент окончания выполнения задачи."""
        return self.__start + self.__duration

    def __str__(self):
        if self.is_downtime:
            return SCHEDULE_ITEM_DOWNTIME_STR_TEMPL.format(self.start, self.end)
        return SCHEDULE_ITEM_STR_TEMPL.format(self.task_name, self.start, self.end)

    def __eq__(self, other):
        return (
            self.__task == other.__task
            and self.start == other.start
            and self.duration == other.duration
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.__task, self.start, self.duration))

    @staticmethod
    def __validate_params(task: Task | None, start: float, duration: float) -> None:
        """Проверяет корректность входных данных для создания экземпляра
        класса."""
        if not isinstance(start, int) and not isinstance(start, float):
            raise ScheduleItemError(ErrorMessages.START_NOT_NUMBER)
        if start < 0:
            raise ScheduleItemError(ErrorMessages.START_NEG_NUMBER)
        if not isinstance(duration, int) and not isinstance(duration, float):
            raise ScheduleItemError(ErrorMessages.DUR_NOT_NUMBER)
        if duration <= 0:
            raise ScheduleItemError(ErrorMessages.DUR_NOT_POS_NUMBER)


if __name__ == "__main__":
    print("Пример использования класса ScheduleItem\n")

    # Инициализируем экземпляр класса ScheduleItem
    task = Task("task 1", 1.1)
    schedule_item = ScheduleItem(task, 0, 1)

    # Контроль корректности входных данных
    try:
        ScheduleItem(task, -1, 1)
    except ScheduleItemError as error:
        print(f"Ошибка инициализации: {error}")

    # Приведение экземпляра класса ScheduleItem к строковому типу
    print(schedule_item)
