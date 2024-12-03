"""
Додаткове завдання 2. Уяви, що ти розробляєш систему для відправки повідомлень різними каналами:
через SMS, Email та Push-повідомлення. Усі ці канали мають різні інтерфейси для відправки повідомлень,
але ти хочеш уніфікувати їх, щоб використовувати один універсальний інтерфейс для відправки повідомлень
незалежно від каналу.

Базова структура:
Створи інтерфейс MessageSender, який визначає метод для відправки повідомлення

Існуючі класи:
Є три класи, кожен з яких реалізує власний метод для відправки повідомлень:
- SMSService: має метод send_sms(phone_number, message).
- EmailService: має метод send_email(email_address, message).
- PushService: має метод send_push(device_id, message).
Створи ці класи з відповідними методами для відправки повідомлень.

Створення адаптерів:
Для кожного з класів (SMSService, EmailService, PushService) створи окремі адаптери, які будуть реалізовувати
інтерфейс MessageSender. Адаптери мають використовувати відповідні методи існуючих класів для відправки повідомлень:
- SMSAdapter: адаптує SMSService для використання через інтерфейс MessageSender.
- EmailAdapter: адаптує EmailService.
- PushAdapter: адаптує PushService.

Використання:
Напиши код, який створює екземпляри адаптерів для кожного типу сервісу (SMS, Email, Push) та відправляє повідомлення
за допомогою універсального інтерфейсу MessageSender

Додатково (опціонально):
Реалізуй систему відправки повідомлень, яка приймає список адаптерів і відправляє одне і те ж повідомлення
через усі доступні сервіси.
Додай обробку помилок для кожного сервісу, якщо відправка повідомлення не вдалася.

*************************************************************************************************************

Для реалізації завдання створимо Python-проєкт з такою структурою:

homework_06_07/
│
├── main.py                     # демонстрація використання
├── message_sender/
│   ├── __init__.py             # файл ініціалізації пакета message_sender
│   ├── adapters.py             # адаптери для кожного сервісу
│   ├── services.py             # сервіси для відправки повідомлень
│   ├── interfaces.py           # інтерфейс MessageSender
│   └── message_dispatcher.py   # логіка для відправки повідомлень через всі сервіси та обробка помилок
"""

from message_sender import SMSAdapter, EmailAdapter, PushAdapter
from message_sender import SMSService, EmailService, PushService
from message_sender import MessageDispatcher


def main():
    """
    Основна функція програми для відправки повідомлень через різні сервіси
    Створює екземпляри сервісів SMS, Email, Push і адаптерів для них
    Відправляє одне і те ж повідомлення через всі сервіси
    """

    # Створення сервісів для відправки повідомлень
    sms_service = SMSService()
    email_service = EmailService()
    push_service = PushService()

    # Створення адаптерів для сервісів
    sms_adapter = SMSAdapter(sms_service, "+380123456789")
    email_adapter = EmailAdapter(email_service, "user@example.com")
    push_adapter = PushAdapter(push_service, "device123")

    # Список адаптерів
    adapters = [sms_adapter, email_adapter, push_adapter]

    # Створення екземпляру MessageDispatcher
    dispatcher = MessageDispatcher(adapters)

    # Текст повідомлення для відправки через різні сервіси
    message = "Привіт! Це тестове повідомлення."

    # Відправка повідомлення через всі адаптери
    dispatcher.send_message_to_all(message)


if __name__ == "__main__":
    """
    Точка входу в програму
    Викликає основну функцію main(), яка ініціалізує сервіси та відправляє повідомлення
    """
    main()
