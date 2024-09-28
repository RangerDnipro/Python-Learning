"""
Завдання 5. For built-in functions implementation
1.	Реалізуйте власну версію функцій len(), sum(), та min().
Використовуйте спеціальні методи __len__, __iter__, __getitem__, якщо необхідно.
2.	Напишіть тест для кожної з реалізованих функцій.
"""


class MyList:
    def __init__(self, data):
        """
        Ініціалізація списку на основі переданих елементів.
        :param data: список елементів
        """
        self.data = data

    def __len__(self):
        """
        Повертає кількість елементів у списку.
        :return: довжина списку
        """
        count = 0
        for _ in self.data:
            count += 1
        return count

    def __sum__(self):
        """
        Повертає суму елементів у списку.
        :return: сума елементів
        """
        total = 0
        for item in self.data:
            total += item
        return total

    def __min__(self):
        """
        Повертає мінімальний елемент у списку.
        :return: мінімальний елемент
        """
        if self.__len__() > 0:
            smallest = self.data[0]
            for value in self.data[1:]:
                if value < smallest:
                    smallest = value
            return smallest
        else:
            raise ValueError("Порожній об'єкт")

    def __repr__(self):
        """
        Повертає рядкове представлення класу у вигляді MyList: зміст
        :return: рядок
        """
        return f"MyList:{self.data}"


def my_len(obj):
    """
    Власна версія функції len().
    :param obj: об'єкт MyList
    :return: кількість елементів у списку
    """
    return obj.__len__()


def my_sum(obj):
    """
    Власна версія функції sum().
    :param obj: об'єкт MyList
    :return: сума елементів у списку
    """
    return obj.__sum__()


def my_min(obj):
    """
    Власна версія функції min().
    :param obj: об'єкт MyList
    :return: мінімальний елемент у списку
    """
    return obj.__min__()


# Тестування власних версій функцій
# Перевірка на списку
my_list = MyList([1, 2, 3, 4, 5])
print(f"Довжина {my_list} складає {my_len(my_list)}")
print(f"Сума {my_list} складає {my_sum(my_list)}")
print(f"Мінімальний елемент {my_list} це {my_min(my_list)}\n")

# Перевірка на порожньому списку
empty_list = MyList([])
print(f"Довжина {empty_list} складає {my_len(empty_list)}")
print(f"Сума {empty_list} складає {my_sum(empty_list)}")
try:
    my_min(empty_list)
except ValueError:
    print("Для мінімального елемента порожнього списку виникає виняток ValueError")
    pass
