"""
Завдання 7. Vector class implementation
1.	Створіть клас Vector, який представляє вектор у просторі з n вимірами.
Додайте методи для додавання, віднімання векторів та обчислення скалярного добутку.
Використовуйте dunder-методи (__add__, __sub__, __mul__).
2.	Додайте можливість порівняння двох векторів за їх довжиною.
"""

import math


class Vector:
    def __init__(self, *components):
        """
        Ініціалізує вектор з будь-якою кількістю компонентів.
        :param components: компоненти вектора
        """
        self.components = components

    def __add__(self, other):
        """
        Додає два вектори
        :param other: інший вектор
        :return: новий вектор як сума
        """
        if len(self.components) != len(other.components):
            raise ValueError("Вектори повинні мати однакову розмірність")
        return Vector(*(x + y for x, y in zip(self.components, other.components)))

    def __sub__(self, other):
        """
        Віднімає два вектори
        :param other: інший вектор
        :return: новий вектор як різниця
        """
        if len(self.components) != len(other.components):
            raise ValueError("Вектори повинні мати однакову розмірність")
        return Vector(*(x - y for x, y in zip(self.components, other.components)))

    def __mul__(self, other):
        """
        Обчислює скалярний добуток двох векторів.
        :param other: інший вектор
        :return: скалярний добуток
        """
        if len(self.components) != len(other.components):
            raise ValueError("Вектори повинні мати однакову розмірність")
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        """
        Обчислює довжину (модуль) вектора.
        :return: довжина вектора
        """
        return math.sqrt(sum(x ** 2 for x in self.components))

    def __lt__(self, other):
        """
        Порівнює два вектори за їх довжиною.
        :param other: інший вектор
        :return: True, якщо довжина поточного вектора менша за довжину іншого
        """
        return self.magnitude() < other.magnitude()

    def __eq__(self, other):
        """
        Перевіряє рівність двох векторів за їх довжиною.
        :param other: інший вектор
        :return: True, якщо довжини векторів рівні
        """
        return self.magnitude() == other.magnitude()

    def __repr__(self):
        """
        Повертає рядкове представлення вектора.
        :return: рядок з компонентами вектора
        """
        return f"Vector{self.components}"


# Приклад використання для операцій з векторами, а саме:
# ...створення
print("Створюємо два вектори довільної вимірності")
print(vec1 := Vector(1, 2, 3, 4))
print(vec2 := Vector(4, 5, 9, 5))
# ...додавання
print(f"Сума {vec1} та {vec2} складає {vec1 + vec2}")
# ...віднімання
print(f"Різниця {vec1} та {vec2} складає {vec1 - vec2}")
# ...множення
print(f"Добуток {vec1} та {vec2} складає {vec1 * vec2}")
# ...отримання довжин векторів
print(f"Довжина {vec1} складає {vec1.magnitude()}")
print(f"Довжина {vec2} складає {vec2.magnitude()}")
# ...порівняння за довжиною
if vec1 < vec2:
    print(f"{vec1} менший ніж {vec2}")
elif vec1 == vec2:
    print(f"{vec1} більший ніж {vec2}")
else:
    print(f"{vec1} дорівнює {vec2}")
