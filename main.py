import time


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    a, b = abs(a), abs(b)
    if a == 0 or b == 0:
        return a + b
    else:
        if a > b:
            return gcd_recursive(a % b, b)
        else:
            return gcd_recursive(a, b % a)


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    a, b = abs(a), abs(b)
    while a != 0 and b != 0:
        if a > b:
            a -= b
        elif b > a:
            b -= a
        else:
            return a
    return a + b


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Быстрая итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    a, b = abs(a), abs(b)
    while a != 0 and b != 0:
        if a > b:
            a %= b
        elif b > a:
            b %= a
        else:
            return a
    return a + b


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел

    :param a: натуральное число a
    :param b: натуральное число b
    :return: значение наименьшего общего кратного
    """
    a, b = abs(a), abs(b)
    c = a * b
    while a != 0 and b != 0:
        if a > b:
            a %= b
        elif b > a:
            b %= a
        else:
            return c // a
    return c // (a + b)


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
