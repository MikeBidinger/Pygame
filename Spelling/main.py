import pygame
from os.path import join
import math
import random
# from pprint import pprint as pp

from json_functions import read_json, write_json

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
player_name = ""
start_game = False

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spelling Game")
clock = pygame.time.Clock()


class Player():
    def __init__(self, name, player_object=None):
        if player_object != None:
            self.name = name
            self.level = player_object["level"]
        elif name != "":
            self.name = name
            self.level = 3


def load_players():
    players = {}
    players_data = read_json("players.json")
    for player in players_data:
        players[player] = Player(player, player_object=players_data[player])
    return players


def save_players(players):
    players_output = {}
    for name in players:
        player = players[name]
        players_output[name] = {}
        players_output[name]["level"] = player.level
    write_json("players", players_output)


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
def main(player, words):
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

        draw(word, str(player.level), letters)

    return True


if __name__ == "__main__":
    run = True

    words_data = read_json("words.json")
    players = load_players()

    while run:
        if start_game:
            if main(player, words):
                player.level += 1
                start_game = False
                save_players(players)
            else:
                run = False
        else:
            display_message(
                ["Naam:", player_name.upper()], BLACK, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if player_name != "":
                    if event.key == pygame.K_RETURN:
                        if player_name not in players:
                            player = Player(player_name)
                            players[player.name] = player
                            save_players(players)
                        else:
                            player = players[player_name]
                        start_game = True
                        words = words_data[str(player.level)]
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                if event.unicode.isalpha():
                    player_name += event.unicode

pygame.quit()
