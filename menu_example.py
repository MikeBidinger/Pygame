import pygame
from pygame import Rect
from game_state import GameState
from menu import Menu, Button, WHITE, BLACK, RED, GREEN, BLUE

WIDTH, HEIGHT = (500, 800)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(BLACK)
pygame.display.set_caption("Multi Menu (test)")
pygame.font.init()
FONT = pygame.font.SysFont("arialrounded", 25)

BTN_MAIN = [
    Button("Menu", FONT, GameState().menu, GREEN),
    Button("Settings", FONT, GameState().settings, BLUE)
]
BTN_MENU = [
    Button("Main", FONT, GameState().main, WHITE),
    Button("Settings", FONT, GameState().settings, BLUE)
]
BTN_SETTINGS = [
    Button("Main", FONT, GameState().main, WHITE),
    Button("Menu", FONT, GameState().menu, GREEN)
]


main_menu = Menu(WIN, WHITE, 50, BTN_MAIN, 50)
menu = Menu(WIN, GREEN, 50, BTN_MENU, 100, True)
setting_menu = Menu(WIN, BLUE, 50, BTN_SETTINGS, 100, True)


def main():
    gs = GameState()

    while gs.state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gs.state = gs.quit

        if gs.state == gs.main:
            main_menu.draw(WIN, gs)
        elif gs.state == gs.menu:
            menu.draw(WIN, gs)
        elif gs.state == gs.settings:
            setting_menu.draw(WIN, gs)

        pygame.display.update()


main()

pygame.quit()
