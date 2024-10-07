class MessageSender:
    """
    Інтерфейс MessageSender для уніфікованої відправки повідомлень через різні канали
    :method send_message: Метод для відправки повідомлення
    :param message: Текст повідомлення, яке потрібно відправити
    """

    def send_message(self, message: str):
        pass
