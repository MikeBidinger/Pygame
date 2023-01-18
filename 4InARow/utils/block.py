import pygame
from pygame.locals import Rect
from .constants import BLOCK_W, BLOCK_H


class Block():
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = BLOCK_W * self.col
        self.y = BLOCK_H * self.row
        self.rect = Rect(self.x, self.y, BLOCK_W, BLOCK_H)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
