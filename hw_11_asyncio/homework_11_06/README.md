# Завдання 6: Завантаження зображень з декількох сайтів

Уявімо, що ми розробляємо веб-скрапер, який має завантажити зображення з декількох сайтів одночасно. Кожне завантаження зображення - це окрема операція введення-виводу, яка може зайняти певний час.
Створити асинхронну функцію download_image, яка приймає URL зображення та ім'я файлу для збереження. Вона використовуватиме aiohttp для виконання HTTP-запиту та збереження отриманих даних у файл.
Головна асинхронна функція main створює список завдань (tasks), кожне з яких відповідає за завантаження одного зображення. Функція asyncio.gather дозволяє запускати всі завдання одночасно і очікувати їх завершення.