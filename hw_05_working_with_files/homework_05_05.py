"""
Завдання 5. Генератор для створення нескінченної послідовності
Створіть генератор, який генерує нескінченну послідовність парних чисел.
Використайте менеджер контексту для обмеження кількості генерованих чисел до 100 і збереження їх у файл.
"""


def even_number_generator():
    """
    Генератор для створення нескінченної послідовності парних чисел
    :yield: Парне число, починаючи з 2
    """
    num = 2
    while True:
        yield num
        num += 2


class LimitedGenerator:
    """
    Менеджер контексту для обмеження кількості згенерованих чисел
    """

    def __init__(self, generator, limit):
        """
        Ініціалізація менеджера контексту
        :param generator: Генератор, який буде обмежений
        :param limit: Кількість елементів, яку потрібно згенерувати
        """
        self.generator = generator
        self.limit = limit

    def __enter__(self):
        """
        Входження в контекст, ініціалізація генерації
        :return: Обмежений генератор
        """
        return (next(self.generator) for _ in range(self.limit))

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Вихід з контексту (очищення, якщо потрібно)
        """
        pass


def save_even_numbers_to_file(file_name, limit):
    """
    Функція для збереження згенерованих парних чисел у файл
    :param file_name: Ім'я файлу для збереження чисел
    :param limit: Кількість парних чисел, яку потрібно згенерувати
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        even_gen = even_number_generator()

        # Використання менеджера контексту для обмеження генерації
        with LimitedGenerator(even_gen, limit) as limited_gen:
            for number in limited_gen:
                file.write(f"{number}\n")

    print(f"{limit} парних чисел успішно збережено у файл {file_name}")


# Використання генератора для збереження 100 парних чисел у файл
output_file = 'homework_05_05.txt'
save_even_numbers_to_file(output_file, 100)
