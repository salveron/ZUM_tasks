from collections import deque

from tiles import *


class Snake:
    def __init__(self, head_start_x, head_start_y):
        self.alive = True
        self.tiles = deque([SnakeTile(head_start_x, head_start_y)])
        self.direction = DIRECTIONS["Right"]
        self.prev_tail = self.tail

        self.score = 0
        self.move_counter = 0

    @property
    def head(self):
        return self.tiles[0]

    @property
    def body(self):
        return list(self.tiles)[1:]

    @property
    def tail(self):
        return self.tiles[-1]

    def move(self, fruit):
        self.tiles.appendleft(SnakeTile(self.head.x + self.direction[0],
                                        self.head.y + self.direction[1]))
        self.move_counter += 1

        if self.head.pos != fruit.pos:
            self.prev_tail = self.tiles.pop()
        else:
            self.score += 1
            raise FruitEatenException()

    def check(self, win_sq_width, win_sq_height):
        if len(self.tiles) > 4 and self.head in self.body:
            print("Game over. The snake collided with its body.")
            self.alive = False
        elif self.head.x < 0 or self.head.x >= win_sq_width or self.head.y < 0 or self.head.y >= win_sq_height:
            print("Game over. The snake collided with the wall.")
            self.alive = False
