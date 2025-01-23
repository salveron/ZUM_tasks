from game import *
from ai.evolution import *


class MainMenu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(NORMAL_WINDOW_SIZE)
        pygame.display.set_caption("Snake Menu")
        self.running = True

        self.background_image = pygame.image.load("sprites/mm_bg.jpg").convert()
        self.selected_button = 0
        self.buttons = [ButtonTile(MM_FIRST_BUTTON_X,
                                   MM_FIRST_BUTTON_Y,
                                   MM_BUTTON_WIDTH,
                                   MM_BUTTON_HEIGHT,
                                   selected=True,
                                   text=MM_BUTTON_TEXTS[0]),
                        ButtonTile(MM_FIRST_BUTTON_X,
                                   MM_FIRST_BUTTON_Y + 2 * MM_BUTTON_SQUARE_HEIGHT,
                                   MM_BUTTON_WIDTH,
                                   MM_BUTTON_HEIGHT,
                                   selected=False,
                                   text=MM_BUTTON_TEXTS[1]),
                        ButtonTile(MM_FIRST_BUTTON_X,
                                   MM_FIRST_BUTTON_Y + 4 * MM_BUTTON_SQUARE_HEIGHT,
                                   MM_BUTTON_WIDTH,
                                   MM_BUTTON_HEIGHT,
                                   selected=False,
                                   text=MM_BUTTON_TEXTS[2])]

    def draw(self):
        self.window.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(self.window)

    def handle_keys(self, key):
        if len(self.buttons) in [0, 1]:
            return

        if (key == pygame.K_w or key == pygame.K_UP) and self.selected_button > 0:
            self.buttons[self.selected_button].selected = False
            self.selected_button -= 1
            self.buttons[self.selected_button].selected = True

        elif (key == pygame.K_s or key == pygame.K_DOWN) and self.selected_button < len(self.buttons) - 1:
            self.buttons[self.selected_button].selected = False
            self.selected_button += 1
            self.buttons[self.selected_button].selected = True

        elif key == pygame.K_RETURN:
            if self.buttons[self.selected_button].text == MM_BUTTON_TEXTS[0]:
                Game().start()
            elif self.buttons[self.selected_button].text == MM_BUTTON_TEXTS[1]:
                Game(ai_playing=True).start()
            elif self.buttons[self.selected_button].text == MM_BUTTON_TEXTS[2]:
                self.running = False
                return

            pygame.display.quit()
            pygame.display.init()
            self.window = pygame.display.set_mode(NORMAL_WINDOW_SIZE)

    def start(self):
        while self.running:
            self.clock.tick(HUMAN_GAME_FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.handle_keys(pygame.K_w)
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.handle_keys(pygame.K_s)
                elif keys[pygame.K_RETURN]:
                    self.handle_keys(pygame.K_RETURN)

            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    MainMenu().start()
    pygame.quit()
