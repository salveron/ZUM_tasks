from collections import deque

from zum_1 import utils


def dfs_iterative(stdscr, matrix, coordinates):
    """This is an iterative Depth-First Search algorithm implementation for an adjacency matrix.

    This algorithm doesn't convert a matrix into graph. It uses utils.MOVES dictionary to get all four possible
    directions of steps and then checks if the next node is valid to move to it.

    :param stdscr: a curses screen to animate the process
    :param matrix: a matrix with a pattern to work with
    :param coordinates: start and end points
    :return: the changed matrix, the start and end points coordinates, a number of opened nodes and a length of path
    to be printed either to the terminal or written to the output file
    """
    start_node = coordinates[0]
    end_node = coordinates[1]
    matrix[start_node[1]][start_node[0]] = utils.START_NODE
    matrix[end_node[1]][end_node[0]] = utils.END_NODE

    node_counter = 0
    found = False
    q = deque()
    p = {}
    q.append(start_node)

    while q:
        utils.refresh_screen(stdscr, matrix)

        current_node = q.pop()

        if current_node == end_node:
            found = True

        for move_col, move_row in utils.INVERTED_MOVES.values():
            next_col = current_node[0] + move_col
            next_row = current_node[1] + move_row

            if next_col < 0 or next_col > matrix.shape[1] - 1 \
            or next_row < 0 or next_row > matrix.shape[0] - 1:
                continue
            elif matrix[next_row][next_col] in [utils.FREE_NODE, utils.END_NODE]:
                matrix[next_row][next_col] = utils.OPENED_NODE
                q.append((next_col, next_row))
                p[(next_col, next_row)] = current_node
                node_counter += 1

        if current_node not in [start_node, end_node]:
            matrix[current_node[1]][current_node[0]] = utils.CLOSED_NODE

        if found:
            break

    path = utils.reconstruct_path(start_node, end_node, p)
    path_length = len(path)

    for col, row in path[:-1]:
        matrix[row][col] = utils.PATH_NODE
    matrix[end_node[1]][end_node[0]] = utils.END_NODE

    utils.show_path(stdscr, path)
    utils.show_final_message(stdscr, matrix.shape[0], 0)

    return matrix, coordinates, node_counter, path_length
