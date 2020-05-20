import random

from snake import *
from ai.evolution import Evolution


class Game:
    def __init__(self, ai_playing=False):
        self.ai_playing = ai_playing

        self.clock = pygame.time.Clock()

        if not self.ai_playing:
            self.window_width = NORMAL_WINDOW_WIDTH
            self.window_height = NORMAL_WINDOW_HEIGHT
            self.window_squares_width = NORMAL_WINDOW_SQUARES_WIDTH
            self.window_squares_height = NORMAL_WINDOW_SQUARES_HEIGHT
            self.window_size = NORMAL_WINDOW_SIZE
            self.snake = Snake(NORMAL_HEAD_START_X, NORMAL_HEAD_START_Y)
        else:
            self.window_width = AI_WINDOW_WIDTH
            self.window_height = AI_WINDOW_HEIGHT
            self.window_squares_width = AI_WINDOW_SQUARES_WIDTH
            self.window_squares_height = AI_WINDOW_SQUARES_HEIGHT
            self.window_size = AI_WINDOW_SIZE
            self.snake = Snake(AI_HEAD_START_X, AI_HEAD_START_Y)

        pygame.display.quit()
        pygame.display.init()
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Snake")

        self.background_image = pygame.image.load("sprites/game_bg.jpg").convert()
        self.score_image = pygame.image.load("sprites/score_bg.jpg").convert()

        pygame.transform.scale(self.window, self.window_size)
        self.window.blit(self.background_image, (0, 0))
        self.window.blit(self.score_image, (0, self.window_height))

        self.fruit = self.spawn_fruit()

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.snake.direction != DIRECTIONS["Right"]:
            self.snake.direction = DIRECTIONS["Left"]
        elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.snake.direction != DIRECTIONS["Down"]:
            self.snake.direction = DIRECTIONS["Up"]
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.snake.direction != DIRECTIONS["Left"]:
            self.snake.direction = DIRECTIONS["Right"]
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.snake.direction != DIRECTIONS["Up"]:
            self.snake.direction = DIRECTIONS["Down"]

    def redraw_snake(self):
        self.window.blit(self.background_image,
                         (self.snake.prev_tail.x * SQUARE_WIDTH, self.snake.prev_tail.y * SQUARE_HEIGHT),
                         self.snake.prev_tail.outer_rect)
        self.snake.head.draw(self.window)

    def print_score(self):
        font = pygame.font.SysFont(SCORE_FONT, SCORE_FONT_SIZE, bold=True)
        text = f"Score: {self.snake.score}"
        text_pos = ((self.window_width - font.size(text)[0]) // 2,
                     self.window_height + (SQUARE_HEIGHT - font.size(text)[1]) // 2 + int(0.1 * SQUARE_HEIGHT))
        self.window.blit(self.score_image, (0, self.window_height))
        self.window.blit(font.render(text, True, SCORE_FONT_COLOR), text_pos)

    def spawn_fruit(self):
        fruit = FruitTile(random.randrange(0, self.window_squares_width),
                          random.randrange(0, self.window_squares_height))
        if fruit in self.snake.tiles:
            fruit = self.spawn_fruit()
        fruit.draw(self.window)
        pygame.display.update()
        return fruit

    def start(self):
        while self.snake.alive:
            if not self.ai_playing:
                self.clock.tick(HUMAN_GAME_FPS)
            else:
                self.clock.tick(AI_GAME_FPS)

            if self.ai_playing:
                self.snake.direction = Evolution(self.snake, self.fruit).start().get_new_direction()
                # print(f"Direction: {self.snake.direction}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.snake.alive = False
                    break

                if not self.ai_playing:
                    self.check_keys()

            try:
                self.snake.move(self.fruit)
            except FruitEatenException:
                self.fruit = self.spawn_fruit()

            self.snake.check(self.window_squares_width, self.window_squares_height)
            self.redraw_snake()
            self.print_score()
            pygame.display.update()

        pygame.time.delay(1000)
        # print(f"Moves: {self.snake.move_counter}, score: {self.snake.score}")
