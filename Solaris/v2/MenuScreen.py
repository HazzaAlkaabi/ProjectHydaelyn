import pygame


class Menu:
    def __init__(self, SCREEN, RESOLUTION, background_color, splash_title, buttons):
        self.SCREEN = SCREEN
        self.RESOLUTION = RESOLUTION
        self.background = pygame.Surface(RESOLUTION)
        self.background.fill(background_color)
        self.buttons = buttons
        self.splash_title = splash_title

        # Create text modules
        self.title_text = pygame.font.SysFont('Arial', 50)
        self.context_text = pygame.font.SysFont('Arial', 20)

    def render(self):
        # Title splash
        title = self.title_text.render(self.splash_title, False, (255, 255, 255))
        title_rect = title.get_rect(center=(self.RESOLUTION[0]/2, self.RESOLUTION[1]/2 - 150))
        self.SCREEN.blit(title, title_rect)

        # Render buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        for button in self.buttons:
            button.check_active(mouse_pos, mouse_click)
            button.render(self.SCREEN)

        # Apply to screen
        pygame.display.flip()


class MenuButton:
    def __init__(self, pos, idle_color, active_color, text_render, label, command):
        self.pos = pos
        self.size = [0, 0]
        self.idle_color = idle_color
        self.active_color = active_color
        self.text_render = text_render
        self.active = False
        self.label = label
        self.command = command

    def check_active(self, mouse_pos, mouse_click):
        left_bound = self.pos[0] - self.size[0]/2
        right_bound = self.pos[0] + self.size[0]/2
        top_bound = self.pos[1] - self.size[1]/2
        bottom_bound = self.pos[1] + self.size[1]/2
        x_active = False
        y_active = False
        if left_bound <= mouse_pos[0] <= right_bound:
            x_active = True
        if top_bound <= mouse_pos[1] <= bottom_bound:
            y_active = True
        if x_active is True and y_active is True:
            self.active = True
        else:
            self.active = False

        if self.active is True and mouse_click[0] == 1:
            button_handler(self.label)

    def render(self, SCREEN):
        color = self.idle_color
        if self.active is True:
            color = self.active_color
        label = self.text_render.render(self.label, False, color)
        render_rect = label.get_rect(center=(self.pos[0], self.pos[1]))
        self.size = render_rect.size
        SCREEN.blit(label, render_rect)


def button_handler(command):
    command = command.strip().lower()
    if command == 'play':
        pass
    elif command == 'options':
        pass
    elif command == 'quit':
        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
