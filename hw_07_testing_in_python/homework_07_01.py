"""
Завдання 1. Модульне тестування з використанням unittest
Напишіть простий застосунок для обробки рядків та напишіть модульні тести
з використанням бібліотеки unittest.
Створіть клас StringProcessor з методами:
reverse_string(s: str) -> str: повертає перевернутий рядок.
capitalize_string(s: str) -> str: робить першу літеру рядка великої.
count_vowels(s: str) -> int: повертає кількість голосних у рядку.
Напишіть тести для кожного методу, перевіряючи кілька різних сценаріїв:
- порожні рядки,
- рядки з різними регістрами,
- рядки з цифрами та символами.
Використовуйте декоратор @unittest.skip для пропуску тесту, який тестує
метод reverse_string з порожнім рядком, оскільки це відома проблема,
яку ви плануєте вирішити пізніше.
"""

import unittest


class StringProcessor:
    """
    Клас для обробки рядків, який надає методи для перевертання,
    капіталізації та підрахунку голосних у рядках
    """

    def reverse_string(self, s: str) -> str:
        """
        Повертає перевернутий рядок
        :param s: Вхідний рядок для перевертання
        :return: Перевернутий рядок
        """
        return s[::-1]

    def capitalize_string(self, s: str) -> str:
        """
        Робить першу літеру рядка великою
        :param s: Вхідний рядок для капіталізації
        :return: Рядок з великою першою літерою
        """
        return s.capitalize()

    def count_vowels(self, s: str) -> int:
        """
        Повертає кількість голосних у рядку
        :param s: Вхідний рядок для підрахунку голосних
        :return: Кількість голосних у рядку
        """
        vowels = "aeiouAEIOU"
        return sum(1 for char in s if char in vowels)


class TestStringProcessor(unittest.TestCase):
    """
    Набір тестів для перевірки функціональності класу StringProcessor
    """

    def setUp(self) -> None:
        """
        Ініціалізує об'єкт StringProcessor для тестування
        """
        self.processor = StringProcessor()

    @unittest.skip("Тест пропущено через відому проблему з порожнім рядком")
    def test_reverse_string_empty(self) -> None:
        """
        Перевіряє метод reverse_string з порожнім рядком
        """
        self.assertEqual(self.processor.reverse_string(''), '')

    def test_reverse_string_normal(self) -> None:
        """
        Перевіряє метод reverse_string з нормальним рядком
        """
        self.assertEqual(self.processor.reverse_string('hello'), 'olleh')

    def test_reverse_string_with_symbols(self) -> None:
        """
        Перевіряє метод reverse_string з рядком, що містить символи
        """
        self.assertEqual(self.processor.reverse_string('123!@#'), '#@!321')

    def test_capitalize_string_empty(self) -> None:
        """
        Перевіряє метод capitalize_string з порожнім рядком
        """
        self.assertEqual(self.processor.capitalize_string(''), '')

    def test_capitalize_string_lowercase(self) -> None:
        """
        Перевіряє метод capitalize_string з рядком, де всі літери малі
        """
        self.assertEqual(self.processor.capitalize_string('hello'), 'Hello')

    def test_capitalize_string_uppercase(self) -> None:
        """
        Перевіряє метод capitalize_string з рядком, де всі літери великі
        """
        self.assertEqual(self.processor.capitalize_string('HELLO'), 'Hello')

    def test_capitalize_string_with_numbers(self) -> None:
        """
        Перевіряє метод capitalize_string з рядком, що містить цифри
        """
        self.assertEqual(self.processor.capitalize_string('123hello'), '123hello')

    def test_count_vowels_empty(self) -> None:
        """
        Перевіряє метод count_vowels з порожнім рядком
        """
        self.assertEqual(self.processor.count_vowels(''), 0)

    def test_count_vowels_lowercase(self) -> None:
        """
        Перевіряє метод count_vowels з рядком, де всі літери малі
        """
        self.assertEqual(self.processor.count_vowels('hello'), 2)

    def test_count_vowels_uppercase(self) -> None:
        """
        Перевіряє метод count_vowels з рядком, де всі літери великі
        """
        self.assertEqual(self.processor.count_vowels('HELLO'), 2)

    def test_count_vowels_with_numbers_and_symbols(self) -> None:
        """
        Перевіряє метод count_vowels з рядком, що містить цифри та символи
        """
        self.assertEqual(self.processor.count_vowels('123!aEiou'), 5)


if __name__ == '__main__':
    unittest.main()
