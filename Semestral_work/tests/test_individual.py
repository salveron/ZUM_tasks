import pytest

from snake import Snake
from tiles import FruitTile
from ai.snake_individual import SnakeIndividual
from utils import *


snake = Snake(NORMAL_HEAD_START_X, NORMAL_HEAD_START_Y)
fruit = FruitTile(NORMAL_HEAD_START_X + 1, NORMAL_HEAD_START_Y)
individual = SnakeIndividual(snake, fruit)
nn_inputs = nn_inputs_type(*individual.get_nn_inputs())


def test_nn_inputs():
    assert len(nn_inputs) == 12
    assert all(x >= 0 for x in list(nn_inputs)[::3])  # distances to the walls
    assert all(x >= 0 for x in list(nn_inputs)[2::3])  # distances to the body
    assert nn_inputs.lw == NORMAL_HEAD_START_X  # distance to the left wall
    assert nn_inputs.rf == 1  # distance to the fruit to the right
    assert nn_inputs.lf == -nn_inputs.rf
    assert nn_inputs.uf == nn_inputs.df
