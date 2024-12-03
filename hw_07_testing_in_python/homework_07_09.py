"""
Завдання 9. Тестування різних сценаріїв скіпів та умов (опціонально)
Завдання: Напишіть програму для перевірки віку користувачів та додайте різні скіпи та умови у тестах
Реалізуйте клас AgeVerifier, який перевіряє вік:
is_adult(age: int) -> bool: повертає True, якщо вік більше або дорівнює 18.
Напишіть тести, які:
перевіряють коректну роботу функції для різного віку,
пропускають тест, якщо вік менший за 0 (некоректне значення), з використанням pytest.mark.skip.
Додайте умовний скіп, який пропустить тест, якщо вік понад 120, тому що це малоймовірний сценарій:
@pytest.mark.skipif(age > 120, reason="Неправильне значення віку")
def test_is_adult():
     assert AgeVerifier.is_adult(121) == False
"""

# pylint: disable=too-few-public-methods

import pytest


class AgeVerifier:
    """
    Клас для перевірки віку користувачів
    """

    @staticmethod
    def is_adult(age: int) -> bool:
        """
        Перевіряє, чи є користувач дорослим (вік >= 18).

        :param age: Вік користувача, має бути додатним цілим числом
        :return: True, якщо вік більше або дорівнює 18, False - якщо менше
        """
        if age < 0:
            raise ValueError("Вік не може бути від'ємним числом")
        return age >= 18


# Тести для перевірки коректної роботи функції для різних значень віку
def test_is_adult_correct_values():
    """
    Тест перевіряє функцію is_adult для різних значень віку.
    """
    assert AgeVerifier.is_adult(18) is True
    assert not AgeVerifier.is_adult(17)
    assert AgeVerifier.is_adult(30) is True
    assert not AgeVerifier.is_adult(0)


# Тест, що пропускається для некоректного значення віку
@pytest.mark.skip(reason="Некоректне від'ємне значення віку")
def test_is_adult_negative_age():
    """
    Тест перевіряє, що функція правильно реагує на від'ємний вік
    """
    with pytest.raises(ValueError):
        AgeVerifier.is_adult(-5)


# Тест з умовним скіпом для малоймовірного сценарію (вік понад 120)
@pytest.mark.skipif(AgeVerifier.is_adult(121), reason="Неправильне значення віку")
def test_is_adult_age_above_120():
    """
    Тест перевіряє значення віку понад 120 років
    """
    assert not AgeVerifier.is_adult(121)


# Запуск тестів
if __name__ == "__main__":
    pytest.main([__file__])
