from data_structures.lists.doubly_linked_list.doubly_linked_list import DoublyLinkedList

"""В файле расположен пример использования класса DoublyLinkedList.
Сам класс DoublyLinkedList, который необходимо реализовать, расположен 
в data_structures/lists/doubly_linked_list/doubly_linked_list.py
"""


def main():
    dll = DoublyLinkedList()

    dll.append(10)
    dll.append(20)
    dll.append(30)
    print("После добавления:", dll)

    dll.insert(0, 5)
    print("После вставки в начало:", dll)

    dll.insert(2, 15)
    print("После вставки в середину:", dll)

    dll.remove(20)
    print("После удаления 20:", dll)

    idx = dll.index(30)
    print(f"Индекс элемента 30: {idx}")

    print("Размер списка:", len(dll))

    print("Элементы списка:", [x for x in dll])

    print("Обратный обход:", [x for x in reversed(dll)])
