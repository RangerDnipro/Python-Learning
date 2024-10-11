"""
Завдання 8. Тестування з використанням doctest та покриття складних сценаріїв (опціонально)
Додайте документацію з прикладами використання більш складних функцій,
які включають роботу з матрицями. Реалізуйте функції для роботи з матрицями:
matrix_multiply(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[List[int]]:
множення двох матриць.
transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
транспонування матриці.
Додайте doctest для кожної функції
Переконайтеся, що приклади коректно працюють і додайте складніші тестові випадки до документації.
Запустіть тести із doctest для перевірки правильності роботи функцій з матрицями.
"""

from typing import List


def matrix_multiply(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[List[int]]:
    """
    Множить дві матриці
    :param matrix1: Перша матриця у вигляді списку списків цілих чисел
    :param matrix2: Друга матриця у вигляді списку списків цілих чисел
    :return: Результат множення двох матриць у вигляді списку списків цілих чисел

    >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]

    >>> matrix_multiply([[1, 0], [0, 1]], [[1, 2], [3, 4]])
    [[1, 2], [3, 4]]

    >>> matrix_multiply([[2, 3, 4]], [[1], [2], [3]])
    [[20]]
    """
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Число стовпців першої матриці повинно дорівнювати числу рядків другої")

    result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*matrix2)] for row in matrix1]
    return result


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Транспонує матрицю
    :param matrix: Матриця у вигляді списку списків цілих чисел
    :return: Транспонована матриця у вигляді списку списків цілих чисел

    >>> transpose_matrix([[1, 2], [3, 4]])
    [[1, 3], [2, 4]]

    >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]

    >>> transpose_matrix([[1]])
    [[1]]
    """
    return list(map(list, zip(*matrix)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
