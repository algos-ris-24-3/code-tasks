from problems.sorting_problem.some_sort import some_sort

"""В файле расположен пример использования метода сортировки, который необходимо реализовать.
Метод расположен в problems/sorting_problem/some_sort.py
"""


def main():
    print("Пример сортировки ...")
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print(f"Исходный массив: {items}")
    print(f"Отсортированный массив: {some_sort(items)}")


if __name__ == "__main__":
    main()
