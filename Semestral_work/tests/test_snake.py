import pytest

from snake.snake import Snake
from snake.tiles import FruitTile
from snake.utils import *


def test_snake_creation():
    snake = Snake(NORMAL_HEAD_START_X, NORMAL_HEAD_START_Y)
    assert len(snake.tiles) == 1
    assert snake.head == snake.tail
    assert snake.head.pos == (NORMAL_HEAD_START_X, NORMAL_HEAD_START_Y)
    assert snake.alive
    assert snake.direction == DIRECTIONS["Right"]
    assert snake.score == 0 and snake.move_counter == 0


def test_moving():
    snake = Snake(1, 1)
    fruit = FruitTile(3, 1)
    snake.move(fruit)
    assert snake.head.pos == (2, 1)
    assert snake.direction == DIRECTIONS["Right"]
    assert (snake.head.x != fruit.x or snake.head.y != fruit.y) and snake.head.pos != fruit.pos
    assert snake.move_counter == 1 and snake.score == 0
    assert len(snake.tiles) == 1

    with pytest.raises(FruitEatenException):
        snake.move(fruit)
    assert snake.head.pos == fruit.pos
    assert snake.move_counter == 2 and snake.score == 1
    assert len(snake.tiles) == 2 and snake.head.pos != snake.tail.pos
