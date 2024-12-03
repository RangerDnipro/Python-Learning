from .interfaces import MessageSender


class MessageDispatcher:
    """
    Клас MessageDispatcher для відправки повідомлень через список адаптерів
    :method send_message_to_all: Відправляє повідомлення через усі адаптери в списку
    :param adapters: Список адаптерів, які реалізують інтерфейс MessageSender
    :param message: Текст повідомлення для відправки через всі сервіси
    """

    def __init__(self, adapters: list[MessageSender]):
        """
        Конструктор класу MessageDispatcher
        :param adapters: Список об'єктів, які реалізують інтерфейс MessageSender
        """
        self.adapters = adapters

    def send_message_to_all(self, message: str):
        """
        Відправляє повідомлення через усі сервіси, обробляючи можливі помилки
        :param message: Текст повідомлення, яке потрібно відправити через всі сервіси
        """
        for adapter in self.adapters:
            try:
                adapter.send_message(message)
                print(f"Повідомлення успішно відправлено через {adapter.__class__.__name__}")
            except Exception as e:
                # Обробка помилки: виведення на консоль або запис в лог
                print(f"Помилка при відправці через {adapter.__class__.__name__}: {e}")
