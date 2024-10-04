"""
Завдання 11. Інкрементне обчислення середніх значень (опціонально)
Напишіть генератор, який по черзі зчитує великий файл даних (наприклад, числові показники продуктивності),
обчислює середнє значення на кожній ітерації та оновлює результат. Це корисно для обробки великих даних,
які не можна завантажити повністю в пам'ять.
"""


class IncrementalAverage:
    """
    Генератор для інкрементного обчислення середнього значення з файлу, що містить числові показники
    """

    def __init__(self, filename):
        """
        Ініціалізація генератора
        :param filename: Ім'я файлу, з якого читатимуться числові показники
        """
        self.filename = filename
        self.total_sum = 0.0
        self.count = 0

    def __iter__(self):
        """
        Повертає сам об'єкт для ітерації
        :return: Повертає сам себе
        """
        return self

    def __next__(self):
        """
        Повертає середнє значення на кожній ітерації
        :return: Середнє значення чисел, прочитаних до поточного моменту
        :raises StopIteration: Якщо всі рядки зчитано
        """
        if not hasattr(self, 'file'):
            # Відкриваємо файл тільки при першому виклику
            self.file = open(self.filename, 'r')

        line = self.file.readline()
        # Якщо файл закінчився
        if not line:
            self.file.close()
            raise StopIteration

        # Перевірка на числове значення, якщо, наприклад, строка - пропускаємо
        try:
            number = float(line.strip())
        except ValueError:
            return self.__next__()

        self.total_sum += number
        self.count += 1

        return self.total_sum / self.count if self.count > 0 else 0.0


# Використання генератора
filename = "homework_05_11.txt"
avg_gen = IncrementalAverage(filename)
for avg in avg_gen:
    print(f"Середнє значення на поточному кроці: {avg:.2f}")
