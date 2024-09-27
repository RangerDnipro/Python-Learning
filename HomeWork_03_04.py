"""
Завдання 4. Binary
1.	Реалізуйте клас BinaryNumber, який представляє двійкове число.
Додайте методи для виконання двійкових операцій: AND (__and__), OR (__or__), XOR (__xor__) та NOT (__invert__).
2.	Напишіть тест для цих операцій.
"""


class BinaryNumber:
    def __init__(self, binary_string):
        """
        Ініціалізація об'єкта класу BinaryNumber.
        :param binary_string: Двійкове число у вигляді рядка.
        """
        if not all(c in '01' for c in binary_string):
            raise ValueError("Рядок має містити лише 0 та 1")
        self.binary_string = binary_string

    def binary_operation(self, other, operation):
        """
        Виконує бінарну операцію над двома двійковими числами.
        :param other: Інший об'єкт BinaryNumber.
        :param operation: Функція, що виконує бінарну операцію (наприклад, lambda b1, b2: b1 & b2).
        :return: Новий об'єкт BinaryNumber.
        """
        max_len = max(len(self.binary_string), len(other.binary_string))
        self_padded = self.binary_string.zfill(max_len)
        other_padded = other.binary_string.zfill(max_len)
        result = ""
        for b1, b2 in zip(self_padded, other_padded):
            result += str(operation(int(b1), int(b2)))
        return BinaryNumber(result)

    def __and__(self, other):
        """
        Операція AND
        :param other: Інший об'єкт BinaryNumber.
        :return: Новий об'єкт BinaryNumber.
        """
        return self.binary_operation(other, lambda b1, b2: b1 & b2)

    def __or__(self, other):
        """
        Операція OR
        :param other: Інший об'єкт BinaryNumber.
        :return: Новий об'єкт BinaryNumber.
        """
        return self.binary_operation(other, lambda b1, b2: b1 | b2)

    def __xor__(self, other):
        """
        Операція XOR
        :param other: Інший об'єкт BinaryNumber.
        :return: Новий об'єкт BinaryNumber.
        """
        return self.binary_operation(other, lambda b1, b2: b1 ^ b2)

    def __invert__(self):
        """
        Операція NOT
        :return: Новий об'єкт BinaryNumber.
        """
        result = ""
        for symbol in self.binary_string:
            result += str(int(not int(symbol)))
        return BinaryNumber(result)

    def __repr__(self):
        """
        Повертає рядкове представлення двійкового числа у вигляді "BinaryNumber(value)"
        :return: рядок
        """
        return f"BinaryNumber('{self.binary_string}')"

    def to_decimal(self):
        """
        Перетворення двійкового числа в десяткове
        :return: Десяткове число.
        """
        return int(self.binary_string, 2)


# Тестування операцій
a = BinaryNumber('1101')
print(f"Двійкове число {a} означає в десятинній системі {a.to_decimal()}")
b = BinaryNumber('1010')
print(f"Двійкове число {b} означає в десятинній системі {b.to_decimal()}")

c = a & b
print(f"Двійкове число {c} означає в десятинній системі {c.to_decimal()}")
c = a | b
print(f"Двійкове число {c} означає в десятинній системі {c.to_decimal()}")
c = a ^ b
print(f"Двійкове число {c} означає в десятинній системі {c.to_decimal()}")
c = ~a
print(f"Двійкове число {c} означає в десятинній системі {c.to_decimal()}")
