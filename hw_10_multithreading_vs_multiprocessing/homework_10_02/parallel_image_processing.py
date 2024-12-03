"""
Модуль для паралельної обробки зображень, яке використовує бібліотеку Pillow для змінення розміру
зображень, а також модуль concurrent.futures для роботи з потоками та процесами
Розмір зображень змінюється за допомогою потоків,
а накладання фільтра виконується за допомогою процесів
"""

import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PIL import Image, ImageFilter


def resize_image(image_path: str, resized_path: str, size: tuple[int, int]) -> None:
    """
    Змінює розмір зображення та зберігає його в заданій директорії
    :param image_path: Шлях до оригінального зображення
    :param resized_path: Шлях для збереження зміненого зображення
    :param size: Новий розмір зображення (ширина, висота)
    :return: None
    """
    try:
        # Відкриваємо зображення
        with Image.open(image_path) as img:
            # Змінюємо розмір зображення
            img_resized = img.resize(size)
            # Зберігаємо змінене зображення в resized_path
            img_resized.save(resized_path)
            print(f"Зображення {image_path} успішно змінено та збережено в {resized_path}")
    except OSError as e:
        print(f"Помилка під час змінення розміру зображення {image_path}: {e}")


def apply_filter(image_path: str, output_path: str) -> None:
    """
    Застосовує фільтр до зображення та зберігає його в заданій директорії
    :param image_path: Шлях до зміненого зображення
    :param output_path: Шлях для збереження обробленого зображення
    :return: None
    """
    try:
        # Відкриваємо зображення
        with Image.open(image_path) as img:
            # Застосовуємо фільтр розмиття
            img_filtered = img.filter(ImageFilter.BLUR)
            # Зберігаємо оброблене зображення в output_path
            img_filtered.save(output_path)
            print(f"Зображення {image_path} успішно оброблено та збережено в {output_path}")
    except OSError as e:
        print(f"Помилка під час застосування фільтра до зображення {image_path}: {e}")


def process_images_concurrently(input_directory: str, output_directory: str,
                                size: tuple[int, int]) -> None:
    """
    Обробляє зображення паралельно, змінюючи їх розмір за допомогою потоків
    та застосовуючи фільтр за допомогою процесів
    :param input_directory: Директорія, де знаходяться зображення для обробки
    :param output_directory: Директорія для збереження оброблених зображень
    :param size: Новий розмір зображень (ширина, висота)
    :return: None
    """
    # Створюємо output_directory, якщо вона не існує
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Отримуємо список шляхів до всіх зображень в input_directory
    image_paths = [
        os.path.join(input_directory, f) for f in os.listdir(input_directory)
        if f.endswith(('.gif', '.jpg', '.jpeg', '.png', '.tiff', '.webp'))
    ]

    resized_paths = []

    # Виконуємо зміну розміру зображень за допомогою потоків
    with ThreadPoolExecutor() as executor:
        futures = []
        for image_path in image_paths:
            resized_path = os.path.join(output_directory,
                                        f"resized_{os.path.basename(image_path)}")
            resized_paths.append(resized_path)
            futures.append(executor.submit(resize_image, image_path, resized_path, size))

        # Очікуємо завершення всіх завдань зміни розміру
        for future in futures:
            future.result()

    # Виконуємо застосування фільтра за допомогою процесів
    with ProcessPoolExecutor() as executor:
        futures = []
        for resized_path in resized_paths:
            output_path = os.path.join(output_directory,
                                       f"filtered_{os.path.basename(resized_path)}")
            futures.append(executor.submit(apply_filter, resized_path, output_path))

        # Очікуємо завершення всіх завдань застосування фільтра
        for future in futures:
            future.result()


if __name__ == "__main__":
    # Директорія, де знаходяться зображення для обробки
    INPUT_DIR = "input_images"

    # Директорія для збереження оброблених зображень
    OUTPUT_DIR = "output_images"

    # Новий розмір зображень
    NEW_SIZE = (800, 600)

    # Виконуємо паралельну обробку зображень за допомогою потоків та процесів
    process_images_concurrently(INPUT_DIR, OUTPUT_DIR, NEW_SIZE)
