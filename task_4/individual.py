import random


class Individual:
    def __init__(self, genome=None):
        if genome is None:
            self.genome = [random.randint(0, 1) for _ in range(8)]
        else:
            self.genome = genome

    def __eq__(self, other):
        return self.genome == other.genome

    def __hash__(self):
        return hash(tuple(self.genome) + (self.fitness, ))

    def __str__(self):
        res = "Fitness: " + str(self.fitness) + ", [ "
        for i, gene in enumerate(self.genome):
            res += str(gene)
            if i == len(self.genome) // 2 - 1:
                res += " "
        return res + " ]"

    def __repr__(self):
        return self.__str__()

    @property
    def fitness(self):
        if self.genome.count(1) == 8:  # 1111 1111
            return 22
        elif self.genome.count(0) == 8:  # 0000 0000
            return 20
        elif self.genome[:4] == [1, 1, 1, 1] or self.genome[4:] == [1, 1, 1, 1]:  # 1111 **** or **** 1111
            return 11
        elif self.genome[:4] == [0, 0, 0, 0] or self.genome[4:] == [0, 0, 0, 0]:  # 0000 **** or **** 0000
            return 10
        else:
            return 1

    def mutate(self, rate):
        new_genome = []
        for gene in self.genome:
            assert gene in [0, 1]

            if random.uniform(0.0, 1.0) <= rate:
                new_genome.append(0 if gene == 1 else 1)
            else:
                new_genome.append(gene)
        return Individual(genome=new_genome)

    def one_point_cross(self, other, rate):
        if random.uniform(0.0, 1.0) > rate:  # Crossover will not occur
            return Individual(genome=self.genome), Individual(genome=other.genome)

        # Crossover occurs
        cross_point = random.randint(0, len(self.genome) - 1)
        parent_1 = self.genome.copy()
        parent_2 = other.genome.copy()
        offspring_1 = parent_1[:cross_point] + parent_2[cross_point:]
        offspring_2 = parent_2[:cross_point] + parent_1[cross_point:]
        return Individual(genome=offspring_1), Individual(genome=offspring_2)

    def two_point_cross(self, other, rate):
        if random.uniform(0.0, 1.0) > rate:  # Crossover will not occur
            return Individual(genome=self.genome), Individual(genome=other.genome)

        # Crossover occurs
        cross_point_1 = random.randint(0, len(self.genome) - 2)
        cross_point_2 = random.randint(cross_point_1, len(self.genome) - 1)
        parent_1 = self.genome.copy()
        parent_2 = other.genome.copy()
        offspring_1 = parent_1[:cross_point_1] + parent_2[cross_point_1:cross_point_2] + parent_1[cross_point_2:]
        offspring_2 = parent_2[:cross_point_1] + parent_1[cross_point_1:cross_point_2] + parent_2[cross_point_2:]
        return Individual(genome=offspring_1), Individual(genome=offspring_2)
