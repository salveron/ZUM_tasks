import sys

import bfs
import dfs
import random_search
import dijkstra
import greedy_search
import a_star
import utils

import curses


while True:
    animated_flag = None
    animate = input('Animate the process? [yes/no]: ')
    animate = animate.lower().strip()

    if animate == 'yes':
        animated_flag = True
    elif animate == 'no':
        animated_flag = False
    else:
        print('Try again.')
        continue
    break

while True:
    choice = input("Select an algorithm: ")
    choice = choice.lower().strip()

    if choice not in ['bfs', 'dfs', 'random', 'dijkstra', 'greedy', 'a-star']:
        print('Try again.')
        continue
    break

if animated_flag:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(False)
    curses.start_color()
    utils.initialize_colors()
else:
    stdscr = None

arguments = (stdscr, *utils.extract_all(sys.argv[1]), animated_flag)
result = choice

if choice == 'bfs':
    result = result, *bfs.bfs_iterative(*arguments)
elif choice == 'dfs':
    result = result, *dfs.dfs_iterative(*arguments)
elif choice == 'random':
    result = result, *random_search.random_search(*arguments)
elif choice == 'dijkstra':
    result = result, *dijkstra.dijkstra(*arguments)
elif choice == 'greedy':
    result = result, *greedy_search.greedy_search(*arguments)
elif choice == 'a-star':
    result = result, *a_star.a_star(*arguments)

if animated_flag:
    curses.curs_set(True)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

if animated_flag:
    utils.print_all_to_file('output.txt', *result)
else:
    utils.print_all_to_terminal(*result)
