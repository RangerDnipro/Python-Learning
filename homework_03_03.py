"""
Завдання 3. to-Compare
1.	Реалізуйте клас Person із параметрами name та age. Додайте методи для порівняння за віком (__lt__, __eq__, __gt__).
2.	Напишіть програму для сортування списку об'єктів класу Person за віком.
"""


class Person:
    def __init__(self, name: str, age: int):
        """
        Ініціалізація об'єкта класу Person
        :param name: Ім'я людини
        :param age: Вік людини
        """
        self.name = name
        self.age = age

    def __lt__(self, other):
        """
        Перевіряє, чи є вік поточного об'єкта меншим за вік іншого
        :param other: Інший об'єкт Person
        :return: True, якщо вік поточного об'єкта менший, False — якщо ні
        """
        return self.age < other.age

    def __eq__(self, other):
        """
        Перевіряє, чи є вік поточного об'єкта рівним віку іншого
        :param other: Інший об'єкт Person
        :return: True, якщо вік рівний, False — якщо ні
        """
        return self.age == other.age

    def __gt__(self, other):
        """
        Перевіряє, чи є вік поточного об'єкта більшим за вік іншого
        :param other: Інший об'єкт Person
        :return: True, якщо вік поточного об'єкта більший, False — якщо ні
        """
        return self.age > other.age

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта Person у форматі "name: age"
        :return: рядок
        """
        return f"{self.name}: {self.age}"


# Тестування функцій
print(Person("Anya", 30) < Person("Dmytro", 25))
print(Person("Anya", 30) == Person("Dmytro", 25))
print(Person("Anya", 30) > Person("Dmytro", 25), end='\n\n')

# Тестування з сортуванням
if __name__ == "__main__":
    people = [
        Person("Anya", 30),
        Person("Dmytro", 25),
        Person("Natalia", 35),
        Person("Petro", 28)
    ]

    # Сортування за віком
    sorted_people = sorted(people)

    # Перевірка правильності сортування
    expected = ["Dmytro: 25", "Petro: 28", "Anya: 30", "Natalia: 35"]
    result = [repr(person) for person in sorted_people]
    assert result == expected, f"Expected {expected}, got {result}"

    # Виведення відсортованого списку
    for person in sorted_people:
        print(person)
