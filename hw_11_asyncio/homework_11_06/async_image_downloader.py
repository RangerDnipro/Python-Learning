"""
Модуль для одночасного завантаження зображень з декількох сайтів
"""

import os
import asyncio
import aiohttp


async def download_image(url: str, filename: str) -> None:
    """
    Завантажує зображення за заданим URL та зберігає його у файл
    :param url: URL зображення, яке необхідно завантажити
    :param filename: Ім'я файлу, у який зберігатиметься зображення
    :return: None
    """
    try:
        # Створюємо сесію aiohttp для виконання запиту
        async with aiohttp.ClientSession() as session:
            # Виконуємо GET запит для завантаження зображення
            async with session.get(url) as response:
                # Перевіряємо статус відповіді
                if response.status == 200:
                    # Зчитуємо дані зображення
                    image_data = await response.read()
                    # Створюємо папку, якщо її не існує
                    os.makedirs('uav_ua', exist_ok=True)
                    # Зберігаємо зображення у файл
                    filepath = os.path.join('uav_ua', filename)
                    with open(filepath, 'wb') as file:
                        file.write(image_data)
                    print(f"Зображення успішно завантажено та збережено у файл {filepath}")
                else:
                    print(f"Не вдалося завантажити зображення з {url}. Статус: {response.status}")
    except aiohttp.ClientError as e:
        # Обробка винятків, якщо щось пішло не так
        print(f"Помилка під час завантаження зображення з {url}: {e}")


async def main() -> None:
    """
    Головна асинхронна функція, що створює завдання для завантаження зображень одночасно
    :return: None
    """
    # Список URL-адрес зображень для завантаження разом з іменами файлів
    image_urls = [
        ("https://novynarnia.com/wp-content/uploads/2023/11/leleka-lr.jpg", "leleka.jpg"),
        ("https://athlonavia.com/wp-content/uploads/2020/05/furia4-1.jpg", "furia.jpg"),
        ("https://glavcom.ua/img/article/6020/46_main-v1560519785.jpg", "spectator.jpg"),
        ("https://kor.ill.in.ua/m/610x385/2781331.jpg", "shark.jpg"),
        ("https://tverezo.info/wp-content/uploads/2023/06/pap-valkirii-1_1.jpg", "valkyrja.jpg")
    ]

    # Створюємо список завдань для завантаження кожного зображення
    tasks = [download_image(url, filename) for url, filename in image_urls]
    # Виконуємо всі завдання одночасно
    await asyncio.gather(*tasks)


# Запуск програми
if __name__ == "__main__":
    asyncio.run(main())
