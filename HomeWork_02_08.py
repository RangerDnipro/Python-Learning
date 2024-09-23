"""
Завдання 8: Зберігання налаштувань користувача
Реалізувати систему зберігання налаштувань користувача за допомогою замикань.
1.	Створити функцію create_user_settings, яка повертає функцію для зберігання та отримання налаштувань.
2.	Налаштування можуть включати такі параметри, як theme, language і notifications.
3.	Додати можливість зберігати, змінювати та переглядати налаштування.
"""

# Збережені налаштування користувача
settings = {'theme': 'dark', 'language': 'en', 'notifications': True}


# Функція для зберігання та отримання налаштувань
def create_user_settings():
    # Глобальний словник з параметрами
    global settings

    # Вкладена функція для виконання операції
    def manage_user_settings(action, key=None, value=None):
        if action == 'get':
            # Користувач хоче переглянути налаштування
            return settings
        elif action == 'set':
            # Користувач хоче змінити налаштування
            if key and value is not None:
                settings[key] = value
                return f"Налаштування '{key}' оновлено на {value}"
            else:
                return "Невірний ключ або значення"
        else:
            return "Невідома дія"

    return manage_user_settings


# Консольний інтерфейс для користувача
def user_settings_interface():
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
            key = {'2': ('theme', 'light/dark'), '3': ('language', 'en/ua'), '4': ('notifications', 'True/False')}[
                choice]
            value = input(f"Введіть нове значення для {key[0]}, наприклад {key[1]}: ")

            result = user_settings('set', key[0], value)
            print(result)

        elif choice == '5':
            break

        else:
            print("Невірний вибір, спробуйте ще раз.")
            continue


# Запуск інтерфейсу
user_settings_interface()
