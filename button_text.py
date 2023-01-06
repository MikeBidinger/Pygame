import pygame
from pygame.locals import *

# Define colours
BG_COLOR = (204, 102, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
DEF_BUTTON = (200, 200, 200)

# Define global variable
counter = 0


def invert_rgb(rgb_val):
    r_val, g_val, b_val = rgb_val
    r_val = 255 - r_val
    g_val = 255 - g_val
    b_val = 255 - b_val
    return (r_val, g_val, b_val)


def darken_rgb(rgb_val, ratio=2, steps=4):
    r_val, g_val, b_val = rgb_val
    r_val = r_val - int(ratio * (r_val / steps))
    g_val = g_val - int(ratio * (g_val / steps))
    b_val = b_val - int(ratio * (b_val / steps))
    return (r_val, g_val, b_val)


def lighten_rgb(rgb_val, ratio=2, steps=4):
    r_val, g_val, b_val = rgb_val
    r_val = int(ratio * ((r_val + 255) / steps))
    g_val = int(ratio * ((g_val + 255) / steps))
    b_val = int(ratio * ((b_val + 255) / steps))
    return (r_val, g_val, b_val)


class States():
    def __init__(self):
        self.normal = 0
        self.hover = 1
        self.pressed = 2


button_states = States()


class Button():
    def __init__(self, width, height, x, y, value, font,
                 btn_col=DEF_BUTTON, border_px=1):
        # Rectangle
        self.rect = pygame.Rect(x, y, width, height)
        # State
        self.state = button_states.normal
        # Button
        self.value = value
        self.cur_btn_col = btn_col
        self.btn_col = btn_col
        self.darken_effect = False
        for i in btn_col:
            if i > 128:
                self.darken_effect = True
                break
        self.hover_col = self.btn_col
        self.press_col = self.btn_col
        # Text
        self.font = font
        self.txt_col = BLACK
        self.text = self.font.render(value, True, self.txt_col)
        # Border (shading)
        self.border_col = BLACK
        self.border_thickness = border_px

    def draw_button(self, surface):
        # Draw button
        pygame.draw.rect(surface, self.cur_btn_col, self.rect)
        # Draw text
        width = self.text.get_width()
        height = self.text.get_height()
        # Draw borders
        offset = int((self.border_thickness / 3) + (self.border_thickness / 5))
        x = self.rect.x + offset
        y = self.rect.y + offset
        top_left = (x, y)
        top_right = (x + self.rect.width - self.border_thickness, y)
        bottom_left = (x, y + self.rect.height - self.border_thickness)
        bottom_right = (x + self.rect.width - self.border_thickness,
                        y + self.rect.height - self.border_thickness)
        pygame.draw.line(surface, self.border_col,  # Top
                         top_left, top_right, self.border_thickness)
        pygame.draw.line(surface, self.border_col,  # Left
                         top_left, bottom_left, self.border_thickness)
        pygame.draw.line(surface, self.border_col,  # Bottom
                         bottom_left, bottom_right, self.border_thickness)
        pygame.draw.line(surface, self.border_col,  # Right
                         top_right, bottom_right, self.border_thickness)
        # Calculate position
        pos_x = self.rect.centerx - (width / 2)
        pos_y = self.rect.centery - (height / 2)
        # Draw button onto surface
        surface.blit(self.text, (pos_x, pos_y))

    def is_clicked(self, event):
        if self.is_collide():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.press = True
                self.change_color(button_states.pressed)
                return True
            else:
                return False
        else:
            return False

    def is_collide(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.change_color(button_states.hover)
            return True
        else:
            self.change_color(button_states.normal)
            return False

    def is_pressed(self):
        self.change_color(button_states.pressed)

    def change_color(self, state: States):
        if state == button_states.normal:
            self.cur_btn_col = self.btn_col
        if self.darken_effect:
            self.border_col = (0, 0, 0)
            self.txt_col = (0, 0, 0)
            if state == button_states.hover:
                self.cur_btn_col = darken_rgb(self.btn_col)
            elif state == button_states.pressed:
                self.cur_btn_col = darken_rgb(self.btn_col, 3)
        else:
            self.border_col = invert_rgb((0, 0, 0))
            self.txt_col = invert_rgb((0, 0, 0))
            if state == button_states.hover:
                self.cur_btn_col = lighten_rgb(self.btn_col)
            elif state == button_states.pressed:
                self.cur_btn_col = lighten_rgb(self.btn_col, 3)
        self.text = self.font.render(self.value, True, self.txt_col)
