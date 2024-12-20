"""
Модуль API для управління студентами, курсами та результатами.
"""

from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import django_auth

from management.models import Student, Course, Enrollment, Grade
from management.schemas import StudentSchema, CourseSchema, EnrollmentSchema, GradeSchema

# Створюємо маршрутизатор для всіх ендпоінтів
router = Router(auth=django_auth)
# Створюємо окремий роутер для користувачів
user_router = Router()


# Студенти
@router.post("/students", response={201: StudentSchema}, summary="Створити нового студента")
def create_student(request, name: str, email: str):
    """
    Створити нового студента.
    :param request: HTTP запит.
    :param name: Ім'я студента.
    :param email: Електронна пошта.
    :return: Створений студент.
    """
    student = Student.objects.create(name=name, email=email)
    return 201, student


@router.get("/students", response=list[StudentSchema], summary="Отримати список студентів")
def get_students(request):
    """
    Отримати список студентів.
    :param request: HTTP запит.
    :return: Список студентів.
    """
    return Student.objects.all()


@router.put("/students/{student_id}", response={200: StudentSchema}, summary="Оновити дані студента")
def update_student(request, student_id: int, name: str = None, email: str = None):
    """
    Оновити дані студента.
    :param request: HTTP запит.
    :param student_id: ID студента.
    :param name: Нове ім'я студента.
    :param email: Нова електронна пошта.
    :return: Оновлений студент.
    """
    student = get_object_or_404(Student, id=student_id)
    if name:
        student.name = name
    if email:
        student.email = email
    student.save()
    return 200, student


@router.delete("/students/{student_id}", response={204: None}, summary="Видалити студента")
def delete_student(request, student_id: int):
    """
    Видалити студента.
    :param request: HTTP запит.
    :param student_id: ID студента.
    :return: None.
    """
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return 204, None


# Курси
@router.post("/courses", response={201: CourseSchema}, summary="Створити новий курс")
def create_course(request, title: str, description: str = None):
    """
    Створити новий курс.
    :param request: HTTP запит.
    :param title: Назва курсу.
    :param description: Опис курсу.
    :return: Створений курс.
    """
    course = Course.objects.create(title=title, description=description)
    return 201, course


@router.get("/courses", response=list[CourseSchema], summary="Отримати список курсів")
def get_courses(request):
    """
    Отримати список курсів.
    :param request: HTTP запит.
    :return: Список курсів.
    """
    return Course.objects.all()


@router.put("/courses/{course_id}", response={200: CourseSchema}, summary="Оновити дані курсу")
def update_course(request, course_id: int, title: str = None, description: str = None):
    """
    Оновити дані курсу.
    :param request: HTTP запит.
    :param course_id: ID курсу.
    :param title: Нова назва курсу.
    :param description: Новий опис курсу.
    :return: Оновлений курс.
    """
    course = get_object_or_404(Course, id=course_id)
    if title:
        course.title = title
    if description:
        course.description = description
    course.save()
    return 200, course


@router.delete("/courses/{course_id}", response={204: None}, summary="Видалити курс")
def delete_course(request, course_id: int):
    """
    Видалити курс.
    :param request: HTTP запит.
    :param course_id: ID курсу.
    :return: None.
    """
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None


# Реєстрація студентів на курси
@router.post("/enroll", response={201: EnrollmentSchema, 200: EnrollmentSchema},
             summary="Зареєструвати студента на курс")
def enroll_student(request, student_id: int, course_id: int):
    """
    Зареєструвати студента на курс.
    :param request: HTTP запит.
    :param student_id: ID студента.
    :param course_id: ID курсу.
    :return: Реєстрація студента на курс.
    """

    # Перевірка, чи існують студент і курс
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    # Перевірка, чи вже існує така реєстрація
    enrollment = Enrollment.objects.filter(student=student, course=course).first()
    if enrollment:
        return 200, {
            "id": enrollment.id,
            "student_id": enrollment.student.id,
            "course_id": enrollment.course.id,
            "enrolled_on": enrollment.enrolled_on.isoformat(),
        }

    # Створення нової реєстрації
    enrollment = Enrollment.objects.create(
        student=student,
        course=course,
        enrolled_on=datetime.now()
    )

    return 201, {
        "id": enrollment.id,
        "student_id": enrollment.student.id,
        "course_id": enrollment.course.id,
        "enrolled_on": enrollment.enrolled_on.isoformat(),
    }


# Оцінки
@router.post("/grade", response={201: GradeSchema}, summary="Додати або оновити оцінку студента")
def grade_student(request, student_id: int, course_id: int, grade: float):
    """
    Додати або оновити оцінку студента.
    :param request: HTTP запит.
    :param student_id: ID студента.
    :param course_id: ID курсу.
    :param grade: Оцінка студента.
    :return: Оцінка студента.
    """
    grade_obj, created = Grade.objects.update_or_create(
        student_id=student_id, course_id=course_id, defaults={"grade": grade}
    )
    return 201, grade_obj


@router.get("/courses/{course_id}/average-grade", response=float, summary="Підрахувати середню оцінку за курсом")
def get_average_grade(request, course_id: int):
    """
    Підрахувати середню оцінку за курсом.
    :param request: HTTP запит.
    :param course_id: ID курсу.
    :return: Середня оцінка.
    """
    grades = Grade.objects.filter(course_id=course_id).values_list("grade", flat=True)
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


# Користувачі
@user_router.post("/register", summary="Реєстрація нового користувача")
def register_user(request, username: str, password: str):
    """
    Зареєструвати нового користувача.
    :param request: HTTP запит.
    :param username: Ім'я користувача.
    :param password: Пароль.
    :return: Повідомлення про успішну реєстрацію.
    """

    user = User.objects.create_user(username=username, password=password)
    return {"message": "Користувач успішно зареєстрований", "user_id": user.id, "username": user.username}


@user_router.get("/me", summary="Отримати дані поточного користувача")
def get_current_user(request):
    """
    Отримати дані поточного користувача.
    :param request: HTTP запит.
    :return: Дані користувача.
    """
    user = request.user
    if request.user.is_authenticated:
        return {"id": request.user.id, "username": request.user.username}
    return {"message": "User is not authenticated"}
