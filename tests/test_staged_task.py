import unittest

from schedules.constants import STAGED_TASK_STR_TEMPL
from schedules.task import Task
from schedules.staged_task import StagedTask
from schedules.errors import (
    TaskArgumentError,
    ErrorMessages,
    ErrorTemplates,
)


class TestStagedTask(unittest.TestCase):
    name = "a"
    stage_0_duration = 1
    stage_1_duration = 2
    stage_2_duration = 3
    stage_durations = [stage_0_duration, stage_1_duration, stage_2_duration]
    task = StagedTask(name, stage_durations)

    def test_class_inheritance(self):
        """Проверяет наследование от класса Task"""
        self.assertIsInstance(self.task, Task)

    def test_init_incorrect_name(self):
        """Проверяет выброс исключения при некорректном названии задачи"""
        incorrect_name_values = [None, 1, 1.1, True, []]
        for value in incorrect_name_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                StagedTask(value, self.stage_durations)
            self.assertEqual(ErrorMessages.NOT_STR_NAME, str(error.exception))

    def test_init_empty_name(self):
        """Проверяет выброс исключения если название задачи является пустой
        строкой"""
        with self.assertRaises(TaskArgumentError) as error:
            StagedTask("", self.stage_durations)
        self.assertEqual(ErrorMessages.EMPTY_NAME, str(error.exception))

    def test_init_not_list_duration(self):
        """Проверяет выброс исключения при некорректном типе данных списка
        этапов задачи"""
        incorrect_durations_values = [None, "1", {}]
        for value in incorrect_durations_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                StagedTask(self.name, value)
            self.assertEqual(ErrorMessages.NOT_LIST_DUR, str(error.exception))

    def test_init_empty_list_duration(self):
        """Проверяет выброс исключения при передаче пустого списка этапов
        задачи"""
        with self.assertRaises(TaskArgumentError) as error:
            StagedTask(self.name, [])
        self.assertEqual(ErrorMessages.EMPTY_LIST_DUR, str(error.exception))

    def test_init_incorrect_duration(self):
        """Проверяет выброс исключения при некорректной продолжительности
        этапа задачи"""
        incorrect_duration_values = [None, "1", []]
        for value in incorrect_duration_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                stage_durations = [self.stage_0_duration, value]
                StagedTask(self.name, stage_durations)
            self.assertEqual(
                ErrorTemplates.NOT_NUMBER_DUR.format(1), str(error.exception)
            )

    def test_init_non_positive_duration(self):
        """Проверяет выброс исключения если продолжительность этапа задачи
        меньше или равна нулю"""
        incorrect_duration_values = [0, -1, -0.1]
        for value in incorrect_duration_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                stage_durations = [self.stage_0_duration, value]
                StagedTask(self.name, stage_durations)
            self.assertEqual(
                ErrorTemplates.NEG_NUMBER_DUR.format(1), str(error.exception)
            )

    def test_str(self):
        """Проверка приведения задачи к строковому типу"""
        task_str = STAGED_TASK_STR_TEMPL.format(
            self.name, sum(self.stage_durations), len(self.stage_durations)
        )
        self.assertEqual(task_str, str(self.task))

    def test_name_property(self):
        """Проверка свойства name"""
        self.assertEqual(self.task.name, self.name)

    def test_duration_property(self):
        """Проверка свойства duration"""
        self.assertEqual(self.task.duration, sum(self.stage_durations))

    def test_stage_count_property(self):
        """Проверка свойства stage_count"""
        self.assertEqual(self.task.stage_count, len(self.stage_durations))

    def test_stage_durations_property(self):
        """Проверка свойства stage_count"""
        self.assertEqual(self.task.stage_durations, tuple(self.stage_durations))

    def test_stage_duration(self):
        """Проверка метода получения длительности этапа"""
        self.assertEqual(self.task.stage_duration(1), self.stage_1_duration)

    def test_stage_duration_not_int_idx(self):
        """Проверка выброса исключения при нечисловом индексе этапа"""
        incorrect_idx_values = [None, "1", -1, 1.1, {}]
        for value in incorrect_idx_values:
            with (
                self.subTest(value=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                self.task.stage_duration(value)
            self.assertEqual(ErrorMessages.STAGE_NOT_INT, str(error.exception))

    def test_stage_duration_incorrect_idx(self):
        """Проверка выброса исключения при некорректном индексе этапа"""
        with self.assertRaises(TaskArgumentError) as error:
            self.task.stage_duration(len(self.stage_durations) + 1)
        self.assertEqual(ErrorMessages.STAGE_OUT_OF_RANGE, str(error.exception))

    def test_eq(self):
        """Проверка операции эквивалентности заданий"""
        task1 = StagedTask("a", [1, 1, 1])
        task2 = StagedTask("a", [1, 1, 1])
        self.assertTrue(task1 == task2)
        self.assertTrue(hash(task1) == hash(task2))

    def test_not_eq(self):
        """Проверка операции неэквивалентности заданий"""
        task1 = StagedTask("a", [1.1, 1, 1])
        task2 = StagedTask("a", [1, 1, 1])
        self.assertTrue(task1 != task2)
        self.assertTrue(hash(task1) != hash(task2))


if __name__ == "__main__":
    unittest.main()
