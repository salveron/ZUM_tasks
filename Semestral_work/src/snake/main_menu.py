from snake.ai.evolution import *
from snake.game import *
from snake.utils import *

import pygame


class MainMenu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(NORMAL_WINDOW_SIZE)
        pygame.display.set_caption("Snake Menu")
        self.running = True

        self.background_image = pygame.image.load("src/sprites/mm_bg.jpg").convert()

        self.selected_button = 0
        self.buttons = [ButtonTile(MM_FIRST_BUTTON_X,
                                   MM_FIRST_BUTTON_Y,
                                   MM_BUTTON_WIDTH,
                                   MM_BUTTON_HEIGHT,
                                   selected=True,
                                   text="Classic Snake",
                                   action=lambda: Game().start()),
                        ButtonTile(MM_FIRST_BUTTON_X,
                                   MM_FIRST_BUTTON_Y + 2 * MM_BUTTON_SQUARE_HEIGHT,
                                   MM_BUTTON_WIDTH,
                                   MM_BUTTON_HEIGHT,
                                   selected=False,
                                   text="Snake AI",
                                   action=lambda: Game(ai_playing=True).start()),
                        ButtonTile(MM_FIRST_BUTTON_X,
                                   MM_FIRST_BUTTON_Y + 4 * MM_BUTTON_SQUARE_HEIGHT,
                                   MM_BUTTON_WIDTH,
                                   MM_BUTTON_HEIGHT,
                                   selected=False,
                                   text="Quit")]

    def draw(self):
        self.window.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(self.window)

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.buttons[self.selected_button].action()

            if self.selected_button == 2:
                self.running = False
                return

        elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.selected_button > 0:
            self.buttons[self.selected_button].selected = False
            self.selected_button -= 1
            self.buttons[self.selected_button].selected = True

        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.selected_button < len(self.buttons) - 1:
            self.buttons[self.selected_button].selected = False
            self.selected_button += 1
            self.buttons[self.selected_button].selected = True

    def start(self):
        while self.running:
            self.clock.tick(HUMAN_GAME_FPS)
            self.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                self.handle_keys()

