import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Font Demo")

FONT = pygame.font.SysFont("Constantia", 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = BLACK
DEF_BUTTON = (200, 200, 200)

font_list = pygame.font.get_fonts()
font_list.sort()
font_count = 0
font_amount = 20
font_len = len(font_list)

def draw_font_style(i):
    font = pygame.font.SysFont(font_list[i + font_count], 25)
    text_str = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    text_img = font.render(text_str, True, (255, 255, 255))
    text_rect = text_img.get_rect()
    text_rect.left = 2
    text_rect.top = (i * 35) + 15
    screen.blit(text_img, text_rect)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, text_rect.top, SCREEN_WIDTH, 35), 1)

def draw_font_name(i):
    text_img = FONT.render(font_list[i + font_count], True, (255, 255, 255))
    text_rect = text_img.get_rect()
    text_rect.right = SCREEN_WIDTH - 2
    text_rect.top = (i * 35) + 15
    screen.blit(text_img, text_rect)

def draw_fonts():
    for i in range(0, font_amount):
        if (i + font_count) > font_len:
            break
        draw_font_style(i)
        draw_font_name(i)


def invert_rgb(rgb_val):
    r_val = 255 - rgb_val[0]
    g_val = 255 - rgb_val[1]
    b_val = 255 - rgb_val[2]
    return (r_val, g_val, b_val)


def darken_rgb(rgb_val, ratio=2, steps=4):
    r_val = rgb_val[0] - int(ratio * (rgb_val[0] / steps))
    g_val = rgb_val[1] - int(ratio * (rgb_val[1] / steps))
    b_val = rgb_val[2] - int(ratio * (rgb_val[2] / steps))
    return (r_val, g_val, b_val)


def lighten_rgb(rgb_val, ratio=2, steps=4):
    r_val = rgb_val[0] + int(ratio * ((rgb_val[0] + 255) / steps))
    g_val = rgb_val[1] + int(ratio * ((rgb_val[1] + 255) / steps))
    b_val = rgb_val[2] + int(ratio * ((rgb_val[2] + 255) / steps))
    return (r_val, g_val, b_val)


class States():
    def __init__(self):
        self.normal = 0
        self.hover = 1
        self.pressed = 2


button_states = States()


class Button():
    def __init__(self, width, height, x, y, text,
                 btn_col=DEF_BUTTON, border_px=2, shading=True
                 ):
        # Metrics
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        # State
        self.state = button_states.normal
        # Text
        self.text = text
        # Colors
        self.button_col = btn_col
        self.darken_effect = False
        for i in self.button_col:
            if i > 128:
                self.darken_effect = True
                break
        if self.darken_effect:
            self.text_col = (0, 0, 0)
            self.border_color = (0, 0, 0)
            self.hover_col = darken_rgb(self.button_col)
            self.press_col = darken_rgb(self.button_col, 3)
        else:
            self.text_col = invert_rgb((0, 0, 0))
            self.border_color = invert_rgb((0, 0, 0))
            self.hover_col = lighten_rgb(self.button_col)
            self.press_col = lighten_rgb(self.button_col, 3)
        # Border (shading)
        self.border_thickness = border_px
        self.shading = shading

    def draw_button(self):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        # Create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)
        # Set button state
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.state = button_states.pressed
            elif pygame.mouse.get_pressed()[0] == 0 and self.state == button_states.pressed:
                self.state = button_states.hover
                action = True
            else:
                self.state = button_states.hover
        else:
            self.state = button_states.normal
        # Draw button (state dependent)
        if self.state == button_states.normal:
            pygame.draw.rect(screen, self.button_col, button_rect)
        elif self.state == button_states.hover:
            pygame.draw.rect(screen, self.hover_col, button_rect)
        elif self.state == button_states.pressed:
            pygame.draw.rect(screen, self.press_col, button_rect)
        # Draw border (state and shading dependent)
        if self.shading:
            top_left = WHITE
            bottom_right = BLACK
        else:
            top_left = self.border_color
            bottom_right = self.border_color
        if self.state == button_states.hover or self.state == button_states.pressed:
            top_left = invert_rgb(top_left)
            bottom_right = invert_rgb(bottom_right)
        pygame.draw.line(screen, top_left, (self.x, self.y),
                         (self.x + self.width, self.y), self.border_thickness)
        pygame.draw.line(screen, top_left, (self.x, self.y),
                         (self.x, self.y + self.height), self.border_thickness)
        pygame.draw.line(screen, bottom_right, (self.x, self.y + self.height),
                         (self.x + self.width, self.y + self.height), self.border_thickness)
        pygame.draw.line(screen, bottom_right, (self.x + self.width, self.y),
                         (self.x + self.width, self.y + self.height), self.border_thickness)
        # Draw text (state dependent)
        col_val = self.text_col
        if self.state == button_states.hover or self.state == button_states.pressed:
            col_val = invert_rgb(self.text_col)
        text_img = FONT.render(self.text, True, col_val)
        text_rect = text_img.get_rect()
        text_rect.center = ((self.x + (self.width // 2),
                            self.y + (self.height // 2)))
        screen.blit(text_img, text_rect)
        # Return click action
        return action


# Create buttons
previous = Button(40, 40, 10, 750, '<')
next = Button(40, 40, 1150, 750, '>')

run = True
while run:

    screen.fill(BG_COLOR)

    draw_fonts()

    if previous.draw_button():
        font_count -= font_amount
        if font_count < 0:
            font_count = 0
    if next.draw_button():
        font_count += font_amount
        if font_count + font_amount > font_len:
            font_count = font_len - font_amount

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()
