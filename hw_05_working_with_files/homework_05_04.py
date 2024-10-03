"""
Завдання 4. Генератор для обробки великих файлів
Реалізуйте генератор, який читає великий текстовий файл рядок за рядком (наприклад, лог-файл) і повертає лише ті рядки,
що містять певне ключове слово. Використайте цей генератор для фільтрації файлу та запису відповідних рядків у новий файл.
"""


def line_filter(file_name, keyword):
    """
    Генератор для фільтрації рядків у великому файлі, які містять ключове слово.
    :param file_name: Ім'я файлу, який буде зчитуватися.
    :param keyword: Ключове слово, яке повинно бути присутнє в рядку.
    :yield: Рядки, що містять ключове слово.
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            if keyword in line:
                yield line


def save_filtered_lines(input_file, output_file, keyword):
    """
    Використовує генератор для фільтрації рядків з вхідного файлу та записує результат у новий файл.
    :param input_file: Вхідний файл для читання.
    :param output_file: Файл для запису відфільтрованих рядків.
    :param keyword: Ключове слово для пошуку у рядках.
    """
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for line in line_filter(input_file, keyword):
            out_file.write(line)

    print(f"Фільтровані рядки успішно збережені у файл {output_file}")


# Використання генератора для фільтрації файлу
input_file = 'homework_05_01.txt'
output_file = 'homework_05_04.txt'
# Ключове слово для пошуку
keyword = 'Ітератор'
save_filtered_lines(input_file, output_file, keyword)
