from snake.main_menu import MainMenu

import pygame


def main():
    pygame.init()
    pygame.font.init()
    MainMenu().start()
    pygame.quit()


if __name__ == "__main__":
    main()
