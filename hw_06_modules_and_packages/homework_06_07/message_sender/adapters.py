from .interfaces import MessageSender
from .services import SMSService, EmailService, PushService


class SMSAdapter(MessageSender):
    """
    Адаптер для використання SMSService через інтерфейс MessageSender
    :method send_message: Використовує SMSService для відправки повідомлення
    :param message: Текст повідомлення для відправки
    """

    def __init__(self, sms_service: SMSService, phone_number: str):
        """
        Конструктор класу SMSAdapter
        :param sms_service: Екземпляр класу SMSService для відправки SMS
        :param phone_number: Номер телефону для відправки повідомлення
        """

        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str):
        """
        Використовує SMSService для відправки повідомлення
        :param message: Текст повідомлення для відправки
        """

        self.sms_service.send_sms(self.phone_number, message)


class EmailAdapter(MessageSender):
    """
    Адаптер для використання EmailService через інтерфейс MessageSender
    :method send_message: Використовує EmailService для відправки повідомлення
    :param message: Текст повідомлення для відправки
    """

    def __init__(self, email_service: EmailService, email_address: str):
        """
        Конструктор класу EmailAdapter
        :param email_service: Екземпляр класу EmailService для відправки email
        :param email_address: Адреса електронної пошти для відправки повідомлення
        """

        self.email_service = email_service
        self.email_address = email_address

    def send_message(self, message: str):
        """
        Використовує EmailService для відправки повідомлення
        :param message: Текст повідомлення для відправки
        """

        self.email_service.send_email(self.email_address, message)


class PushAdapter(MessageSender):
    """
    Адаптер для використання PushService через інтерфейс MessageSender
    :method send_message: Використовує PushService для відправки повідомлення
    :param message: Текст повідомлення для відправки
    """

    def __init__(self, push_service: PushService, device_id: str):
        """
        Конструктор класу PushAdapter
        :param push_service: Екземпляр класу PushService для відправки push-повідомлення
        :param device_id: Ідентифікатор пристрою для відправки повідомлення
        """

        self.push_service = push_service
        self.device_id = device_id

    def send_message(self, message: str):
        """
        Використовує PushService для відправки повідомлення
        :param message: Текст повідомлення для відправки
        """

        self.push_service.send_push(self.device_id, message)
