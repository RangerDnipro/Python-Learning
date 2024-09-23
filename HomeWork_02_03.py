"""
Завдання 3: Магазин замовлень з акційними знижками
Написати програму, яка імітує систему замовлення з акціями, де знижки зберігаються у глобальній області,
а нарахування знижки відбувається локально для кожного клієнта.
1.	Створити глобальну змінну discount = 0.1 (10% знижка).
2.	Створити функцію create_order, яка приймає ціну товару як аргумент і всередині:
-	обчислює кінцеву ціну з урахуванням знижки, що визначена глобальною.
-	створює вкладену функцію apply_additional_discount, яка додає додаткову знижку (наприклад, для VIP-клієнтів)
і змінює фінальну ціну.
3.	Використати ключове слово nonlocal, щоб функція могла змінювати кінцеву ціну у вкладеній області видимості.
4.	Після застосування всіх знижок вивести фінальну ціну.

Приклад використання:
create_order(1000) # Початкова ціна: 1000, кінцева ціна зі знижкою 10%: 900
"""

# Глобальна змінна для стандартної знижки 10%
discount = 0.1
# Додаткова знижка для VIP 5%
vip_discount = 0.05

# Функція для створення замовлення
def create_order(price, vip=False):
    """
    Створює замовлення і обчислює кінцеву ціну з урахуванням знижок.

    Параметри:
    price (float): Початкова ціна товару.
    vip (bool, опціонально): Якщо True, застосовується додаткова знижка для VIP-клієнтів (стандартно False).

    Вкладена функція:
    apply_vip_discount(): Додає додаткову знижку для VIP-клієнтів і змінює фінальну ціну.

    Приклад використання:
    create_order(1000)  # Звичайний клієнт
    create_order(1000, True)  # VIP-клієнт
    """
    # Розраховуємо стандартну знижку
    final_price = price * (1 - discount)

    # Вкладена функція для застосування додаткової знижки
    def apply_vip_discount():
        """
        Застосовує додаткову VIP-знижку до ціни, змінюючи значення final_price.

        Повертає:
        float: Нову фінальну ціну після додаткової знижки.
        float: Загальний відсоток знижки (стандартна + VIP).
        """
        # Використовуємо ключове слово nonlocal
        nonlocal final_price
        # Розраховуємо додаткову знижку
        final_price = price * (1 - (vip_discount + discount))
        return final_price, vip_discount + discount

    if not vip:
        # Виводимо кінцеву ціну після застосування стандартної знижки
        print(f"Початкова ціна: {price}, кінцева ціна зі знижкою {round(discount * 100)}%: {final_price}")
    else:
        # Викликаємо функцію для додаткової знижки
        final_price, new_discount = apply_vip_discount()
        # Виводимо кінцеву ціну після застосування всіх знижок
        print(f"Початкова ціна: {price}, кінцева ціна для VIP зі знижкою {round(new_discount * 100)}% : {final_price}")


# Приклад використання для звичайного клієнта
create_order(1000)
# Приклад використання для VIP клієнта
create_order(1000, True)
