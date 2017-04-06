import pygame


class HUD:
    def __init__(self):
        self.elements = []

    def render(self, screen):
        for element in self.elements:
            element.render(screen)


class HUDButton:
    def __init__(self, fonts, label, pos, action_listener, command, command_parms=None):
        self.fonts = fonts
        self.label = label
        self.pos = pos
        self.rect = None
        self.color = (255, 255, 255)
        self.active = False
        self.action_listener = action_listener
        self.command = command
        self.mouse_state = 0
        self.command_param= command_parms

    def check_active(self):
        if self.rect is None:
            return

        mouse_pos = pygame.mouse.get_pos()
        xactive = False
        yactive = False
        if self.rect.left <= mouse_pos[0] <= self.rect.right:
            xactive = True
        if self.rect.top <= mouse_pos[1] <= self.rect.bottom:
            yactive = True
        if xactive is True and yactive is True:
            self.active = True
            self.color = (100, 255, 100)
        else:
            self.active = False
            self.color = (255, 255, 255)

        mouse_buttons = pygame.mouse.get_pressed()
        if self.active is True:
            if self.mouse_state == 1 and mouse_buttons[0] == 0:
                self.action_listener.run(self.command, self.command_param)
        self.mouse_state = mouse_buttons[0]

    def render(self, screen):
        self.check_active()
        text = self.fonts[3].render(self.label, False, self.color)
        self.rect = text.get_rect(center=self.pos)
        screen.blit(text, self.rect)


class HUDText:
    def __init__(self, fonts, text, pos, color=(255, 255, 255)):
        self.fonts = fonts
        self.text = text
        self.pos = pos
        self.color = color

    def render(self, screen, font_size=3, text_var='', override_text=''):
        text = self.text + text_var
        if override_text != '':
            text = override_text

        text = self.fonts[font_size].render(text, False, self.color)
        text_rect = text.get_rect(center=self.pos)
        screen.blit(text, text_rect)


class HUDRect:
    def __init__(self, top_left, bot_right, color, border_width=0):
        self.top_left = top_left
        self.bot_right = bot_right
        self.color = color
        self.border_width = border_width

    def render(self, screen):
        rect = pygame.Rect(self.top_left, self.bot_right)
        pygame.draw.rect(screen, self.color, rect, self.border_width)


def test_hud(fonts, resolution, action_listener):
    hud = HUD()
    zoom_indication = 'Zoom level: '
    hud.elements.append(HUDText(fonts, zoom_indication, [resolution[0]/2, 30]))
    hud.elements.append(HUDButton(fonts, 'Quit', [40, resolution[1] - 40], action_listener, 'quit'))
    hud.elements.append(HUDButton(fonts, 'Pause', [120, resolution[1] - 40], action_listener, 'pause'))
    return hud
