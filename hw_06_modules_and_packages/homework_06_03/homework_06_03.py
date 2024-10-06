"""
Завдання 3: Робота з CSV файлами
Створи CSV-файл з даними про студентів, де кожен рядок містить:
Ім'я, Вік, Оцінка
Петро,21,90
Марина,22,85
Андрій,20,88
Напиши програму, яка:
Читає дані з CSV-файлу.
Виводить середню оцінку студентів.
Додає нового студента до файлу.
"""

import os
import csv


def create_students_file(filename):
    """
    Створюємо файл зі студентами, якщо він не існує
    :param filename: Ім'я файлу, який буде створюватися
    """
    if not os.path.exists(filename):
        students_data = [
            ["Ім'я", "Вік", "Оцінка"],
            ["Петро", 21, 90],
            ["Марина", 22, 85],
            ["Андрій", 20, 88]
        ]
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(students_data)
        print(f"CSV-файл '{filename}' створено.")
    else:
        print(f"CSV-файл '{filename}' вже існує.")


def read_students(filename):
    """
    Читаємо дані з CSV-файлу та повертає список студентів
    :param filename: Ім'я файлу, який буде зчитуватися
    :return: Список студентів у вигляді словників, де ключами є 'name', 'age', 'grade'
    """
    students = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Пропускаємо заголовок
        next(reader)
        for row in reader:
            students.append({
                "name": row[0],
                "age": int(row[1]),
                "grade": int(row[2])
            })
    return students


def calculate_average_grade(students):
    """
    Обчислюємо середню оцінку студентів
    :param students: Список студентів, де кожен студент - словник з ключами 'name', 'age', 'grade'
    :return: Середня оцінка студентів
    """
    total_grade = sum(student["grade"] for student in students)
    average_grade = total_grade / len(students) if students else 0
    return average_grade


def add_student(filename, name, age, grade):
    """
    Додаємо нового студента до CSV-файлу
    :param filename: Ім'я файлу, куди буде додано студента
    :param name: Ім'я студента
    :param age: Вік студента
    :param grade: Оцінка студента
    """

    # Зчитуємо наявних студентів
    students = read_students(filename)

    # Перевіряємо, чи існує студент з таким ім'ям
    if any(student["name"] == name for student in students):
        print(f"Студент з іменем {name} вже існує. Додавання пропущено")
        return

    # Якщо студента не існує, додаємо його
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, grade])
    print(f"Студента {name} додано.")


# Використання функцій, створюємо файл даних
filename = 'homework_06_03.csv'
create_students_file(filename)

# Читаємо дані з файлу
students = read_students(filename)

# Обчислюємо середню оцінку
average = calculate_average_grade(students)
print(f"Середня оцінка студентів: {average:.2f}")

# Додаємо нового студента
add_student(filename, "Олег", 23, 92)
