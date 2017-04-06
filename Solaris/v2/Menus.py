import pygame
from MenuScreen import *

RESOLUTION = None
SCREEN = None

def set_globals():
    global RESOLUTION, SCREEN


def main_menu_buttons():
    button_text = pygame.font.SysFont('Arial', 30)
    center_x = RESOLUTION[0] / 2
    center_y = RESOLUTION[1] / 2
    center = [center_x, center_y]
    idle_color = (255, 255, 255)
    active_color = (100, 255, 100)
    play_button = MenuButton(center, idle_color, active_color, button_text, 'Play', 'Play')
    options_button = MenuButton([center_x, center_y + 50], idle_color, active_color, button_text, 'Options', 'Options')
    quit_button = MenuButton([center_x, center_y + 100], idle_color, active_color, button_text, 'Quit', 'Quit')
    buttons = [play_button, options_button, quit_button]
    return buttons

MainMenu = Menu(SCREEN, RESOLUTION, (0, 0, 0), 'Solaris', main_menu_buttons())