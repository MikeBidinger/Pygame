import pygame
from .block import Block
from .constants import WIDTH, HEIGHT, BLOCK_W, BLOCK_H, \
                       LENGTH_WINNER, ROWS, COLS, BLACK, GRAY


class Board():
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(Block(BLACK, row, col))

    def draw(self, win):
        # Blocks
        for row in range(ROWS):
            for col in range(COLS):
                block = self.board[row][col]
                if block != 0:
                    block.draw(win)
        # Gridlines
        for row in range(1, ROWS):
            pygame.draw.line(win, GRAY, (0, row * BLOCK_H),
                             (WIDTH, row * BLOCK_H))
            for col in range(1, COLS):
                pygame.draw.line(win, GRAY, (col * BLOCK_W, 0),
                                 (col * BLOCK_W, HEIGHT))

    def change_block(self, color, pos):
        col = pos[0] // BLOCK_W
        for i in range(1, ROWS + 1):
            block = self.board[-i][col]
            if block.color == BLACK:
                block.color = color
                return True
        return False

    def board_status(self):
        # Check for winner
        color = self._check_win(LENGTH_WINNER)
        if color == None:
            # Check if board is full
            for row in range(ROWS):
                for col in range(COLS):
                    block = self.board[row][col]
                    if block.color == BLACK:
                        return True
        return color

    def _check_win(self, length):
        # Directions (x, y):            (diagonal)
        #              right  down  right/down  right/up
        #               |       |       |        |
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        # For all possible directions (horizontal, vertical and both diagonals)
        for dir in directions:
            # Start-coordinate = (row, col)
            for row in range(ROWS):
                for col in range(COLS):
                    # End-coordinate = (x, y)
                    x = row + (length - 1) * dir[0]
                    y = col + (length - 1) * dir[1]
                    # Check if end-coordinate is valid (within board dimesion)
                    if (0 <= x < ROWS) and (0 <= y < COLS):
                        #print((row, col), (x, y))
                        # Check for win (all equal colors)
                        color = None
                        for i in range(length):
                            #print("", (row + i, col + i))
                            block = self.board[row + i *
                                               dir[0]][col + i * dir[1]]
                            if block.color == BLACK:
                                break
                            elif color == None:
                                color = block.color
                            elif color != block.color:
                                break
                            elif i == length - 1:
                                return color
        return None
