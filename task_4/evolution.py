from steps.simple_step import *
from steps.crowding_step import *
from individual import Individual


class Evolution:
    def __init__(self, population_size, simple, replacement):  # simple == True, crowding otherwise
        self.simple = simple
        self.replacement = replacement
        self.population = [Individual() for _ in range(population_size)]
        self.diversity = set(self.population)

        self.print_generation(0)

    @property
    def avg_fitness(self):
        return sum([individual.fitness for individual in self.population]) / len(self.population)

    def roulette_selection(self, how_many):
        selected = []
        overall_fitness = sum([i.fitness for i in self.population])
        chances = {i: i.fitness / overall_fitness for i in self.population}
        for _ in range(how_many):
            pick = random.uniform(0.0, 1.0)
            current = 0
            for individual, chance in chances.items():
                current += chance
                if current >= pick:
                    selected.append(individual)
                    break
        return selected

    def binary_tournament_selection(self, how_many):
        if len(self.population) == how_many:
            return self.population.copy()

        selected = []
        candidates = self.population.copy()
        for _ in range(how_many):
            candidate_1, candidate_2 = tuple(random.sample(candidates, 2))
            winner = candidate_1 if candidate_1.fitness >= candidate_2.fitness else candidate_2
            selected.append(winner)
            candidates.remove(winner)
        return selected

    def start(self, num_of_generations, parents_to_select, crossover_rate=.9, mutation_rate=.01):
        for i in range(num_of_generations):
            if self.simple:
                simple_step(self, parents_to_select, crossover_rate, mutation_rate)
            else:
                crowding_step(self, parents_to_select, crossover_rate, mutation_rate)

            self.diversity = set(self.population)
            self.print_generation(i + 1)

        self.print_ending()

    def print_generation(self, num_of_generation):
        print("\nGeneration:", num_of_generation, "size:", len(self.population))
        for individual in self.diversity:
            print(individual)
        print("Avg fitness:", self.avg_fitness)

    def print_ending(self):
        high_individuals = [i for i in self.population if i.fitness >= self.avg_fitness]
        print("\nEvolution completed.\nAverage fitness:", self.avg_fitness,
              "\nIndividuals that are better than the average",
              "(" + str(round(len(high_individuals) * 100 / len(self.population), 2)) + "%):")
        for i in set(high_individuals):
            optimal = len([j for j in self.population if i == j])
            print(optimal,
                  "out of",
                  len(self.population),
                  "(" + str(round(optimal * 100 / len(self.population), 2)) + "%)",
                  "individuals equal to this optimum: (",
                  i, ")")
