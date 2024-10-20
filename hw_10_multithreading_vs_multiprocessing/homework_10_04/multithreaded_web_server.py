"""
Простий веб-сервер, який може одночасно обслуговувати декілька клієнтів у багатопотоковому режимі
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import requests


# pylint: disable=invalid-name
class SimpleRequestHandler(BaseHTTPRequestHandler):
    """
    Обробник запитів для простого веб-сервера
    """

    # Метод do_GET не відповідає стилю іменування snake_case, бо це вимога стандарту бібліотеки
    def do_GET(self) -> None:
        """
        Обробляє GET-запит від клієнта та відправляє текстову відповідь
        """
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        response_text = "Привіт, клієнт! Це відповідь від простого веб-сервера"
        self.wfile.write(response_text.encode('utf-8'))


class SimpleWebServer:
    """
    Простий багатопотоковий веб-сервер, який обслуговує кілька клієнтів одночасно,
    використовуючи HTTPServer
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Ініціалізує сервер з вказаними хостом і портом
        :param host: Адреса хоста для прослуховування
        :param port: Порт для прослуховування запитів
        """
        self.server = HTTPServer((host, port), SimpleRequestHandler)
        self.host = host
        self.port = port
        print(f"Сервер запущено на {self.host}:{self.port}")

    def start(self) -> None:
        """
        Запускає сервер для приймання з'єднань від клієнтів у багатопотоковому режимі
        """
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Сервер працює у фоновому потоці.")
        try:
            # Запуск клієнтських запитів
            self.send_multiple_requests()
            server_thread.join()
        except KeyboardInterrupt:
            print("\nСервер зупиняється...")
            self.server.shutdown()
            self.server.server_close()

    def send_multiple_requests(self) -> None:
        """
        Відправляє кілька одночасних запитів до сервера для демонстрації багатопотоковості
        """

        def send_request():
            try:
                response = requests.get(f"http://{self.host}:{self.port}", timeout=5)
                print(response.text)
            except requests.exceptions.RequestException as e:
                print(f"Помилка: {e}")

        threads = []
        for _ in range(5):  # Створюємо 5 потоків для одночасних запитів
            thread = threading.Thread(target=send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Після успішного відпрацювання запитів зупиняємо сервер
        print("Всі запити були оброблені. Зупинка сервера...")
        self.server.shutdown()
        self.server.server_close()


if __name__ == "__main__":
    # Ініціалізуємо сервер на локальному хості та порту 8080
    server = SimpleWebServer(host="127.0.0.1", port=8080)
    server.start()
