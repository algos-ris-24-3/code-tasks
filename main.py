from profilehooks import profile

def fibonacci_rec(n: int) -> int:
    if(n == 1 or n == 2):
        return 1
    
    return (fibonacci_rec(n - 1) + fibonacci_rec(n - 2))

def fibonacci_iter(n: int) -> int:
    a = [1] * n
    
    for i in range(2, n):
        a[i] = a[i - 1] + a[i - 2]
    return a[n - 1]


def fibonacci(n: int) -> int:
    if(n == 1 or n == 2):
        return 1

    n1, n2 = 1, 1
    
    for i in range(2,n):
        n1, n2 = n2, n1 + n2

    return n2

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
