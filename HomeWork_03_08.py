"""
8. Price class discussion before the PaymentGateway implementation
1.	Реалізуйте клас Price, що представляє ціну товару з можливістю заокруглення до двох десяткових знаків.
Додайте методи для додавання, віднімання та порівняння цін.
2.	Поміркуйте, як клас Price може бути використаний в майбутньому класі PaymentGateway для обробки фінансових транзакцій.
"""


class Price:
    def __init__(self, amount):
        """
        Ініціалізує об'єкт Price з вказаною сумою
        :param amount: сума ціни з заокругленням до двох десяткових знаків
        """
        self.amount = round(amount, 2)

    def __add__(self, new_amount):
        """
        Додає до ціни суму new_amount
        :param new_amount: деяка сума яку треба додати
        """
        self.amount += round(new_amount, 2)

    def __sub__(self, new_amount):
        """
        Віднімає від ціни суму new_amount
        :param new_amount: деяка сума яку треба відняти
        """
        if self.amount < round(new_amount, 2):
            raise ValueError("Існуюча ціна менша за суму що треба відняти")
        self.amount -= round(new_amount, 2)

    def __lt__(self, other):
        """
        Порівнює дві ціни. Повертає True, якщо поточна ціна менша за іншу
        :param other: інший об'єкт Price
        :return: bool
        """
        return self.amount < other.amount

    def __eq__(self, other):
        """
        Перевіряє, чи рівні дві ціни
        :param other: інший об'єкт Price
        :return: bool
        """
        return self.amount == other.amount

    def __repr__(self):
        """
        Повертає рядкове представлення ціни.
        :return: рядок у форматі Ціна: amount
        """
        return f"Ціна: {self.amount:.2f}"


# Тестування, вводимо ціну товару
p1 = Price(10.505)
print(p1, end='\n\n')
# Додаємо деяку суму
p1.__add__(5.868)
print(p1)
# Віднімаємо деяку суму
p1.__sub__(4.656)
print(p1, end='\n\n')
# Створюємо нову ціну та порівнюємо з попередньою
p2 = Price(11.585)
print(p2, end='\n\n')
if p1 == p2:
    print("Ціни ідентичні")
elif p1 < p2:
    print(f"{p1} менша ніж {p2}")
else:
    print(f"{p1} більша ніж {p2}")
