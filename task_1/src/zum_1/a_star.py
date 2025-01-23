import heapq

from zum_1 import utils


def a_star(stdscr, matrix, coordinates):
    """This is an A* (A-star) algorithm implementation for a weighted graph.

    This algorithm works with a weighted graph, but changes the given matrix. The weighted graph is simply converted
    from the matrix, and all weights are equal to 1.0. Heuristics is built by the utils.build_heuristics(...) function
    and then applied along with the neighbor distance to get the priority of a node to be extended.

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

    graph = utils.matrix_to_weighted_graph(matrix)
    distances = {node: float('inf') for node in graph.keys()}
    heuristics = utils.build_heuristics(end_node, graph)
    priority_queue = [(0.0, 0.0, start_node)]
    opened_nodes = set()
    closed_nodes = set()
    parents = {}

    found = False
    node_counter = 0
    distances[start_node] = 0.0
    opened_nodes.add(start_node)

    while len(priority_queue) > 0:
        utils.refresh_screen(stdscr, matrix)

        _, current_distance, current_node = heapq.heappop(priority_queue)
        opened_nodes.discard(current_node)

        if current_node == end_node:
            found = True

        for neighbor, cost in graph[current_node].items():
            if neighbor in closed_nodes:
                continue

            neighbor_distance = current_distance + cost
            neighbor_heuristics = heuristics[neighbor]
            neighbor_priority = neighbor_distance + neighbor_heuristics

            if neighbor in opened_nodes:
                if distances[neighbor] > neighbor_distance:
                    distances[neighbor] = neighbor_distance
            else:
                if neighbor != start_node:
                    matrix[neighbor[1]][neighbor[0]] = utils.OPENED_NODE
                heapq.heappush(priority_queue, (neighbor_priority, neighbor_distance, neighbor))
                opened_nodes.add(neighbor)
                node_counter += 1

            parents[neighbor] = current_node

        closed_nodes.add(current_node)
        if current_node not in [start_node, end_node]:
            matrix[current_node[1]][current_node[0]] = utils.CLOSED_NODE

        if found:
            break

    path = utils.reconstruct_path(start_node, end_node, parents)
    path_length = len(path)

    for col, row in path[:-1]:
        matrix[row][col] = utils.PATH_NODE
    matrix[end_node[1]][end_node[0]] = utils.END_NODE

    utils.show_path(stdscr, path)
    utils.show_final_message(stdscr, matrix.shape[0], 0)

    return matrix, coordinates, node_counter, path_length
