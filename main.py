from data_structures.linked_list.linked_list import LinkedList

"""В файле расположен пример использования класса LinkedList.
Сам класс LinkedList, который необходимо реализовать, расположен 
в data_structures/linked_list/linked_list.py
"""


def main():
    lst = LinkedList()
    print("Создан пустой список:", lst)

    lst.append(10)
    lst.append(20)
    lst.append(30)
    print("После добавления элементов:", lst)

    lst.insert(1, 15)
    print("После вставки 15 в позицию 1:", lst)

    lst.remove(20)
    print("После удаления элемента 20:", lst)

    idx = lst.index(30)
    print("Индекс элемента 30:", idx)
    print("Поиск отсутствующего элемента:", lst.index(99))

    print("Элементы в списке через цикл for:")
    for x in lst:
        print(x)

    print("Длина списка:", len(lst))


if __name__ == "__main__":
    main()
