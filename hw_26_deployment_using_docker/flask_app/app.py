"""
Модуль містить основний Flask-застосунок.
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home() -> str:
    """
    Відображає головну сторінку з повідомленням.
    :return: Вітальний текст.
    """
    return "Flask in Docker is working!"

if __name__ == "__main__":
    app.run(debug=True)
