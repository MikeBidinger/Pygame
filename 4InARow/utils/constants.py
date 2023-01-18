import pygame

pygame.font.init()

WIDTH, HEIGHT = 700, 600
ROWS, COLS = 6, 7
BLOCK_W, BLOCK_H = WIDTH // COLS, HEIGHT // ROWS
LENGTH_WINNER = 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DEF_BUTTON = (200, 200, 200)

FONT = pygame.font.SysFont("arialrounded", 40)
CLOSE_FONT = pygame.font.SysFont("arialrounded", 25)
