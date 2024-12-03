"""
Завдання 4: Таймер для тренування

Розробити програму, яка симулює таймер для тренувань із вбудованою функцією,
що дозволяє змінювати час тренування на кожному кроці.
1.	Створити глобальну змінну default_time = 60, яка задає стандартний час на кожне тренування (у хвилинах).
2.	Створити функцію training_session, яка:
-	приймає кількість раундів тренування.
-	використовує змінну time_per_round, що відповідає за час на раунд, і локально змінює її для кожного тренування.
-	в середині функції створити вкладену функцію adjust_time, яка дозволяє налаштовувати час для кожного окремого раунду
(через неявне використання nonlocal).
3.	Програма повинна виводити тривалість кожного раунду тренування.

Приклад використання:

training_session(3)
# Результат:
# Раунд 1: 60 хвилин
# Раунд 2: 55 хвилин (після коригування часу)
# Раунд 3: 50 хвилин (після коригування часу)
"""

# Глобальна змінна для стандартного часу на тренування
default_time = 60


# Функція для тренувальної сесії
def training_session(rounds):
    """
    Виконує тренувальну сесію, де кожен раунд може мати налаштований час.

    Параметри:
    rounds (int): Кількість раундів тренування.

    Вкладена функція:
    adjust_time(adjustment): Коригує час для кожного раунду через зміну значення time_per_round.

    Приклад використання:
    training_session(3)
    # Раунд 1: 60 хвилин
    # Раунд 2: 55 хвилин (після коригування часу)
    # Раунд 3: 50 хвилин (після коригування часу)
    """
    # Локальна змінна для часу на раунд (список з одним елементом)
    time_per_round = [default_time]

    # Вкладена функція для налаштування часу на кожен раунд через неявне використання nonlocal
    def adjust_time(adjustment):
        """
        Коригує час для поточного раунду.

        Параметри:
        adjustment (int): Значення, на яке змінюється час для поточного раунду.
        """
        # Коригування часу для раунду
        time_per_round[0] += adjustment

    # Проходимо через кожен раунд і коригуємо час та, якщо не перший раунд, додаємо припис
    suffix = ''
    for i in range(1, rounds + 1):
        print(f"Раунд {i}: {time_per_round[0]} хвилин{suffix}")

        # Коригуємо час (наприклад, на -5 хвилин), додаємо припис
        adjust_time(-5)
        suffix = ' (після коригування часу)'


# Приклад використання
training_session(3)
