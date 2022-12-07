import pygame
from os.path import join
import math
import random

from json_functions import read_json

pygame.init()

# Consts:
# - Screen
WIDTH, HEIGHT = 800, 500
FPS = 60
# - Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
# - Buttons
RADIUS = 20
GAP = 15
# - Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Variables
words_data = read_json("words.json")
word_length = 3
start_game = False

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spelling Game")
clock = pygame.time.Clock()


def display_message(message, color, delay=True):
    win.fill(WHITE)
    if type(message) == str:
        text = WORD_FONT.render(message, 1, color)
        win.blit(text, (WIDTH / 2 - text.get_width() /
                        2, HEIGHT / 2 - text.get_height() / 2))
    elif type(message) == list:
        for idx, msg in enumerate(message):
            text = WORD_FONT.render(msg, 1, color)
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, 100 + idx * 100))
    pygame.display.update()
    if delay:
        pygame.time.delay(1500)


def draw(word, folder, letters):
    win.fill(WHITE)

    # Draw word
    display_word = ""
    for i in range(len(word)):
        if i < len(letters):
            display_word += letters[i] + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw image
    image = pygame.image.load(join("img", folder, word + ".png"))
    win.blit(image, (100, 90))

    pygame.display.update()


def check_spelling(chk):
    if chk:
        image = pygame.image.load(join("img", "ok.png"))
    else:
        image = pygame.image.load(join("img", "nok.png"))
    _, _, width, height = image.get_rect()
    win.blit(image, (WIDTH / 2 - width / 2, HEIGHT - height - 10))
    pygame.display.update()
    pygame.time.delay(1000)
    return chk


# Game loop
def main(words):
    run = True

    # Game variables
    word = random.choice(words)
    letters = ""

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(letters) == len(word):
                        if check_spelling(letters == word.upper()):
                            words.remove(word)
                            if len(words) == 0:
                                run = False
                                break
                        word = random.choice(words)
                        letters = ""
                        break
                elif event.key == pygame.K_BACKSPACE:
                    letters = letters[:-1]
                elif event.unicode.isalpha() and len(letters) < len(word):
                    letters += event.unicode.upper()

        draw(word, str(word_length), letters)

    return True


if __name__ == "__main__":
    run = True

    while run:
        if start_game:
            if main(words):
                word_length += 1
                start_game = False
            else:
                run = False
        else:
            display_message(
                ["Enter amount and press enter to start", str(word_length)], BLACK, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and word_length >= 3:
                    start_game = True
                    print(word_length)
                    words = words_data[str(word_length)]
                elif event.key == pygame.K_BACKSPACE:
                    if len(str(word_length)) == 1:
                        word_length = 0
                    else:
                        word_length = int(str(word_length)[:-1])
                elif event.unicode.isnumeric():
                    word_length = int(str(word_length) + event.unicode)

pygame.quit()
