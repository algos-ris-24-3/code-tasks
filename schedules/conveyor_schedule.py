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
        if not hasattr(self, '_executor_schedule'):
            self._executor_schedule = [[], []]
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        if not self._executor_schedule or not self._executor_schedule[1]:
            return 0.0
        return self._executor_schedule[1][-1].end

    def __fill_schedule(self, sorted_tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""

        current_first_machine_time = 0
        current_second_machine_time = 0

        schedule_0 = [] 
        schedule_1 = []  

        for task in sorted_tasks:
            first_stage_time = task.stage_duration(0)
            second_stage_time = task.stage_duration(1)

            first_machine_start = current_first_machine_time
            first_machine_end = first_machine_start + first_stage_time
            current_first_machine_time = first_machine_end

            second_machine_start = max(first_machine_end, current_second_machine_time)
            second_machine_end = second_machine_start + second_stage_time
            current_second_machine_time = second_machine_end

            item_1 = ScheduleItem(task, first_machine_start, first_stage_time)
            item_2 = ScheduleItem(task, second_machine_start, second_stage_time)

            schedule_0.append(item_1)
            schedule_1.append(item_2)

        total_duration = current_second_machine_time

        def add_idles(schedule: list[ScheduleItem], total_duration: float) -> list[ScheduleItem]:
            if not schedule:
                return [ScheduleItem(None, 0, total_duration)] if total_duration > 0 else []
            sorted_schedule = sorted(schedule, key=lambda x: x.start)
            new_schedule = []
            current_time = 0.0
            for item in sorted_sch:
                if item.start > current_time:
                    new_schedule.append(ScheduleItem(None, current_time, item.start - current_time))
                new_schedule.append(item)
                current_time = item.end
            if total_duration > current_time:
                new_schedule.append(ScheduleItem(None, current_time, total_duration - current_time))
            return new_schedule

        self._executor_schedule[0] = add_idles(schedule_0, total_duration)
        self._executor_schedule[1] = add_idles(schedule_1, total_duration)

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""

        first_group = []
        second_group = []

        for task in tasks:
            first_stage_time = task.stage_duration(0)
            second_stage_time = task.stage_duration(1)

            if first_stage_time <= second_stage_time:
                first_group.append((task, first_stage_time))
            else:
                second_group.append((task, second_stage_time))

        first_group.sort(key=lambda x: x[1])
        second_group.sort(key=lambda x: x[1], reverse=True)

        result = []
        for task, _ in first_group:
            result.append(task)

        for task, _ in second_group:
            result.append(task)

        return result

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
                
    def update_tasks(self):
        """
        Изменяет состав задач и перерасчитывает расписание
        """
        tasks = list(self._tasks)
        
        print('Введите новые значения времени для каждой задачи:')
        
        for i, task in enumerate(tasks, 1):
            print(f"Задача: {task.name}, текущее время: [{task.stage_duration(0)}, {task.stage_duration(1)}]")
        
            while True:
                try:
                    input_str = input("Новое время для этапа 1: ").strip()
                    new_first = float(input_str)
                    if new_first < 0:
                        print('Время не может быть отрицательным')
                        continue
                    break
                except ValueError:
                    print('Введите число')
        
            while True:
                try:
                    input_str = input("Новое время для этапа 2: ").strip()
                    new_second = float(input_str)
                    if new_second < 0:
                        print("Время не может быть отрицательным")
                        continue
                    break
                except ValueError:
                    print("Введите число")
        
            tasks[i-1] = StagedTask(task.name, [new_first, new_second])
            print(f"Задача '{task.name}' обновлена")
        
        print('Перерасчет расписания:')
        
        self._tasks = tuple(tasks)
        self._executor_schedule = [[], []]
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

if __name__ == "__main__":
    print("Пример использования класса ConveyorSchedule")

    tasks = [
        StagedTask("a", [7, 2]),
        StagedTask("b", [3, 4]),
        StagedTask("c", [2, 5]),
        StagedTask("d", [4, 1]),
        StagedTask("e", [6, 6]),
        StagedTask("f", [5, 3]),
        StagedTask("g", [4, 5]),
    ]

    schedule = ConveyorSchedule(tasks)

    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)

    print("Хотите изменить состав задач?")
    response = input("Введите 'да' для изменения или Enter для выхода: ").strip().lower()
    
    if response in ['да', 'Да']:
        schedule.update_tasks()
        
        print(schedule)
        for i in range(schedule.executor_count):
            print(f"\nРасписание для исполнителя # {i + 1}:")
            for schedule_item in schedule.get_schedule_for_executor(i):
                print(schedule_item)
