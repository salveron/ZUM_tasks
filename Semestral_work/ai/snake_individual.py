import math

from snake import *
from ai.neural_network import *
from ai.bfs_check import bfs_check


class SnakeIndividual:
    def __init__(self, snake, fruit, nn=None):
        if nn is None:
            self.nn = NeuralNetwork()
        else:
            self.nn = nn

        self.snake = snake
        self.fruit = fruit
        self.fitness = self.calculate_fitness()

    def __str__(self):
        return f"[fitness: {self.fitness}]"

    def __repr__(self):
        return self.__str__()

    def mutate(self, rate):
        return SnakeIndividual(self.snake, self.fruit, nn=self.nn.mutate(rate))

    def cross(self, other, rate):
        offspring_1, offspring_2 = self.nn.cross(other.nn, rate)
        return SnakeIndividual(self.snake, self.fruit, nn=offspring_1), \
               SnakeIndividual(self.snake, self.fruit, nn=offspring_2)

    def calculate_fitness(self):
        def get_distance(snake_head, fruit):  # Euclidean distance between the snake's head and the fruit
            return math.sqrt((snake_head.x - fruit.x) ** 2 + (snake_head.y - fruit.y) ** 2)

        current_distance = get_distance(self.snake.head, self.fruit)
        new_direction = self.get_new_direction()  # new snake direction computed from its NN outputs
        new_head = SnakeTile(self.snake.head.x + new_direction[0],
                             self.snake.head.y + new_direction[1])  # new snake head if it moves in new direction
        new_distance = get_distance(new_head, self.fruit)

        if new_head in self.snake.body \
                or new_head.x in [-1, AI_WINDOW_SQUARES_WIDTH] \
                or new_head.y in [-1, AI_WINDOW_SQUARES_HEIGHT]:  # 0 if the snake is going to die
            return 0

        reachable_nodes = bfs_check(self.snake, new_head)
        free_nodes = AI_WINDOW_SQUARES_WIDTH * AI_WINDOW_SQUARES_HEIGHT - len(self.snake.tiles)
        # trying to move to the node from which more other nodes can be reached -> computing the ratio
        reachable_nodes_ratio = reachable_nodes / free_nodes

        if len(self.snake.tiles) < int(0.25 * AI_WINDOW_SQUARES_WIDTH * AI_WINDOW_SQUARES_HEIGHT):
            if reachable_nodes_ratio < 0.9:  # ratio if the snake won't be able to reach at least 90% of the free nodes
                fitness = reachable_nodes_ratio
            else:
                if current_distance < new_distance:  # 2 if the snake will get further from the fruit
                    fitness = 2
                elif current_distance == new_distance:  # 3 if the distance won't change
                    fitness = 3
                else:  # 4 if the snake will get closer to the fruit
                    fitness = 4
        else:
            if current_distance < new_distance:
                multiplier = 1
            elif current_distance == new_distance:
                multiplier = 1.1
            else:
                multiplier = 1.2
            # for the long snake ratio is more valuable than the distance to the fruit
            fitness = reachable_nodes_ratio * multiplier
        return fitness

    def get_nn_inputs(self):
        inputs = []

        for direction in DIRECTIONS.keys():  # Left -> Up -> Right -> Down
            self.append_metadata(inputs, direction)

        return np.asarray(inputs)

    def append_metadata(self, inputs, direction):
        # For the given direction appends a distance to the wall, to the body and to the fruit to the given array

        axis, axis_dir = decode_direction(direction)
        head_coord = self.snake.head.x if axis == 0 else self.snake.head.y
        fruit_coord = self.fruit.x if axis == 0 else self.fruit.y

        wall_dist_coord = abs(head_coord - AI_WALLS[direction][axis]) - 1

        inputs.append(wall_dist_coord)  # distance along the axis to the wall
        inputs.append((fruit_coord - head_coord) * axis_dir)  # distance along the axis to the fruit

        for step in range(1, wall_dist_coord + 1):  # searching for the closest body tile along the axis
            new_tile_x = head_coord + axis_dir * step if axis == 0 else self.snake.head.x
            new_tile_y = head_coord + axis_dir * step if axis == 1 else self.snake.head.y

            if SnakeTile(new_tile_x, new_tile_y) in self.snake.body:
                inputs.append(step - 1)
                break
        else:
            inputs.append(wall_dist_coord)  # no body tile in this direction

    def get_new_direction(self):  # Decodes NN outputs and returns a new direction for the snake
        outputs = self.nn.forward_propagation(self.get_nn_inputs())
        assert outputs.shape == (1, NN_OUTPUT_LAYER_SIZE)

        chosen_dir_index = int(np.argmax(outputs))
        if chosen_dir_index == 0:  # turn to the left
            new_direction = (self.snake.direction[1], -self.snake.direction[0])
        elif chosen_dir_index == 2:  # turn to the right
            new_direction = (-self.snake.direction[1], self.snake.direction[0])
        else:  # continue forward
            new_direction = self.snake.direction
        return new_direction


def decode_direction(direction):
    if direction == "Left":
        return 0, -1
    elif direction == "Up":
        return 1, -1
    elif direction == "Right":
        return 0, 1
    elif direction == "Down":
        return 1, 1
