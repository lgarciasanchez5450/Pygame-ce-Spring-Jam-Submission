if __name__ != '__main__': raise RuntimeError

import pygame
import menu
import game

win = pygame.Window(
    title = 'A Game About Pushing Boxes',
    size = (1920,1080),
    fullscreen = True
)
main_menu = menu.MainMenu(win)
while True:
    main_menu.run()
    try:
        g = game.Game(win)
        g.run()
    except SystemExit as err:
        if err.code != 1:
            raise


    