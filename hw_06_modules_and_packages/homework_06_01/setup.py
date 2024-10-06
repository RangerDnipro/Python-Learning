from setuptools import setup, find_packages

setup(
    # Назва пакета
    name="my_package",
    # Версія пакета
    version="0.1",
    # Автоматичне знаходження всіх підпакетів у директорії
    packages=find_packages(),
    # Залежності, якщо такі є
    install_requires=[],
    # Автор
    author="Данило Кочешвілі",
    # Email автора
    author_email="danil@ukr.net",
    # Короткий опис пакета
    description="Python пакет для математичних та рядкових утиліт",
    # Довгий опис із файлу README.md
    long_description=open("README.md").read(),
    # Формат README
    long_description_content_type="text/markdown",
    # URL на репозиторій
    url="https://github.com/RangerDnipro/Python-Learning",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Вимога до версії Python
    python_requires='>=3.6',
)
