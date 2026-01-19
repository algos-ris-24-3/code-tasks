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
        if not self._executor_schedule[0]:
            return 0.0
        dur = self._executor_schedule[0][-1].end
        return int(dur) if dur.is_integer() else dur

    def add_task(self, task: StagedTask) -> None:
        """Добавляет задачу и пересчитывает расписание."""
        if not isinstance(task, StagedTask):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if task.stage_count != 2:
            raise ScheduleArgumentError(ErrorTemplates.INVALID_STAGE_CNT.format("new"))
        
        # Проверка на дубликат
        for existing_task in self._tasks:
            if existing_task.name == task.name:
                raise ScheduleArgumentError(f"Задача с таким именем'{task.name}' уже есть.")
        
        self._tasks.append(task)
        self.__recalculate_schedule()

    def remove_task(self, task_name: str) -> None:
        """Удаляет задачу по имени и пересчитывает расписание."""
        for index, task in enumerate(self._tasks):
            if task.name == task_name:
                del self._tasks[index]
                self.__recalculate_schedule()
                return
        raise ScheduleArgumentError(f"Задача с таким именем '{task_name}' не найдена.")
    

    def __recalculate_schedule(self) -> None:
        """Полностью перестраивает расписание на основе текущих задач."""
        self._executor_schedule = [[], []]
        if self._tasks:
            sorted_tasks = ConveyorSchedule.__sort_tasks(self._tasks)
            self.__fill_schedule(sorted_tasks)


    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""
        time1 = 0.0
        time2 = 0.0
        for task in tasks:
            duration_first = task.stage_duration(0)
            self._executor_schedule[0].append(ScheduleItem(task, time1, duration_first))
            time1 = time1 + duration_first

            start2 = max(time2, time1)
            if time2 < time1:
                downtime_duration = time1 - time2
                self._executor_schedule[1].append(ScheduleItem(None, time2, downtime_duration))
            duration2 = task.stage_duration(1)
            self._executor_schedule[1].append(ScheduleItem(task, start2, duration2))
            time2 = start2 + duration2
    
        if time2 > time1:
            downtime_duration = time2 - time1
            self._executor_schedule[0].append(ScheduleItem(None, time1, downtime_duration))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        left = []
        right = []
        for task in tasks:
            a, b = task.stage_duration(0), task.stage_duration(1)
            if a < b:
                left.append(task)
            else:
                right.append(task)
        left.sort(key=lambda x: x.stage_duration(0))
        right.sort(key=lambda x: x.stage_duration(1), reverse=True)
        return left + right

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
