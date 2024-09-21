"""
Завдання 5: Календар подій
Розробити простий календар подій.
1.	Використовуючи замикання, створити функції для додавання подій, видалення подій та перегляду майбутніх подій.
2.	Зберігати події у списку за допомогою глобальної змінної.
"""


# Функція для створення календаря подій
def event_calendar():
    # Локальна змінна для зберігання подій
    events = []

    # Функція для додавання події
    def add_event(event):
        events.append(event)
        print(f"Подію '{event}' додано до календаря")

    # Функція для видалення події
    def remove_event(event):
        if event in events:
            events.remove(event)
            print(f"Подію '{event}' видалено з календаря")
        else:
            print(f"Подія '{event}' не знайдена")

    # Функція для перегляду всіх подій
    def view_events():
        if events:
            print("Майбутні події:")
            for i, event in enumerate(events, start=1):
                print(f"{i}. {event}")
        else:
            print("Немає майбутніх подій")

    # Повертаємо функції у вигляді замикань
    return add_event, remove_event, view_events


# Створюємо календар подій
add_event, remove_event, view_events = event_calendar()

# Приклад використання
add_event("День народження")
add_event("Конференція")
add_event("Дедлайн")
# Перегляд подій
view_events()
remove_event("Конференція")
# Перегляд подій після видалення
view_events()
