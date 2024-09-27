"""
Завдання 2. Numeric-like
1.	Реалізуйте клас Vector, що підтримує операції додавання, віднімання, множення на число та порівняння за довжиною.
Використовуйте відповідні dunder-методи (__add__, __sub__, __mul__, __lt__, __eq__).
2.	Додайте до класу метод для отримання довжини вектора.
"""

import math


class Vector:
    def __init__(self, *components):
        """
        Ініціалізація вектора з набору компонент
        :param components: координати вектора
        """
        self.components = components

    def __add__(self, other):
        """
        Додає два вектори
        Реалізуємо перевірку для порівняння розмірностей двох векторів
        :param other: інший об'єкт Vector
        :return: новий об'єкт Vector
        """
        if len(self.components) != len(other.components):
            raise ValueError("Вектори повинні мати однакову розмірність")
        return Vector(*(x + y for x, y in zip(self.components, other.components)))

    def __sub__(self, other):
        """
        Віднімає один вектор від іншого
        Реалізуємо перевірку для порівняння розмірностей двох векторів
        :param other: інший об'єкт Vector
        :return: новий об'єкт Vector
        """
        if len(self.components) != len(other.components):
            raise ValueError("Вектори повинні мати однакову розмірність")
        return Vector(*(x - y for x, y in zip(self.components, other.components)))

    def __mul__(self, scalar):
        """
        Множить вектор на число
        :param scalar: число
        :return: новий об'єкт Vector
        """
        return Vector(*(x * scalar for x in self.components))

    def __eq__(self, other):
        """
        Порівнює два вектори на рівність довжини
        :param other: інший об'єкт Vector
        :return: True, якщо довжини однакові, False — якщо ні
        """
        return self.magnitude() == other.magnitude()

    def magnitude(self):
        """
        Обчислює довжину вектора (модуль)
        :return: довжина вектора
        """
        return math.sqrt(sum(x ** 2 for x in self.components))

    def __repr__(self):
        """
        Повертає рядкове представлення вектора у вигляді "Vector(components)"
        :return: рядок
        """
        return f"Vector{self.components}"


# Приклад використання для операцій з векторами, а саме:
# ...створення
print(vec1 := Vector(1, 2, 3))
print(vec2 := Vector(4, 5, 9))
# ...додавання
print(vec1 + vec2)
# ...віднімання
print(vec1 - vec2)
# ...множення на число
print(vec1 * 3)
# ...порівняння за довжиною
print(vec1 == vec2)
# ...отримання довжини вектора
print(vec1.magnitude())
print(vec2.magnitude())

# Тестування з використанням assert
if __name__ == "__main__":
    vec1 = Vector(1, 2, 3)
    vec2 = Vector(4, 5, 6)

    # Додавання
    result_add = vec1 + vec2
    assert repr(result_add) == "Vector(5, 7, 9)", f"Expected Vector(5, 7, 9), got {repr(result_add)}"

    # Віднімання
    result_sub = vec1 - vec2
    assert repr(result_sub) == "Vector(-3, -3, -3)", f"Expected Vector(-3, -3, -3), got {repr(result_sub)}"

    # Множення на число
    result_mul = vec1 * 2
    assert repr(result_mul) == "Vector(2, 4, 6)", f"Expected Vector(2, 4, 6), got {repr(result_mul)}"

    # Порівняння
    assert (vec1 == vec2) is False, "Expected vec1 to be not equal to vec2"

    print("\nAll tests passed!")
