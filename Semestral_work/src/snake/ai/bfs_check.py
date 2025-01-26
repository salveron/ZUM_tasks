from collections import deque

import numpy as np

from snake.utils import *


def bfs_check(snake, new_head):
    # Returns the count of the reachable free nodes if the snake moves to the new_head tile

    adjacency_matrix = np.zeros((AI_WINDOW_SQUARES_WIDTH, AI_WINDOW_SQUARES_HEIGHT))

    for tile in snake.tiles:
        adjacency_matrix[tile.y][tile.x] = 1

    q = deque([new_head.pos])
    reachable_nodes_count = 0

    while q:
        current_node = q.popleft()

        # if the node is already closed -> continue
        if adjacency_matrix[current_node[1]][current_node[0]] == -1:
            continue

        reachable_nodes_count += 1

        # add all the free neighbor nodes to the queue
        for move_col, move_row in DIRECTIONS.values():
            next_col = current_node[0] + move_col
            next_row = current_node[1] + move_row

            if next_col < 0 or next_col >= AI_WINDOW_SQUARES_WIDTH \
            or next_row < 0 or next_row >= AI_WINDOW_SQUARES_HEIGHT:
                continue
            elif adjacency_matrix[next_row][next_col] == 0:
                q.append((next_col, next_row))

        # mark the node as closed
        adjacency_matrix[current_node[1]][current_node[0]] = -1

    return reachable_nodes_count
