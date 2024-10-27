"""
Модуль для видалення HTML-тегів з тексту та подальшої обробки змісту, включаючи форматування дат,
видобування хеш-тегів, пошук IP-адрес та перевірку на наявність шаблону
"""

import re


def remove_html_tags(text: str) -> str:
    """
    Видаляє всі HTML-теги з тексту, окрім хеш-тегів
    :param text: Текст, що може містити HTML-теги
    :return: Текст без HTML-тегів
    """
    # Використовуємо регулярний вираз для пошуку всіх HTML-тегів та заміни їх на порожній рядок
    clean_text = re.sub(r'<[^>]*>', '', text)
    # Видалення пустих рядків
    clean_text = re.sub(r'\n\s*\n', '\n', clean_text)
    # Видалення зайвих пробілів на початку непустих рядків
    clean_text = re.sub(r'^\s+', '', clean_text, flags=re.MULTILINE)
    return clean_text


def extract_hashtags(text: str) -> list[str]:
    """
    Видобуває всі хеш-теги з тексту
    :param text: Текст, що може містити хеш-теги
    :return: Список хеш-тегів
    """
    # Використовуємо регулярний вираз для пошуку хеш-тегів
    my_hashtags = re.findall(r'#\w+', text)
    return my_hashtags


def extract_ip_addresses(text: str) -> list[str]:
    """
    Знаходить всі IPv4-адреси в тексті
    :param text: Текст, що може містити IP-адреси
    :return: Список IPv4-адрес
    """
    # Використовуємо регулярний вираз для пошуку IPv4-адрес
    my_ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
    # Фільтруємо адреси, щоб бути впевненими, що вони знаходяться в діапазоні від 0 до 255
    valid_ip_addresses = [ip for ip in my_ip_addresses
                          if all(0 <= int(octet) <= 255 for octet in ip.split('.'))]
    return valid_ip_addresses


def find_pattern(text: str) -> list[str]:
    """
    Перевіряє, чи міститься у тексті рядок формату AB12CD34
    :param text: Текст, що може містити рядки заданого формату
    :return: Список рядків, що відповідають формату AB12CD34
    """
    # Використовуємо регулярний вираз для пошуку рядків формату AB12CD34
    my_pattern_matches = re.findall(r'\b[A-Z]{2}\d{2}[A-Z]{2}\d{2}\b', text)
    return my_pattern_matches


def reformat_dates(text: str) -> str:
    """
    Знаходить всі дати у форматі DD/MM/YYYY і перетворює їх у формат YYYY-MM-DD
    :param text: Текст, що може містити дати у форматі DD/MM/YYYY
    :return: Текст з датами у форматі YYYY-MM-DD
    """

    def replace_date(match: re.Match) -> str:
        day, month, year = match.groups()
        reformatted_date = f"{year}-{month}-{day}"
        print(f"Дату {match.group()} виправлено на {reformatted_date}")
        return reformatted_date

    # Використовуємо регулярний вираз для пошуку дат формату DD/MM/YYYY
    reformatted_text = re.sub(r'\b(\d{2})/(\d{2})/(\d{4})\b', replace_date, text)
    return reformatted_text


if __name__ == "__main__":
    # Читання вмісту з файлу example.html
    with open('example.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Видалення HTML-тегів
    clean_content = remove_html_tags(html_content)

    # Форматування дат у тексті
    reformatted_content = reformat_dates(clean_content)

    # Запис результату з оновленими датами у файл example.txt
    with open('example.txt', 'w', encoding='utf-8') as file:
        file.write(reformatted_content)

    print("\nРезультат збережено у файл example.txt")

    # Читання очищеного вмісту з файлу example.txt
    with open('example.txt', 'r', encoding='utf-8') as file:
        clean_content = file.read()

    # Видобування хеш-тегів з тексту
    hashtags = extract_hashtags(clean_content)
    print("\nЗнайдені хеш-теги:", *hashtags, sep='\n')

    # Видобування IP-адрес з тексту
    ip_addresses = extract_ip_addresses(clean_content)
    print("\nЗнайдені IP-адреси:", *ip_addresses, sep='\n')

    # Перевірка на наявність рядків формату AB12CD34
    pattern_matches = find_pattern(clean_content)
    print("\nЗнайдені рядки формату AB12CD34:", *pattern_matches, sep='\n')
