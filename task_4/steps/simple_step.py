

def simple_step(evolution, parents_to_select, crossover_rate, mutation_rate):
    # Select parents for the crossover
    parents = evolution.binary_tournament_selection(int(len(evolution.population) * parents_to_select))

    # Choose a crossover method and get new individuals
    children = list(sum([parent_1.two_point_cross(parent_2, crossover_rate)
                         for parent_1, parent_2 in zip(parents[::2], parents[1::2])], ()))
    if len(parents) % 2 == 1:
        children.append(parents[-1])
    assert len(parents) == len(children)

    # Mutate new individuals
    children = [individual.mutate(mutation_rate) for individual in children]
    assert len(parents) == len(children)

    # Replace the weakest individuals with the new ones
    evolution.population = sorted(evolution.population, key=lambda x: x.fitness)
    evolution.population[:len(children)] = children
