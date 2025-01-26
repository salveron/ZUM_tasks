import pytest

from snake.snake import Snake
from snake.tiles import FruitTile
from snake.ai.evolution import Evolution
from snake.ai.snake_individual import SnakeIndividual
from snake.utils import *

snake = Snake(NORMAL_HEAD_START_X, NORMAL_HEAD_START_Y)
fruit = FruitTile(NORMAL_HEAD_START_X + 1, NORMAL_HEAD_START_Y)
evolution = Evolution(snake, fruit, pop_size=50)


def test_creation():
    assert len(evolution.population) == 50
    assert evolution.population[0].fitness <= evolution.population[-1].fitness
    assert all(isinstance(x, SnakeIndividual) for x in evolution.population)


def test_selection():
    selected = evolution.selection(how_many=30)
    assert len(selected) == 30
    assert all(isinstance(x, SnakeIndividual) for x in selected)
