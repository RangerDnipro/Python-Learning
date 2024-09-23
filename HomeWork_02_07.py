"""
Завдання 7: Трекер витрат
Розробити програму для трекінгу витрат, яка використовує глобальні змінні для зберігання загальної суми витрат.
1.	Створити глобальну змінну total_expense і функцію add_expense, яка приймає суму витрат і додає її до загальної суми.
2.	Додати функцію get_expense, яка повертає загальну суму витрат.
3.	Створити інтерфейс (консольний), щоб користувач міг додавати витрати та переглядати загальну суму.
"""

# Глобальна змінна для зберігання загальної суми витрат
total_expense = 0


# Функція для додавання витрат
def add_expense(amount):
    """
    Додає витрати до загальної суми.

    Параметри:
    amount (float): Сума витрат, яку потрібно додати до загальної суми.

    Оновлює:
    total_expense (float): Оновлює глобальну змінну, додаючи нову витрату.
    """
    global total_expense
    total_expense += amount
    print(f"Додано витрату: {amount}. Загальна сума витрат: {total_expense}")


# Функція для отримання загальної суми витрат
def get_expense():
    """
    Повертає загальну суму витрат.

    Повертає:
    float: Загальна сума витрат, збережена в глобальній змінній total_expense.
    """
    return total_expense


# Консольний інтерфейс для користувача
def expense_tracker():
    """
    Консольний інтерфейс для трекера витрат.

    Користувач може вибрати одну з дій:
    1. Додати нову витрату.
    2. Переглянути загальну суму витрат.
    3. Вийти з програми.

    Функція працює в циклі до тих пір, поки користувач не вибере опцію "Вийти".
    """
    while True:
        print("\nВиберіть дію:")
        print("1. Додати витрату")
        print("2. Переглянути загальну суму витрат")
        print("3. Вийти")

        choice = input("Ваш вибір (1/2/3): ")

        if choice == '1':
            try:
                amount = float(input("Введіть суму витрат: "))
                add_expense(amount)
            except ValueError:
                print("Будь ласка, введіть коректну числову суму.")

        elif choice == '2':
            print(f"Загальна сума витрат: {get_expense()}")

        elif choice == '3':
            print("Дякуємо за користування трекером витрат!")
            break

        else:
            print("Невірний вибір, спробуйте ще раз.")


# Запуск трекера витрат
expense_tracker()
