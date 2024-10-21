"""
Модуль з реалізацією базової симуляції еволюції популяції, де кожен організм обробляється окремо
у паралельних процесах за допомогою модуля multiprocessing
"""

import random
import multiprocessing
from typing import List, Tuple


class Organism:
    """
    Клас, що представляє окремий організм у популяції
    """

    def __init__(self, energy: int, age: int = 0):
        """
        Ініціалізує організм з початковою кількістю енергії та віком
        :param energy: Початкова кількість енергії організму
        :param age: Вік організму (за замовчуванням 0)
        """
        self.energy = energy
        self.age = age
        # Максимальний вік, після якого організм помирає
        self.max_age = random.randint(3, 7)

    def feed(self):
        """
        Організм отримує їжу, що збільшує його енергію на випадкову величину
        """
        self.energy += random.randint(1, 20)

    def consume_energy(self):
        """
        Зменшує енергію організму на витрати для підтримки життєдіяльності
        """
        self.energy -= random.randint(1, 10)

    def reproduce(self) -> List['Organism']:
        """
        Створює нових організмів із певною часткою енергії батька
        :return: Список нових організмів
        """
        # Кількість потомків, що можуть народитися
        num_offspring = random.randint(1, 3)
        offspring = []
        for _ in range(num_offspring):
            child_energy = self.energy // (num_offspring + 1)
            offspring.append(Organism(child_energy))
        self.energy //= (num_offspring + 1)
        return offspring

    def is_alive(self) -> bool:
        """
        Перевіряє, чи живий організм (енергія повинна бути понад 0 і вік не більше максимального)
        :return: True, якщо організм живий, інакше False
        """
        return self.energy > 0 and self.age < self.max_age

    def age_one_year(self):
        """
        Збільшує вік організму на 1 рік
        """
        self.age += 1


def simulate_organism(organism: Organism) -> Tuple[bool, List[Organism]]:
    """
    Симулює життя окремого організму:
    харчування, споживання енергії, розмноження та перевірка на виживання
    :param organism: Організм, який буде симульовано
    :return: Кортеж, що містить статус виживання організму та список нових нащадків
    """
    # Організм харчується
    organism.feed()

    # Організм витрачає енергію на підтримку життєдіяльності
    organism.consume_energy()

    # Організм старіє
    organism.age_one_year()

    # Перевірка чи організм вижив
    if not organism.is_alive():
        return False, []

    # Якщо організм має достатньо енергії, він розмножується
    offspring = []
    if organism.energy > 15:
        offspring.extend(organism.reproduce())

    return organism.is_alive(), offspring


def simulate_population(population: List[Organism], generations: int) -> List[Organism]:
    """
    Симулює еволюцію популяції протягом заданої кількості поколінь
    :param population: Початкова популяція організмів
    :param generations: Кількість поколінь для симуляції
    :return: Кінцева популяція після заданої кількості поколінь
    """
    for generation in range(generations):
        initial_count = len(population)

        with multiprocessing.Pool() as pool:
            results = pool.map(simulate_organism, population)

        new_population = []
        born_count = 0
        dead_count = 0
        for organism_result in results:
            is_alive, offspring = organism_result
            if is_alive:
                # Додаємо актуальний організм після симуляції
                new_population.append(Organism(energy=is_alive,
                                               age=offspring[0].age if offspring else 0))
                new_population.extend(offspring)
                born_count += len(offspring)
            else:
                dead_count += 1

        population = new_population
        print(
            f"Покоління {generation + 1}, початкова кількість організмів: {initial_count}, "
            f"народилось: {born_count}, померло: {dead_count}")

    return population


if __name__ == "__main__":
    # Початкова кількість організмів у популяції
    INITIAL_POPULATION_SIZE = 10
    initial_population = [Organism(random.randint(5, 10)) for _ in range(INITIAL_POPULATION_SIZE)]

    # Кількість поколінь для симуляції
    NUM_GENERATIONS = 10

    # Симуляція еволюції популяції
    final_population = simulate_population(initial_population, NUM_GENERATIONS)

    print(f"Кінцева кількість організмів після {NUM_GENERATIONS} поколінь: {len(final_population)}")
