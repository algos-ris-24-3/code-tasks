import time


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    pass


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    while b > 0:
        a, b = b, a - b
    return a



def gcd_iterative_fast(a: int, b: int) -> int:
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return a * b / gcd_iterative_fast(a,b)


def main():
    a = 1005002
    b = 1354
    print(f"Вычисление НОД чисел {a} и {b} рекурсивно:")
    start_time = time.time()
    print(gcd_recursive(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с вычитанием:")
    start_time = time.time()
    print(gcd_iterative_slow(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с делением:")
    start_time = time.time()
    print(gcd_iterative_fast(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОК чисел {a} и {b}:")
    start_time = time.time()
    print(lcm(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")


if __name__ == "__main__":
    main()
