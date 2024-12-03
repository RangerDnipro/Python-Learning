"""
Завдання 8: Зберігання налаштувань користувача
Реалізувати систему зберігання налаштувань користувача за допомогою замикань.
1.	Створити функцію create_user_settings, яка повертає функцію для зберігання та отримання налаштувань.
2.	Налаштування можуть включати такі параметри, як theme, language і notifications.
3.	Додати можливість зберігати, змінювати та переглядати налаштування.
"""

# Глобальний словник із налаштуваннями
settings = {'theme': 'dark', 'language': 'en', 'notifications': True}


# Функція для зберігання та отримання налаштувань
def create_user_settings():
    """
    Функція створює замикання для управління налаштуваннями користувача.

    Повертає:
    function: Вкладена функція manage_user_settings для зберігання та отримання налаштувань.
    """
    global settings

    # Вкладена функція для виконання операції
    def manage_user_settings(action, key=None, value=None):
        """
        Функція для управління налаштуваннями (отримання, зміна).

        Параметри:
        action (str): Дія, яку потрібно виконати ('get' або 'set').
        key (str): Ключ налаштування, яке потрібно змінити (для 'set').
        value (str/None): Нове значення для ключа (для 'set').

        Повертає:
        str: Результат дії або помилка.
        """
        if action == 'get':
            # Користувач хоче переглянути налаштування
            return settings
        elif action == 'set':
            # Користувач хоче змінити конкретне налаштування
            if key and value is not None:
                if key == 'notifications':
                    # Якщо було введено 'true' тоді вибираємо булеве True інакше False
                    value = value.lower() == 'true'
                settings[key] = value
                return f"Налаштування '{key}' оновлено на {value}"
            else:
                return "Невірний ключ або значення"
        else:
            return "Невідома дія"

    return manage_user_settings


# Консольний інтерфейс для користувача
def user_settings_interface():
    """
    Консольний інтерфейс для керування налаштуваннями користувача.

    Дозволяє користувачеві переглядати та змінювати такі налаштування:
    - Тема (theme)
    - Мова (language)
    - Сповіщення (notifications)
    """
    # Налаштування користувача
    user_settings = create_user_settings()

    while True:
        print("\nВиберіть дію:")
        print("1. Переглянути поточні налаштування")
        print("2. Змінити тему в налаштуваннях")
        print("3. Змінити мову в налаштуваннях")
        print("4. Змінити режим сповіщень в налаштуваннях")
        print("5. Вийти")

        choice = input("Ваш вибір (1/2/3/4/5): ")

        if choice == '1':
            # Перегляд усіх налаштувань
            all_settings = user_settings('get')
            for key, value in all_settings.items():
                print(f"{key}: {value}")

        elif choice in ('2', '3', '4'):
            # Зміна відповідного налаштування
            key = {'2': ('theme', 'light/dark або інша'), '3': ('language', 'en/ua або інша'),
                   '4': ('notifications', 'True/true, якщо буде введено щось інше - сповіщення буде вимкнено')}[
                choice]
            value = input(f"Введіть нове значення для {key[0]}, наприклад {key[1]}: ")

            result = user_settings('set', key[0], value)
            print(result)

        elif choice == '5':
            print("Вихід.")
            break

        else:
            print("Невірний вибір, спробуйте ще раз.")


# Запуск інтерфейсу
user_settings_interface()
