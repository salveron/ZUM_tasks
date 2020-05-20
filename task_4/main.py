import sys
from collections import namedtuple

from evolution import *

Defaults = namedtuple("defaults", "pop_size num_of_gens, parents_percent, cross_rate, mutation_rate")
DEFAULT_VALUES = Defaults(pop_size=20, num_of_gens=100, parents_percent=.4, cross_rate=.9, mutation_rate=.05)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        flag = sys.argv[1]
        if flag in ["-s", "-cd", "-cp"]:
            if flag == "-s":
                simple = True
                replacement = None
            elif flag == "-cd":
                simple = False
                replacement = "d"
            elif flag == "-cp":
                simple = False
                replacement = "p"
        else:
            print("Usage: python3 main.py <-s/-c>")
            exit()
    else:
        print("Usage: python3 main.py <-s/-c>")
        exit()

    pop_size, num_of_gens, parents_percent, cross_rate, mutation_rate = DEFAULT_VALUES

    if len(sys.argv) == 8 and sys.argv[2] == "--handle":
        tmp_pop_size, tmp_num_of_gens, tmp_parents_percent, tmp_cross_rate, tmp_mutation_rate = tuple(sys.argv[3:8])

        try:
            pop_size = int(tmp_pop_size)
            num_of_gens = int(tmp_num_of_gens)
            parents_percent = float(tmp_parents_percent)
            cross_rate = float(tmp_cross_rate)
            mutation_rate = float(tmp_mutation_rate)

            if int(pop_size) <= 0 \
                    or int(num_of_gens) <= 0 \
                    or not 0.0 < float(parents_percent) <= 1.0 \
                    or not 0.0 <= float(cross_rate) <= 1.0 \
                    or not 0.0 <= float(mutation_rate) <= 1.0:
                raise ValueError
        except ValueError:
            print("Usage: python3 main.py <-s/-c> "
                  "[--handle <pop_size> <num_of_gens> <parents_percent> <cross_rate> <mutation_rate>]")
            exit()

    elif len(sys.argv) > 2:
        print("Usage: python3 main.py <-s/-c> "
              "[--handle <pop_size> <num_of_gens> <parents_percent> <cross_rate> <mutation_rate>]")
        exit()

    evolution = Evolution(pop_size, simple, replacement)
    evolution.start(num_of_gens, parents_percent, cross_rate, mutation_rate)
