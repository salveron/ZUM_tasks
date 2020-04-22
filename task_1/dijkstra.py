import heapq
import utils


def dijkstra(stdscr, matrix, coordinates, animated_flag):
    """This is a Dijkstra's algorithm implementation for a weighted graph.

    This algorithm works with a weighted graph, but changes the given matrix. The weighted graph is simply converted
    from the matrix, and all weights are equal to 1.0. This implementation does not degrade to the BFS algorithm in
    the same named module, because BFS there doesn't use a graph, where neighbors of a node aren't listed in the order
    used in the utils.MOVES dictionary, so the node expansion order is not the same here. This is well visible due
    to the animation of these two algorithms using testovaci_data/test_5.txt input file.

    :param stdscr: a curses screen to animate the process
    :param matrix: a matrix with a pattern to work with
    :param coordinates: start and end points
    :param animated_flag: a flag - do we want to animate the process or not
    :return: the changed matrix, the start and end points coordinates, a number of opened nodes and a length of path
    to be printed either to the terminal or written to the output file
    """
    start_node = coordinates[0]
    end_node = coordinates[1]
    matrix[start_node[1]][start_node[0]] = utils.START_NODE
    matrix[end_node[1]][end_node[0]] = utils.END_NODE

    graph = utils.matrix_to_weighted_graph(matrix)
    distances = {node: float('inf') for node in graph.keys()}
    priority_queue = [(0, start_node)]
    parents = {}
    visited_nodes = set()

    found = False
    distances[start_node] = 0.0

    while len(priority_queue) > 0:
        utils.refresh_screen(stdscr, matrix, animated_flag)

        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            found = True

        for neighbor, cost in graph[current_node].items():
            neighbor_distance = current_distance + cost

            if distances[neighbor] > neighbor_distance:
                distances[neighbor] = neighbor_distance
                if neighbor != start_node:
                    matrix[neighbor[1]][neighbor[0]] = utils.OPENED_NODE
                    visited_nodes.add(neighbor)
                heapq.heappush(priority_queue, (neighbor_distance, neighbor))
                parents[neighbor] = current_node

        if current_node not in [start_node, end_node]:
            matrix[current_node[1]][current_node[0]] = utils.CLOSED_NODE

        if found:
            break

    path = utils.reconstruct_path(start_node, end_node, parents)
    path_length = len(path)
    node_count = len(visited_nodes)

    for col, row in path[:-1]:
        matrix[row][col] = utils.PATH_NODE
    matrix[end_node[1]][end_node[0]] = utils.END_NODE

    utils.show_path(stdscr, path, animated_flag)
    utils.show_final_message(stdscr, matrix.shape[0], 0, animated_flag)

    return matrix, coordinates, node_count, path_length
