from typing import Any


def generate_permutations(items: list[Any]) -> list[list[Any]]:
    if not isinstance(items, list):
        raise TypeError("Параметр items не является списком")

    if len(items) != len(set(items)):
        raise ValueError("Список элементов содержит дубликаты")

    if len(items) == 0:
        return []

    if len(items) == 1:
        return [items.copy()]

    prev_perms = generate_permutations(items[:-1])
    last_elem = items[-1]
    result: list[list[Any]] = []

    for perm in prev_perms:
        for pos in range(len(perm) + 1):
            result.append(perm[:pos] + [last_elem] + perm[pos:])

    return result
