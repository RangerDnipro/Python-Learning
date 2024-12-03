"""
Завдання 6. Приклад комплексного тестування
Розробіть програму для роботи з банківськими транзакціями та протестуйте її за допомогою
фікстур, моків, скіпів та параметризації. Напишіть клас BankAccount, який реалізує методи:
deposit(amount: float): поповнення рахунку;
withdraw(amount: float): зняття коштів (якщо достатньо коштів на рахунку).
get_balance() -> float: повертає поточний баланс.
Напишіть тести з використанням:
фікстур для створення об'єкта банківського рахунку перед тестами,
моків для тестування взаємодії із зовнішнім API (наприклад, для перевірки балансу),
скіпів для пропуску тестів зняття коштів, якщо рахунок порожній.
Використовуйте параметризацію для тестування різних сценаріїв поповнення та зняття коштів.
"""

# pylint: disable=redefined-outer-name

from unittest.mock import Mock
import pytest


class BankAccount:
    """
    Клас, що представляє банківський рахунок
    """

    def __init__(self, initial_balance: float = 0.0):
        """
        Ініціалізує об'єкт банківського рахунку
        :param initial_balance: Початковий баланс рахунку, за замовчуванням 0.0
        """
        self.balance = initial_balance

    def deposit(self, amount: float) -> None:
        """
        Поповнення рахунку
        :param amount: Сума для поповнення (повинна бути додатною)
        """
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Сума для поповнення повинна бути додатною")

    def withdraw(self, amount: float) -> None:
        """
        Зняття коштів з рахунку
        :param amount: Сума для зняття (повинна бути додатною і не перевищувати баланс)
        """
        if amount <= 0:
            raise ValueError("Сума для зняття повинна бути додатною")
        if amount > self.balance:
            raise ValueError("Недостатньо коштів на рахунку")
        self.balance -= amount

    def get_balance(self) -> float:
        """
        Повертає поточний баланс рахунку
        :return: Поточний баланс
        """
        return self.balance


# Тести для класу BankAccount
@pytest.fixture
def bank_account():
    """
    Фікстура для створення об'єкта банківського рахунку перед тестами
    :return: Об'єкт BankAccount з початковим балансом 100.0
    """
    return BankAccount(100.0)


def test_deposit(bank_account):
    """
    Тест для методу поповнення рахунку
    """
    bank_account.deposit(50.0)
    assert bank_account.get_balance() == 150.0


def test_withdraw(bank_account):
    """
    Тест для методу зняття коштів з рахунку
    """
    bank_account.withdraw(30.0)
    assert bank_account.get_balance() == 70.0


@pytest.mark.skip(reason="Рахунок порожній, пропускаємо тест зняття коштів")
def test_withdraw_empty_account():
    """
    Тест для методу зняття коштів з порожнього рахунку (пропускається)
    """
    empty_account = BankAccount()
    empty_account.withdraw(10.0)


def test_get_balance_with_mock():
    """
    Тест для методу отримання балансу з використанням мока
    """
    mock_account = Mock(spec=BankAccount)
    mock_account.get_balance.return_value = 200.0
    assert mock_account.get_balance() == 200.0


@pytest.mark.parametrize("deposit_amount, withdraw_amount, expected_balance", [
    (100.0, 50.0, 150.0),
    (200.0, 100.0, 200.0),
    (50.0, 25.0, 125.0)
])
def test_deposit_withdraw(bank_account, deposit_amount, withdraw_amount, expected_balance):
    """
    Тест для різних сценаріїв поповнення та зняття коштів з використанням параметризації
    :param deposit_amount: Сума для поповнення
    :param withdraw_amount: Сума для зняття
    :param expected_balance: Очікуваний баланс після операцій
    """
    bank_account.deposit(deposit_amount)
    bank_account.withdraw(withdraw_amount)
    assert bank_account.get_balance() == expected_balance
