from ai.snake_individual import *


class Evolution:
    def __init__(self, game_snake, game_fruit, pop_size=POPULATION_SIZE):
        self.game_snake = game_snake
        self.game_fruit = game_fruit

        self.population = sorted([SnakeIndividual(self.game_snake, self.game_fruit) for _ in range(pop_size)],
                                 key=lambda x: x.fitness)

    @property
    def avg_fitness(self):
        return sum([individual.fitness for individual in self.population]) / len(self.population)

    def selection(self, how_many):  # Roulette selection
        selected = []
        overall_fitness = sum([i.fitness for i in self.population])
        chances = {i: (i.fitness / overall_fitness if overall_fitness > 0.0 else 1.0 / len(self.population))
                   for i in self.population}
        for _ in range(how_many):
            pick = random.uniform(0.0, 1.0)
            current = 0
            for individual, chance in chances.items():
                current += chance
                if current >= pick:
                    selected.append(individual)
                    break
        return selected

    def start(self, num_of_gens=NUMBER_OF_GENERATIONS, par_percent=PARENTS_PERCENT,
              cross_rate=CROSSOVER_RATE, mut_rate=MUTATION_RATE):
        best_individual = None

        for i in range(num_of_gens):
            # Select parents for the crossover
            parents = self.selection(int(len(self.population) * par_percent))

            # Cross them to get the new ones
            children = list(sum([parent_1.cross(parent_2, cross_rate)
                                 for parent_1, parent_2 in zip(parents[::2], parents[1::2])], ()))
            if len(parents) % 2 == 1:
                children.append(parents[-1])
            assert len(parents) == len(children)

            # Mutate new individuals
            children = [individual.mutate(mut_rate) for individual in children]
            assert len(parents) == len(children)

            # Replace the weakest individuals with the new ones
            self.population[:len(children)] = children
            self.population = sorted(self.population, key=lambda x: x.fitness)

            # Return the best individual
            best_individual = self.population[-1]

        print(f"Best: ", best_individual, f", {nn_inputs_type(*best_individual.get_nn_inputs())}", sep="")
        return best_individual
