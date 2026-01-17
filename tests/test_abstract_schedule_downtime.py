import unittest

from schedules.conveyor_schedule import ConveyorSchedule
from schedules.staged_task import StagedTask


class TestAbstractScheduleDowntime(unittest.TestCase):
    def test_single_task_downtime(self):
        """Проверяет корректность вычисления простоев для одной задачи."""
        task_a = StagedTask("a", [1, 2])
        schedule = ConveyorSchedule([task_a])

        self.assertEqual(2, schedule.get_executor_downtime(0))
        self.assertEqual(1, schedule.get_executor_downtime(1))
        self.assertEqual(3, schedule.get_total_downtime())

    def test_sevenfold_downtime(self):
        """Проверяет корректность вычисления простоев для семи задач."""
        task_a = StagedTask("a", [7, 2])
        task_b = StagedTask("b", [3, 4])
        task_c = StagedTask("c", [2, 5])
        task_d = StagedTask("d", [4, 1])
        task_e = StagedTask("e", [6, 6])
        task_f = StagedTask("f", [5, 3])
        task_g = StagedTask("g", [4, 5])

        schedule = ConveyorSchedule(
            [task_a, task_b, task_c, task_d, task_e, task_f, task_g]
        )

        # Для первой задачи (конвейер 1) есть один простой с 31 по 32
        self.assertEqual(1, schedule.get_executor_downtime(0))

        # Для второй задачи (конвейер 2) ожидаются простои:
        # [0, 2], [25, 27], [29, 31] -> суммарно 6
        self.assertEqual(6, schedule.get_executor_downtime(1))

        self.assertEqual(7, schedule.get_total_downtime())


if __name__ == "__main__":
    unittest.main()
