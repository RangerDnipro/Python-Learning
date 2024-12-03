"""
Завдання 7. Парсинг великих лог-файлів для аналітики
Уявіть, що у вас є великий лог-файл від вебсервера. Створіть генератор, який зчитує файл порціями (по рядку) і повертає
тільки рядки з помилками (код статусу 4XX або 5XX). Запишіть ці помилки в окремий файл для подальшого аналізу.
"""


def error_log_generator(file_name):
    """
    Генератор для зчитування великого лог-файлу і повернення лише рядків з помилками (4XX, 5XX)
    :param file_name: Шлях до лог-файлу вебсервера
    :yield: Рядки з кодом статусу 4XX або 5XX
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            # Припустимо, що статусний код знаходиться після методу (GET, POST тощо), у певній позиції
            # Наприклад: '127.0.0.1 - - [10/Oct/2024:13:55:36 +0000] "GET /page HTTP/1.1" 404 209'
            parts = line.split()
            if len(parts) > 8:
                status_code = parts[8]
                if status_code.startswith('4') or status_code.startswith('5'):
                    yield line


def save_error_logs(input_file, output_file):
    """
    Функція для збереження рядків з помилками (HTTP статус 4XX або 5XX) у новий файл
    :param input_file: Вхідний лог-файл для зчитування
    :param output_file: Файл для запису помилкових рядків
    """
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for error_line in error_log_generator(input_file):
            out_file.write(error_line)

    print(f"Рядки з помилками успішно збережені у файл {output_file}")


# Приклад використання генератора для обробки лог-файлу
# Шлях до лог-файлу веб-сервера
input_file = 'homework_05_07_log.txt'
# Файл для збереження рядків з помилками
output_file = 'homework_05_07_error.txt'
save_error_logs(input_file, output_file)
