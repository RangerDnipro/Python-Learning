"""
Модуль містить моделі для взаємодії з базою даних.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Student(models.Model):
    """
    Модель для студентів.
    Поля:
    - name: Ім'я студента.
    - email: Електронна пошта студента.
    """
    name = models.CharField(max_length=100, verbose_name="Ім'я студента")
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")

    def __str__(self) -> str:
        """
        Повертає рядкове представлення студента.
        :return: Ім'я студента.
        """
        return self.name

    def enrolled_courses(self):
        """
        Отримати список курсів, на які записаний студент.
        :return: Список курсів.
        """
        return [enrollment.course for enrollment in self.enrollment_set.all()]


class Course(models.Model):
    """
    Модель для курсів.
    Поля:
    - title: Назва курсу.
    - description: Опис курсу.
    """
    title = models.CharField(max_length=150, verbose_name="Назва курсу")
    description = models.TextField(verbose_name="Опис курсу")

    def __str__(self) -> str:
        """
        Повертає рядкове представлення курсу.
        :return: Назва курсу.
        """
        return self.title

    def average_grade(self):
        """
        Підраховує середню оцінку за курсом.
        :return: Середня оцінка або None, якщо оцінок немає.
        """
        return self.grade_set.aggregate(Avg('grade'))['grade__avg']


class Enrollment(models.Model):
    """
    Модель для реєстрації студентів на курси.
    Поля:
    - student: Зв'язок зі студентом.
    - course: Зв'язок з курсом.
    - enrolled_on: Дата реєстрації.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_on = models.DateTimeField(auto_now_add=True, verbose_name="Дата реєстрації")

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Реєстрація"
        verbose_name_plural = "Реєстрації"

    def __str__(self) -> str:
        """
        Повертає рядкове представлення реєстрації.
        :return: Студент та курс.
        """
        return f"{self.student.name} -> {self.course.title}"


class Grade(models.Model):
    """
    Модель для оцінок студентів на курсах.
    Поля:
    - student: Зв'язок зі студентом.
    - course: Зв'язок з курсом.
    - grade: Оцінка (від 0 до 100).
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Оцінка"
    )

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"

    def __str__(self) -> str:
        """
        Повертає рядкове представлення оцінки.
        :return: Студент, курс та оцінка.
        """
        return f"{self.student.name} -> {self.course.title}: {self.grade}"
