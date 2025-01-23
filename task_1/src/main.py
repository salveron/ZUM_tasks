import sys

from zum_1 import bfs
from zum_1 import dfs
from zum_1 import random_search
from zum_1 import dijkstra
from zum_1 import greedy_search
from zum_1 import a_star
from zum_1 import utils

import curses


def choose_algorithm() -> str:
    while True:
        choice = input("Select an algorithm. Valid options: [\"bfs\", \"dfs\", \"random\", "
                       "\"dijkstra\", \"greedy\", \"a-star\"]: ").lower().strip()

        if choice not in ["bfs", "dfs", "random", "dijkstra", "greedy", "a-star"]:
            print("Try again.")
            continue

        return choice


def main(stdscr, algorithm, *args, **kwargs):

    if stdscr is not None:
        curses.curs_set(False)
        curses.start_color()
        utils.initialize_colors()
    else:
        stdscr = None

    arguments = (stdscr, *utils.extract_all(sys.argv[1]))
    result = algorithm, *({
        "bfs": bfs.bfs_iterative,
        "dfs": dfs.dfs_iterative,
        "random": random_search.random_search,
        "dijkstra": dijkstra.dijkstra,
        "greedy": greedy_search.greedy_search,
        "a-star": a_star.a_star,
    }[algorithm](*arguments))

    if stdscr is not None:
        curses.curs_set(True)
        # FIXME: utils.print_all_to_file("output.txt", *result)

    return result


if __name__ == "__main__":

    while True:
        animate = input("Animate the process? [yes/no]: ").lower().strip()

        if animate == "yes":
            result = curses.wrapper(main, choose_algorithm())
        elif animate == "no":
            result = main(None, choose_algorithm())
        else:
            print("Try again.")
            continue
        break

    utils.print_all_to_terminal(*result)
