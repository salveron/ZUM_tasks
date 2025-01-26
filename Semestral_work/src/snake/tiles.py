from abc import ABC, abstractmethod

from snake.utils import *

import pygame


class Tile(ABC):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    @property
    def outer_rect(self):
        return pygame.Rect(self.x * SQUARE_WIDTH, self.y * SQUARE_HEIGHT, self.width, self.height)

    @property
    def inner_rect(self):
        return pygame.Rect(self.x * SQUARE_WIDTH + SQUARE_BORDER_SIZE,
                           self.y * SQUARE_HEIGHT + SQUARE_BORDER_SIZE,
                           self.width - 2 * SQUARE_BORDER_SIZE,
                           self.height - 2 * SQUARE_BORDER_SIZE)

    @property
    def pos(self):
        return self.x, self.y

    @abstractmethod
    def draw(self, window):
        pass


class ButtonTile(Tile):
    def __init__(self, x, y, width, height, selected, text, action=lambda: None):
        super().__init__(x, y, width, height)
        self.x *= SQUARE_WIDTH
        self.y *= SQUARE_HEIGHT

        self.font = pygame.font.SysFont(MM_BUTTON_FONT, MM_BUTTON_FONT_SIZE)
        self.selected = selected
        self.text = text
        self.action = action

    def draw(self, window):
        if self.selected:
            pygame.draw.rect(window, MM_SELECTED_BUTTON_BORDER_COLOR, self.outer_rect)
            pygame.draw.rect(window, MM_SELECTED_BUTTON_COLOR, self.inner_rect)
            text_pos = (self.x + (self.width - self.font.size(self.text)[0]) // 2,
                        self.y + (self.height - self.font.size(self.text)[1]) // 2 + int(0.1 * MM_BUTTON_HEIGHT))
            window.blit(self.font.render(self.text, True, MM_SELECTED_BUTTON_FONT_COLOR), text_pos)
        else:
            pygame.draw.rect(window, MM_BUTTON_BORDER_COLOR, self.outer_rect)
            pygame.draw.rect(window, MM_BUTTON_COLOR, self.inner_rect)
            text_pos = (self.x + (self.width - self.font.size(self.text)[0]) // 2,
                        self.y + (self.height - self.font.size(self.text)[1]) // 2 + int(0.1 * MM_BUTTON_HEIGHT))
            window.blit(self.font.render(self.text, True, MM_BUTTON_FONT_COLOR), text_pos)

    @property
    def outer_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def inner_rect(self):
        if self.selected:
            return pygame.Rect(self.x + MM_SELECTED_BUTTON_BORDER_SIZE,
                               self.y + MM_SELECTED_BUTTON_BORDER_SIZE,
                               self.width - 2 * MM_SELECTED_BUTTON_BORDER_SIZE,
                               self.height - 2 * MM_SELECTED_BUTTON_BORDER_SIZE)
        else:
            return pygame.Rect(self.x + MM_BUTTON_BORDER_SIZE,
                               self.y + MM_BUTTON_BORDER_SIZE,
                               self.width - 2 * MM_BUTTON_BORDER_SIZE,
                               self.height - 2 * MM_BUTTON_BORDER_SIZE)


class SnakeTile(Tile):
    def __init__(self, x, y, width=SQUARE_WIDTH, height=SQUARE_HEIGHT):
        super().__init__(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, SNAKE_TILE_BORDER_COLOR, self.outer_rect)
        pygame.draw.rect(window, SNAKE_TILE_COLOR, self.inner_rect)


class FruitTile(Tile):
    def __init__(self, x, y, width=SQUARE_WIDTH, height=SQUARE_HEIGHT):
        super().__init__(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, FRUIT_TILE_BORDER_COLOR, self.outer_rect)
        pygame.draw.rect(window, FRUIT_TILE_COLOR, self.inner_rect)
