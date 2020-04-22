import heapq
import utils


def greedy_search(stdscr, matrix, coordinates, animated_flag):
    """This is a Greedy Search algorithm implementation for a weighted graph.

    This algorithm works with a weighted graph, but changes the given matrix. The weighted graph is simply converted
    from the matrix, and all weights are equal to 1.0. Heuristics is built by the utils.build_heuristics(...) function
    and then applied to get the priority of a node to be extended.

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
    heuristics = utils.build_heuristics(end_node, graph)
    priority_queue = [(heuristics[start_node], start_node)]
    closed_nodes = set()
    parents = {}

    found = False
    node_counter = 0

    while len(priority_queue) > 0:
        utils.refresh_screen(stdscr, matrix, animated_flag)

        _, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            found = True

        for neighbor in graph[current_node].keys():
            if (heuristics[neighbor], neighbor) not in priority_queue and neighbor not in closed_nodes:
                matrix[neighbor[1]][neighbor[0]] = utils.OPENED_NODE
                heapq.heappush(priority_queue, (heuristics[neighbor], neighbor))
                parents[neighbor] = current_node
                node_counter += 1

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

    utils.show_path(stdscr, path, animated_flag)
    utils.show_final_message(stdscr, matrix.shape[0], 0, animated_flag)

    return matrix, coordinates, node_counter, path_length
