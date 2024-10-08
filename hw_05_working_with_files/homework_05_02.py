"""
Завдання 2. Ітератор для генерації унікальних ідентифікаторів
Створіть ітератор, який генерує унікальні ідентифікатори (наприклад, на основі UUID або хеш-функції).
Ідентифікатори повинні генеруватися один за одним при кожній ітерації, і бути унікальними.
"""

import uuid


class UniqueIDIterator:
    """
    Ітератор для генерації унікальних ідентифікаторів на основі UUID
    """

    def __init__(self):
        """
        Ініціалізація ітератора. Налаштування для генерації UUID
        """
        pass

    def __iter__(self):
        """
        Повертає сам ітератор
        """
        return self

    def __next__(self):
        """
        Генерує та повертає новий унікальний ідентифікатор при кожній ітерації
        :return: Унікальний ідентифікатор у вигляді рядка
        """
        return str(uuid.uuid4())


# Використання ітератора для генерації унікальних ідентифікаторів
id_iterator = UniqueIDIterator()
# Згенеруємо 5 унікальних ідентифікаторів
for _ in range(5):
    print(next(id_iterator))
