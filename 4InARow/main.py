import pygame
from utils.constants import WIDTH, HEIGHT, FONT, CLOSE_FONT, WHITE, BLACK, RED
from utils.menu import Menu, Button
from utils.game_state import GameState
from utils.game import Game

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 In A Row")

BTN_CLOSE = Button("X", CLOSE_FONT, 1, RED)
BTN_CLOSE = BTN_CLOSE.create(WIDTH - 40, 10, 30, 30)
# if BTN_CLOSE.draw(WIN):
#     gs.get(gs)
BTN_MAIN = [
    Button("2 Players", FONT, 2, BLACK),
    # Button("1 Player", FONT, 3, BLACK)
]
MAIN_MENU = Menu(WIN, WHITE, 75, BTN_MAIN, 100, 20)


def play(gs: GameState):
    game = Game()

    while gs.state == gs.pvp or gs.state == gs.pve:

        pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gs.get(gs)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    pos = pygame.mouse.get_pos()
                    break

        game.update(WIN, pos)

        if game.won:
            game.draw_won(WIN, game.won)
        elif game.tie:
            game.draw_tie(WIN)

        pygame.display.update()

        if game.won or game.tie:
            gs.state = gs.main
            pygame.time.delay(2000)


def main():
    gs = GameState()

    while gs.state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        WIN.fill(BLACK)

        if gs.state == gs.main:
            MAIN_MENU.draw(WIN, gs)
        else:
            if play(gs) == False:
                return

        pygame.display.update()


if __name__ == "__main__":
    main()
