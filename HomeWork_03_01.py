"""
Завдання 1. Dunder methods
1.	Реалізуйте клас Fraction (дробові числа), який має методи для додавання, віднімання,
множення та ділення двох об'єктів цього класу. Використайте спеціальні методи __add__, __sub__, __mul__, __truediv__.
2.	Реалізуйте метод __repr__, щоб можна було коректно виводити об'єкти цього класу у форматі "numerator/denominator".
"""


class Fraction:
    def __init__(self, numerator, denominator):
        """
        Ініціалізація дробу з чисельником і знаменником.
        :param numerator: чисельник дробу
        :param denominator: знаменник дробу
        """
        if denominator == 0:
            raise ValueError("Знаменник не може дорівнювати нулю")
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, other):
        """
        Додає два дроби.
        :param other: інший об'єкт Fraction
        :return: новий об'єкт Fraction
        """
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other):
        """
        Віднімає один дріб від іншого.
        :param other: інший об'єкт Fraction
        :return: новий об'єкт Fraction
        """
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        """
        Множить два дроби.
        :param other: інший об'єкт Fraction
        :return: новий об'єкт Fraction
        """
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        """
        Ділить два дроби.
        :param other: інший об'єкт Fraction
        :return: новий об'єкт Fraction
        """
        if other.numerator == 0:
            raise ZeroDivisionError("Не можна ділити на нуль")
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)

    def __repr__(self):
        """
        Повертає рядкове представлення дробу у вигляді "numerator/denominator".
        :return: рядок
        """
        return f"{self.numerator}/{self.denominator}"


# Тестування (завдання скорочування дробі не було)
frac1 = Fraction(3, 4)
frac2 = Fraction(1, 4)
print(frac1.__add__(frac2))
print(frac1.__sub__(frac2))
print(frac1.__mul__(frac2))
print(frac1.__truediv__(frac2))

# Тестування з використанням assert
if __name__ == "__main__":
    frac1 = Fraction(1, 2)  # 1/2
    frac2 = Fraction(1, 3)  # 1/3

    # Додавання
    result_add = frac1 + frac2
    assert repr(result_add) == "5/6", f"Expected 5/6, got {repr(result_add)}"

    # Віднімання
    result_sub = frac1 - frac2
    assert repr(result_sub) == "1/6", f"Expected 1/6, got {repr(result_sub)}"

    # Множення
    result_mul = frac1 * frac2
    assert repr(result_mul) == "1/6", f"Expected 1/6, got {repr(result_mul)}"

    # Ділення
    result_div = frac1 / frac2
    assert repr(result_div) == "3/2", f"Expected 3/2, got {repr(result_div)}"

    print("All tests passed!")
