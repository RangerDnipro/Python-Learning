"""
12. Зчитування великих бінарних файлів (опціонально)
Напишіть програму, яка використовує менеджер контексту для зчитування бінарних файлів великими блоками даних
(наприклад, по 1024 байти). Виведіть кількість прочитаних байтів.
"""


class BinaryFileReader:
    """
    Менеджер контексту для зчитування бінарних файлів великими блоками
    """

    def __init__(self, filename, block_size=1024):
        """
        Ініціалізація менеджера контексту
        :param filename: Ім'я бінарного файлу для зчитування
        :param block_size: Розмір блоку даних (за замовчуванням 1024 байти)
        """
        self.filename = filename
        self.block_size = block_size
        self.file = None

    def __enter__(self):
        """
        Відкриває файл для зчитування в бінарному режимі
        :return: Повертає об'єкт файла
        """
        self.file = open(self.filename, 'rb')
        return self

    def read_blocks(self):
        """
        Читає файл блоками та повертає кількість прочитаних байт
        :yield: Кількість прочитаних байт за кожен блок
        """
        while True:
            # Зчитуємо блок даних
            block = self.file.read(self.block_size)
            if not block:
                # Виходимо, якщо досягнуто кінець файлу
                break
            # Повертаємо кількість прочитаних байт
            yield len(block)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закриває файл при виході з контексту
        :param exc_type: Тип виключення
        :param exc_val: Значення виключення
        :param exc_tb: Трекбек виключення
        """
        if self.file:
            self.file.close()


# Використання менеджера контексту
filename = "homework_05_12.bin"

with BinaryFileReader(filename) as reader:
    total_bytes = 0
    for bytes_read in reader.read_blocks():
        print(f"Прочитано байт: {bytes_read}")
        total_bytes += bytes_read

    print(f"Загальна кількість прочитаних байт: {total_bytes}")
