"""
Завдання 1. Створення власного ітератора для зворотного читання файлу
Напишіть власний ітератор, який буде зчитувати файл у зворотному порядку — рядок за рядком з кінця файлу до початку
Це може бути корисно для аналізу лог-файлів, коли останні записи найважливіші
"""


class ReverseFileLineIterator:
    """
    Ітератор для зчитування файлу рядок за рядком у зворотному порядку без зчитування всього файлу в пам'ять.
    """

    def __init__(self, file_name):
        """
        Ініціалізація ітератора, відкриття файлу для читання з кінця до початку.
        :param file_name: Ім'я файлу, який буде зчитуватися
        """
        # Відкриваємо файл у двійковому режимі
        self.file = open(file_name, 'rb')
        # Переміщаємося в кінець файлу
        self.file.seek(0, 2)
        # Зберігаємо поточну позицію в файлі
        self.position = self.file.tell()

    def __iter__(self):
        """
        Повертає сам ітератор.
        """
        return self

    def __next__(self):
        """
        Повертає наступний рядок з файлу у зворотному порядку. Якщо досягнуто початок файлу, зупиняє ітерацію.
        :return: Наступний рядок у зворотному порядку
        """
        if self.position <= 0:
            self.file.close()
            raise StopIteration

        line = b''
        while self.position > 0:
            self.position -= 1
            self.file.seek(self.position)
            char = self.file.read(1)

            if char == b'\n' and line:
                # Рядок у зворотному порядку, повертаємо в форматі 'utf-8'
                return line[::-1].decode('utf-8')

            line += char

        return line[::-1].decode('utf-8') if line else self._stop_iteration()

    def _stop_iteration(self):
        """
        Зупиняє ітерацію та закриває файл.
        """
        self.file.close()
        raise StopIteration


# Використання ітератора для читання з файлу у зворотному порядку
file_iterator = ReverseFileLineIterator('homework_05_01.txt')
for line in file_iterator:
    print(line)
