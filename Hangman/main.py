import pygame
import math
import random
from os.path import join

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
word_length = ""
start_game = False

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")
clock = pygame.time.Clock()

# Load images
images = []
for i in range(10):
    image = pygame.image.load(join("img", "hangman" + str(i) + ".png"))
    images.append(image)


def set_letters():
    letters = []
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(65 + i), True])
    return letters


def draw(word, guessed, letters, hangman_status):
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 2)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - (text.get_width() / 2),
                     y - (text.get_height() / 2)))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message, color, delay=True):
    if delay:
        pygame.time.delay(500)
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


# Game loop
def main(word_length):
    run = True

    # Game variables
    hangman_status = 0
    words = words_data[word_length]
    word = random.choice(words)
    guessed = []
    letters = set_letters()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw(word, guessed, letters, hangman_status)

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("WON!", GREEN)
            break

        if hangman_status == 9:
            display_message("LOST!", RED)
            break

    return True


if __name__ == "__main__":
    run = True

    while run:
        if start_game:
            if main(word_length):
                start_game = False
            else:
                break
        else:
            display_message(
                ["Enter amount and press enter to start", word_length], BLACK, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game = True
                elif event.key == pygame.K_BACKSPACE:
                    word_length = word_length[:-1]
                elif event.unicode.isnumeric():
                    word_length += event.unicode
                    if word_length not in words_data:
                        word_length = word_length[:-1]

pygame.quit()
