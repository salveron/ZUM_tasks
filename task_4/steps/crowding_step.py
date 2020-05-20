import itertools
import random


def crowding_step(evolution, parents_to_select, crossover_rate, mutation_rate):
    random.shuffle(evolution.population)

    # Select parents for the crossover
    parents = evolution.roulette_selection(int(len(evolution.population) * parents_to_select))

    # Choose a crossover method and get new individuals
    children = list(sum([parent_1.one_point_cross(parent_2, crossover_rate)
                        for parent_1, parent_2 in zip(parents[::2], parents[1::2])], ()))
    if len(parents) % 2 == 1:
        children.append(parents[-1])
    assert len(parents) == len(children)

    # Mutate new individuals
    children = [individual.mutate(mutation_rate) for individual in children]
    assert len(parents) == len(children)

    # Compute distances between parents and children - n * n matrix
    distances = {p: {c: compute_distance(p, c) for c in children} for p in parents}

    # Compute the best matching of parents and children, where the sum of distances between them is minimal
    best_matching = compute_best_matching(parents, children, distances)

    # Get new population
    new_population = [deterministic_replacement(p, c) if evolution.replacement == "d"
                 else probabilistic_replacement(p, c)
                      for p, c in best_matching]
    assert len(parents) == len(children) == len(new_population)

    # Replace the weakest individuals with the new ones
    evolution.population = sorted(evolution.population, key=lambda x: x.fitness)
    evolution.population[:len(new_population)] = new_population


def compute_distance(parent, child):
    return len([None for pg, cg in zip(parent.genome, child.genome) if pg != cg])


def compute_best_matching(parents, children, distances):
    # n! complexity -> not recommended to use when selected parents > 8
    # optimal: (pop=12 & pts=.7) or (pop=20 & pts=.4)
    assert len(parents) == len(children)

    permutations = itertools.permutations(children)
    matchings = {}
    for permutation in permutations:
        matching = list(zip(parents, permutation))
        matchings[sum([distances[p][c] for p, c in matching])] = matching

    return matchings[min(matchings.keys())]


def deterministic_replacement(parent, child):
    if parent.fitness > child.fitness:
        return parent
    elif parent.fitness == child.fitness:
        return parent if random.choice([True, False]) else child
    else:
        return child


def probabilistic_replacement(parent, child):
    fit_sum = parent.fitness + child.fitness
    if random.uniform(0.0, 1.0) <= (parent.fitness / fit_sum):
        return parent
    else:
        return child
