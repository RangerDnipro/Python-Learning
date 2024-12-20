"""
Модуль зі схемами додатка
"""

from typing import Optional

from ninja import Schema
from pydantic import Field


class StudentSchema(Schema):
    """
    Схема для відображення студента.
    """
    id: int
    name: str
    email: str


class StudentInSchema(Schema):
    """
    Схема для створення/оновлення студента.
    """
    name: str
    email: str


class CourseSchema(Schema):
    """
    Схема для відображення курсу.
    """
    id: int
    title: str
    description: Optional[str] = None


class CourseInSchema(Schema):
    """
    Схема для створення/оновлення курсу.
    """
    title: str
    description: Optional[str] = None


class EnrollmentSchema(Schema):
    """
    Схема для реєстрації студента на курс.
    """
    id: int
    student_id: int
    course_id: int
    enrolled_on: str = Field(..., description="Дата реєстрації студента на курс у форматі ISO 8601")


class GradeSchema(Schema):
    """
    Схема для відображення оцінки студента за курс.
    """
    id: int
    student_id: int
    course_id: int
    grade: float
