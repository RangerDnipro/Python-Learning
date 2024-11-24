import pytest
from datetime import date, timedelta
from testing.forms import TaskForm


@pytest.mark.django_db
class TestTaskForm:
    """
    Тестування форми TaskForm.
    """

    def test_form_valid(self):
        """
        Тест валідності форми з правильними даними.
        """
        form_data = {
            "title": "Завдання 1",
            "description": "Опис завдання",
            "due_date": date.today() + timedelta(days=1),
        }
        form = TaskForm(data=form_data)
        assert form.is_valid()

    def test_form_invalid_missing_fields(self):
        """
        Тест на помилки, якщо обов'язкові поля відсутні.
        """
        form = TaskForm(data={})
        assert not form.is_valid()
        assert "title" in form.errors
        assert "due_date" in form.errors

    def test_form_invalid_due_date(self):
        """
        Тест на перевірку дати у минулому.
        """
        form_data = {
            "title": "Завдання 2",
            "description": "Опис завдання",
            "due_date": date.today() - timedelta(days=1),
        }
        form = TaskForm(data=form_data)
        assert not form.is_valid()
        assert "due_date" in form.errors
