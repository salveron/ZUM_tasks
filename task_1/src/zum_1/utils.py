import math
import os
import time

import curses
import numpy as np

MOVES = {'u': (0, -1), 'r': (1, 0), 'd': (0, 1), 'l': (-1, 0)}
INVERTED_MOVES = {'l': (-1, 0), 'd': (0, 1), 'r': (1, 0), 'u': (0, -1)}

FREE_NODE = ' '
OPENED_NODE = '.'
CLOSED_NODE = 'o'
START_NODE = 'S'
END_NODE = 'E'
WALL_NODE = '#'
PATH_NODE = 'p'

STANDARD_DELAY = 0.005
PATH_DELAY = 0.1

STRING_FOR_FORMATTED_OUTPUT = "--------------------------\n" + \
                              "Start: {}, end: {}\n" + \
                              "--------------------------\n" + \
                              "Start: '{}'\n" + \
                              "End: '{}'\n" + \
                              "Opened node: '{}'\n" + \
                              "Closed node: '{}'\n" + \
                              "Free node: '{}'\n" + \
                              "Wall: {}\n" + \
                              "Path: {}\n" + \
                              "--------------------------\n" + \
                              "Nodes expanded .. {}\n" + \
                              "Path length .. {}\n"


def print_all_to_terminal(*args):
    """Formats all arguments and prints them to the standard output.

    Arguments are (in order): algorithm name, adjacency matrix, start and end coordinates, number of opened nodes and
    path length.
    """
    for arr in args[1]:
        print(' '.join(arr))

    print(STRING_FOR_FORMATTED_OUTPUT.format(args[2][0], args[2][1],
                                             START_NODE, END_NODE, OPENED_NODE, CLOSED_NODE,
                                             FREE_NODE, WALL_NODE, PATH_NODE,
                                             args[3], args[4]))


def print_all_to_file(file_name, *args):  # FIXME
    """Formats all arguments and writes them to the file with a given name into the output directory.

    Arguments are (in order): algorithm name, adjacency matrix, start and end coordinates, number of opened nodes and
    path length.
    """
    f = open(os.path.join('output', file_name), 'w')
    f.write(args[0] + '\n')
    for line in args[1]:
        f.write(' '.join(line) + '\n')
    f.write(STRING_FOR_FORMATTED_OUTPUT.format(args[2][0], args[2][1],
                                               START_NODE, END_NODE, OPENED_NODE, CLOSED_NODE,
                                               FREE_NODE, WALL_NODE, PATH_NODE,
                                               args[3], args[4]))
    f.close()


def matrix_to_weighted_graph(matrix):
    """Converts a given adjacency matrix into weighted graph, where all edge weights are equal to 1.0.

    The graph is represented by the dict object, where keys are nodes and values are another dict objects,
    where keys are neighbor nodes and values are edge weights between them.
    """
    height, width = matrix.shape
    graph = {(col, row): {}
             for row in range(height)
             for col in range(width)
             if matrix[row][col] != WALL_NODE}
    for current_col, current_row in graph:
        for move_col, move_row in MOVES.values():
            next_col = current_col + move_col
            next_row = current_row + move_row
            if matrix[next_row][next_col] != WALL_NODE:
                distance = 1.0
                graph[(current_col, current_row)][(next_col, next_row)] = distance
                graph[(next_col, next_row)][(current_col, current_row)] = distance
    return graph


def build_heuristics(end_node, graph):
    """Builds heuristics for all nodes in the given graph.

    This function uses Euclidean heuristics and returns a dict object, where keys are nodes and values are
    Euclidean distances between them and the end node.
    """
    heuristics = {}
    for node in graph.keys():
        heuristics[node] = math.sqrt((node[0] - end_node[0]) ** 2 + (node[1] - end_node[1]) ** 2)
    return heuristics


def reconstruct_path(start, end, parents):
    """Reconstructs a path from the given start point to the end point.

    This function uses a dictionary of parent nodes to reconstruct a path from the end to the start. Then it returns a
    reversed copy of it. The final path doesn't contain the start node, and its length matches the number of steps to
    get from the start to the end.
    """
    if start == end:
        return []
    elif parents[end] == start:
        return [end]

    path = [end]
    while parents[end] != start:
        path.append(parents[end])
        end = parents[end]
    return path[::-1]


def extract_all(file_path):
    """Extracts an adjacency matrix and start and end points coordinates from the given file and returns them.

    The matrix is represented by a numpy two-dimensional array. The coordinates are returned as a tuple
    of start and end.
    """
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()

    start_line, end_line = lines[-2:]

    start_coords = __extract_coordinates(start_line)
    end_coords = __extract_coordinates(end_line)
    np_matrix = __extract_matrix(lines[:-2])

    return np_matrix, (start_coords, end_coords)


def initialize_colors():
    """Initializes the curses colors.

    Each color is represented by its unique integer identifier and a couple of curses color constants - foreground and
    background colors.
    """
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_RED)


def refresh_screen(scr, matrix, delay=STANDARD_DELAY):
    """Refreshes the given curses screen and delays it.

    Each matrix symbol is written at its special coordinates with its own color scheme. Then the screen is refreshed
    and delayed, so the user can see the pattern changes.
    """
    if scr is None:
        return

    scr.clear()
    for row_index, line in enumerate(matrix):
        for col_index, symbol in enumerate(line):
            try:
                if symbol == WALL_NODE:
                    scr.addstr(row_index, col_index * 2, symbol + ' ', curses.color_pair(1))
                elif symbol in [START_NODE, END_NODE]:
                    scr.addstr(row_index, col_index * 2, symbol + ' ', curses.color_pair(2))
                elif symbol == CLOSED_NODE:
                    scr.addstr(row_index, col_index * 2, symbol + ' ', curses.color_pair(3))
                elif symbol == OPENED_NODE:
                    scr.addstr(row_index, col_index * 2, symbol + ' ', curses.color_pair(4))
                else:
                    scr.addstr(row_index, col_index * 2, symbol + ' ', curses.color_pair(5))
            except curses.error:
                pass
    scr.refresh()
    time.sleep(delay)


def show_path(scr, path, delay=PATH_DELAY):
    """Shows the final path after the end point is found.

    Each path node is represented by PATH_NODE constant in adjacency matrix and printed with its special color scheme.
    After each node is printed, the screen is refreshed.
    """
    if scr is None or len(path) == 0:
        return

    end_col, end_row = path[-1]
    try:
        scr.addstr(end_row, end_col * 2, END_NODE + ' ', curses.color_pair(2))
    except curses.error:
        pass

    for col, row in path[:-1]:
        try:
            scr.addstr(row, col * 2, PATH_NODE + ' ', curses.color_pair(6))
        except curses.error:
            pass
        scr.refresh()
        time.sleep(delay)


def show_final_message(scr, x, y, message="Press any button to exit..."):
    """Shows the final message below the matrix after the animation is completed.

    The message is simply added to the screen, then the screen is refreshed. To exit animation mode, the used should
    press any button.
    """
    if scr is None:
        return
    try:
        scr.addstr(x, y, message)
    except curses.error:
        pass
    scr.refresh()
    scr.getch()


def __extract_matrix(lines):
    """Converts lines with encoded matrix into numpy array of special symbols."""
    np_matrix = np.asarray([list(line) for line in lines])
    np_matrix = np_matrix[:, :-1]
    np_matrix[np_matrix == 'X'] = WALL_NODE
    np_matrix[np_matrix == ' '] = FREE_NODE
    np_matrix[np_matrix == 'S'] = START_NODE
    np_matrix[np_matrix == 'E'] = END_NODE
    return np_matrix


def __extract_coordinates(line):
    """Parses a line with start or end coordinates and returns them."""
    arr = line.split()
    row, col = int(arr[1][:-1]), int(arr[2])
    return row, col
