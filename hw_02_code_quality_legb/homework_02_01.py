"""
Завдання 1: Built-in область видимості
(демонстрація використання вбудованих функцій та їх перекриття локальними функціями).
1.	Написати функцію my_sum, яка перекриває вбудовану функцію sum. Функція повинна просто виводити повідомлення:
"This is my custom sum function!".
2.	Створити список чисел і викликати вбудовану функцію sum, щоб підсумувати значення списку.
3.	Викликати свою функцію my_sum, а потім ще раз спробувати скористатися вбудованою функцією sum.
Питання для закріплення:
•	Що відбувається, коли локальна функція має те саме ім'я, що й вбудована?
•	Як можна отримати доступ до вбудованої функції, навіть якщо вона перекрита?
"""


# Створюємо функцію my_sum, яка перекриває вбудовану функцію sum
def my_sum():
    """
    Функція, яка перекриває вбудовану функцію sum.

    Ця функція виводить повідомлення та перекриває вбудовану функцію sum в локальній області видимості.
    Після виклику, вбудована функція sum стає недоступною до моменту явного виклику через модуль builtins.
    """
    global sum
    sum = my_sum
    print("This is my custom sum function!")


# Створюємо список чисел і викликаємо вбудовану функцію sum, щоб підсумувати значення списку
numbers = [4, 8, 15, 16, 23, 42]
print("Сума списка чисел:", sum(numbers))

# Викликаємо свою функцію my_sum
my_sum()

# Ще раз спробуємо скористатися вбудованою функцією sum
try:
    print("Сума списка чисел:", sum(numbers))
except TypeError:
    print("Вбудована функція sum наразі перекрита")

"""
Відповіді на питання для закріплення:
1. Що відбувається, коли локальна функція має те саме ім'я, що й вбудована?
- Коли локальна функція має те саме ім'я, що й вбудована, в межах області видимості локальної функції вона перекриває 
вбудовану функцію. Це означає, що при виклику імені функції виконується локальна версія, а не вбудована.
2. Як отримати доступ до вбудованої функції, навіть якщо вона перекрита?
- Можна отримати доступ до вбудованої функції за допомогою модуля builtins, де зберігаються всі вбудовані функції. 
"""

# Отримання доступа до вбудованої функції та підсумування значення списку
import builtins

print("Сума списка чисел перекритою функцією sum:", builtins.sum(numbers))