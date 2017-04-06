import pygame
from Utils import *
import Menus
import settings

RUNNING = True
SCREEN = None
RESOLUTION = None
CURRENT_WINDOW = None


def main():
    pygame.font.init()
    read_settings()
    build_window()
    loop()


def build_window():
    global RESOLUTION, SCREEN
    # Create the game screen
    SCREEN = pygame.display.set_mode(RESOLUTION)
    # Set window info
    pygame.display.set_icon(SCREEN)
    pygame.display.set_caption('Solaris')
    pygame.display.flip()


def read_settings():
    try:
        settings_file = open('config.txt', 'r')
    except:
        make_settings()
        settings_file = open('config.txt', 'r')
    lines = settings_file.readlines()
    for line in lines:
        if line.startswith('resolution'):
            global RESOLUTION
            fields = line.strip().split()
            RESOLUTION = (int(fields[1]), int(fields[2]))


def make_settings():
    settings_file = open('config.txt', 'w')
    contents = 'resolution 800 600'
    settings_file.writelines(contents)


def loop():
    global CURRENT_WINDOW
    game_clock = pygame.time.Clock()
    while RUNNING is True:
        game_clock.tick(60)
        window_event_handler()
        if CURRENT_WINDOW is None:
            CURRENT_WINDOW = Menus.MainMenu
        CURRENT_WINDOW.render()


def render():
    global SCREEN
    # Commit changes to screen
    pygame.display.flip()


# Check if the user interacts with the window
def window_event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global RUNNING
            RUNNING = False
            return

if __name__ == '__main__':
    main()