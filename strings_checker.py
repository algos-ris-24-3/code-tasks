def get_string_count(target_string_length: int) -> int:
    if target_string_length == 1:
        return 2
    prev, preprev = 2, 1

    for _ in range(1, target_string_length):
        prev, preprev = prev + preprev, prev

    return prev


def check_strings(strings: list[str], target_string_length: int) -> bool:
    """Проверяет список строк содержит все строки заданной длины из нулей
    и единиц, где никакие два нуля не стоит рядом.

    param strings: Список строк для проверки.
    param target_string_length: Длина строки.

    return: Результат проверки.
    """
    if target_string_length < 0:
        return False
    if target_string_length == 0:
        return strings == []

    seen = set()
    for s in strings:
        if not isinstance(s, str):
            return False
        if len(s) != target_string_length:
            return False
        if any(ch not in "01" for ch in s):
            return False
        if "00" in s:
            return False
        if s in seen:
            return False
        seen.add(s)

    return len(strings) == get_string_count(target_string_length)


def main():

    correct_strings = ["01", "10", "11"]
    incorrect_strings = ["01", "10", "00"]

    print("Проверка корректного набора строк")
    print("Набор:")
    [print(string) for string in correct_strings]
    print(f"Результат проверки: {check_strings(correct_strings, 2)}")

    print("Проверка некорректного набора строк")
    print("Набор:")
    [print(string) for string in incorrect_strings]
    print(f"Результат проверки: {check_strings(incorrect_strings, 2)}")


if __name__ == "__main__":
    main()
