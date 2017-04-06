import pygame


class Menu:
    def __init__(self, fonts, elements, title, title_pos, context=None, context_pos=None):
        self.fonts = fonts
        self.elements = elements
        self.title = title
        self.title_pos = title_pos
        self.background = None
        self.context = context
        self.context_pos = context_pos

    def render(self, screen):
        # Render title
        if self.background is None:
            self.background = pygame.Surface(screen.get_size())
            self.background.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        title = self.fonts[7].render(self.title, False, (255, 255, 255))
        title_rect = title.get_rect(center=self.title_pos)
        screen.blit(title, title_rect)

        # Render context
        if self.context is not None:
            context = self.fonts[2].render(self.context, False, (255, 255, 255))
            context_rect = context.get_rect(center=self.context_pos)
            screen.blit(context, context_rect)

        # Render buttons
        for elements in self.elements:
            elements.render(screen)


class MenuButton:
    def __init__(self, fonts, label, pos, action_listener, command, command_parm=None):
        self.fonts = fonts
        self.label = label
        self.pos = pos
        self.rect = None
        self.color = (255, 255, 255)
        self.active = False
        self.action_listener = action_listener
        self.command = command
        self.mouse_state = 0
        self.command_param = command_parm

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


class MenuText:
    def __init__(self, font, text, color, pos):
        self.font = font
        self.text = text
        self.color = color
        self.pos = pos

    def render(self, screen):
        text = self.font.render(self.text, False, self.color)
        text_rect = text.get_rect(center=self.pos)
        screen.blit(text, text_rect)


def main_menu(fonts, resolution, action_listener):
    centerx = resolution[0]/2
    centery = resolution[1]/2
    play_button = MenuButton(fonts, 'Play', [centerx, centery - 40], action_listener, 'play')
    options_button = MenuButton(fonts, 'Options', [centerx, centery], action_listener, 'options')
    quit_button = MenuButton(fonts, 'Quit', [centerx, centery + 40], action_listener, 'quit')
    buttons = [play_button, options_button, quit_button]
    menu = Menu(fonts, buttons, 'Solaris', [centerx, centery - 120])
    return menu


def options_menu(fonts, resolution, action_listener):
    centerx = resolution[0] / 2
    centery = resolution[1] / 2
    opt1 = MenuButton(fonts, 'Resolution', [centerx, centery - 40], action_listener, 'resolution')
    opt2 = MenuButton(fonts, 'Placeholder', [centerx, centery], action_listener, 'something')
    mmb = MenuButton(fonts, 'Main Menu', [centerx, centery + 40], action_listener, 'mainmenu')
    buttons = [opt1, opt2, mmb]
    menu = Menu(fonts, buttons, 'Options', [centerx, centery - 200])
    return menu


def resolution_menu(fonts, resolution, action_listener):
    centerx = resolution[0] / 2
    centery = resolution[1] / 2
    res1 = MenuButton(fonts, '800x600', [centerx, centery - 80], action_listener, 'changeres', [800, 600])
    res2 = MenuButton(fonts, '1200x800', [centerx, centery - 40], action_listener, 'changeres', [1200, 800])
    res3 = MenuButton(fonts, '1600x1200', [centerx, centery], action_listener, 'changeres', [1600, 1200])
    res4 = MenuButton(fonts, '1920x1080', [centerx, centery + 40], action_listener, 'changeres', [1920, 1080])
    mmb = MenuButton(fonts, 'Back', [centerx, centery + 80], action_listener, 'options')
    buttons = [res1, res2, res3, res4, mmb]
    context = 'Resolutions over 1200x800 tend to be unstable. Resolutions can be changed manually in config.txt'
    menu = Menu(fonts, buttons, 'Resolution', [centerx, centery - 200], context, [centerx, centery + 150])
    return menu


def confirm_res_change(fonts, resolution, action_listener):
    centerx = resolution[0] / 2
    centery = resolution[1] / 2
    yes_button = MenuButton(fonts, 'Confirm', [centerx, centery - 20], action_listener, 'quit')
    no_button = MenuButton(fonts, 'Back', [centerx, centery + 20], action_listener, 'options')
    buttons=[yes_button, no_button]
    context_text = 'Changing resolution requires restart. Exit now?'
    menu = Menu(fonts, buttons, 'Resolution', [centerx, centery - 200], context_text, [centerx, centery - 100])
    return menu


def pause_menu(fonts, resolution, action_listener):
    centerx = resolution[0] / 2
    centery = resolution[1] / 2
    return_button = MenuButton(fonts, 'Return to game', [centerx, centery - 80], action_listener, 'play')
    new_sys = MenuButton(fonts, 'Generate new system', [centerx, centery], action_listener, 'gensystem')
    mmb = MenuButton(fonts, 'Return to menu', [centerx, centery + 40], action_listener, 'mainmenu')
    controls_button = MenuButton(fonts, 'Controls', [centerx, centery - 40], action_listener, 'controls')
    buttons = [return_button, mmb, new_sys, controls_button]
    menu = Menu(fonts, buttons, 'Pause', [centerx, centery - 200])
    return menu


def controls_menu(fonts, resolution, action_listener):
    centerx = resolution[0] / 2
    centery = resolution[1] / 2
    return_button = MenuButton(fonts, 'Back', [centerx, centery - 100], action_listener, 'pause')
    zoom_in_text = MenuText(fonts[3], '>    Zoom in', (255, 255, 255), [centerx, centery + 40])
    zoom_out_text = MenuText(fonts[3], '<    Zoom out', (255, 255, 255), [centerx, centery])
    launch_text = MenuText(fonts[3], 'space    launch', (255, 255, 255), [centerx, centery - 40])
    arrow_keys_text = MenuText(fonts[3], 'arrow keys    move player', (255, 255, 255), [centerx, centery + 80])
    elements = [return_button, zoom_in_text, zoom_out_text, launch_text, arrow_keys_text]
    menu = Menu(fonts, elements, 'Controls', [centerx, centery - 200])
    return menu