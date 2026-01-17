from schedules.abstract_schedule import AbstractSchedule
from schedules.errors import (
    ScheduleArgumentError,
    ErrorMessages,
    ErrorTemplates,
)
from schedules.staged_task import StagedTask
from schedules.schedule_item import ScheduleItem


class ConveyorSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач, состоящих
     из двух этапов и двух исполнителей. Для построения расписания используется
     алгоритм Джонсона.

    Properties
    ----------
    tasks(self) -> tuple[Task]:
        Возвращает исходный список задач для составления расписания.

    task_count(self) -> int:
        Возвращает количество задач для составления расписания.

    executor_count(self) -> int:
        Возвращает количество исполнителей.

    duration(self) -> float:
        Возвращает общую продолжительность расписания.

    Methods
    -------
    get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleRow]:
        Возвращает расписание для указанного исполнителя.
    """

    def __init__(self, tasks: list[StagedTask]):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество этапов для какой-либо задачи не
        равно двум.
        """
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""

        # Время окончания работы каждого исполнителя
        time_executor_0 = 0.0
        time_executor_1 = 0.0

        for task in tasks:
            stage1_duration = task.stage_duration(0)
            stage2_duration = task.stage_duration(1)

            # Первый исполнитель всегда работает последовательно без простоев
            start_stage1 = time_executor_0
            self._executor_schedule[0].append(
                ScheduleItem(task, start_stage1, stage1_duration)
            )
            time_executor_0 = start_stage1 + stage1_duration

            # Второй исполнитель не может начать раньше, чем:
            # 1) освободится сам
            # 2) завершится первый этап соответствующей задачи
            start_stage2 = max(time_executor_1, time_executor_0)

            # Если второй исполнитель простаивает до начала работы над задачей
            if start_stage2 > time_executor_1:
                self._executor_schedule[1].append(
                    ScheduleItem(
                        None,
                        time_executor_1,
                        start_stage2 - time_executor_1,
                    )
                )

            self._executor_schedule[1].append(
                ScheduleItem(task, start_stage2, stage2_duration)
            )
            time_executor_1 = start_stage2 + stage2_duration

        # После завершения всех задач первый исполнитель может простаивать,
        # пока второй исполнитель завершает свою работу
        if time_executor_1 > time_executor_0:
            self._executor_schedule[0].append(
                ScheduleItem(
                    None,
                    time_executor_0,
                    time_executor_1 - time_executor_0,
                )
            )

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        first_stage_group: list[StagedTask] = []
        second_stage_group: list[StagedTask] = []

        for task in tasks:
            stage1_duration = task.stage_duration(0)
            stage2_duration = task.stage_duration(1)
            if stage1_duration <= stage2_duration:
                first_stage_group.append(task)
            else:
                second_stage_group.append(task)

        # Первая группа сортируется по возрастанию продолжительности первого этапа,
        # вторая группа - по убыванию продолжительности второго этапа
        first_stage_group.sort(key=lambda t: t.stage_duration(0))
        second_stage_group.sort(key=lambda t: t.stage_duration(1), reverse=True)

        return first_stage_group + second_stage_group

    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса ConveyorSchedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ErrorTemplates.INVALID_STAGE_CNT.format(idx)
                )


if __name__ == "__main__":
    print("Пример использования класса ConveyorSchedule")

    # Инициализируем входные данные для составления расписания
    tasks = [
        StagedTask("a", [7, 2]),
        StagedTask("b", [3, 4]),
        StagedTask("c", [2, 5]),
        StagedTask("d", [4, 1]),
        StagedTask("e", [6, 6]),
        StagedTask("f", [5, 3]),
        StagedTask("g", [4, 5]),
    ]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
