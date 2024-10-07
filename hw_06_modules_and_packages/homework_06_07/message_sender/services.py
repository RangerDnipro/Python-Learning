class SMSService:
    """
    Клас SMSService для відправки SMS повідомлень
    :method send_sms: Відправляє SMS на заданий номер
    :param phone_number: Номер телефону для відправки повідомлення
    :param message: Текст повідомлення для відправки
    """

    def send_sms(self, phone_number: str, message: str):
        print(f"Відправка SMS на {phone_number}: {message}")


class EmailService:
    """
    Клас EmailService для відправки Email повідомлень
    :method send_email: Відправляє Email на задану адресу
    :param email_address: Електронна адреса отримувача
    :param message: Текст повідомлення для відправки
    """

    def send_email(self, email_address: str, message: str):
        print(f"Відправка Email на {email_address}: {message}")


class PushService:
    """
    Клас PushService для відправки push-повідомлень
    :method send_push: Відправляє push-повідомлення на пристрій з певним ID
    :param device_id: Ідентифікатор пристрою для відправки повідомлення
    :param message: Текст повідомлення для відправки
    """

    def send_push(self, device_id: str, message: str):
        print(f"Відправка Push-повідомлення на пристрій {device_id}: {message}")
