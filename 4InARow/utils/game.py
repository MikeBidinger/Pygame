import pygame
from pygame.locals import Rect
from .board import Board
from .constants import WIDTH, HEIGHT, FONT, WHITE, BLACK, RED, YELLOW


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = RED
        self.won = None
        self.tie = False

    def _change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = YELLOW
        else:
            self.turn = RED

    def update(self, win, pos=None):
        status = self.board.board_status()
        if status == None:
            self.tie = True
        elif type(status) == tuple:
            self.won = status
        else:
            if pos != None:
                if self.board.change_block(self.turn, pos):
                    self._change_turn()
            self.board.draw(win)

    def draw_tie(self, surface):
        text_img = FONT.render("It's a tie!", 1, WHITE)
        dim = (text_img.get_width(), text_img.get_height())
        pos = (WIDTH // 2 - dim[0] // 2, HEIGHT // 2 - dim[1] // 2)
        pygame.draw.rect(surface, WHITE, Rect(pos[0] - 29, pos[1] - 14,
                                              dim[0] + 58, dim[1] + 28))
        pygame.draw.rect(surface, BLACK, Rect(pos[0] - 25, pos[1] - 10,
                                              dim[0] + 50, dim[1] + 20))
        surface.blit(text_img, pos)

    def draw_won(self, surface, color):
        if color == RED:
            text_img = FONT.render("Red player wins!", 1, WHITE)
            rect = text_img.get_rect()
        else:
            text_img = FONT.render("Yellow player wins!", 1, WHITE)
            rect = text_img.get_rect()
        dim = (text_img.get_width(), text_img.get_height())
        pos = (WIDTH // 2 - dim[0] // 2, HEIGHT // 2 - dim[1] // 2)
        pygame.draw.rect(surface, WHITE, Rect(pos[0] - 29, pos[1] - 14,
                                              dim[0] + 58, dim[1] + 28))
        pygame.draw.rect(surface, BLACK, Rect(pos[0] - 25, pos[1] - 10,
                                              dim[0] + 50, dim[1] + 20))
        surface.blit(text_img, pos)
