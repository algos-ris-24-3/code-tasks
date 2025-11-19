def fibonacci_rec(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:   
    arr = [1] * n

    for i in range(2, n):
        arr[i] = arr[i - 1] + arr[i - 2]

    return arr[n - 1]


def fibonacci(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    first, second = 1, 1
    for i in range(n - 2):
        first, second = second, first + second

    return second


def main():
    n = 35
    print(f"Вычисление {n} числа Фибоначчи рекурсивно:")
    print(fibonacci_rec(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно:")
    print(fibonacci_iter(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно без использования массива:")
    print(fibonacci(n))


if __name__ == "__main__":
    main()
