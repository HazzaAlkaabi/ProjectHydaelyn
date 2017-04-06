import pygame
import settings
import Menu
import Bodies
import HUD
import Utils

running = True
screen = None

fonts = []
current_menu = None
display_menu = True
current_hud = None
action_listener = None
resolution = None
key_limiter = False

star_systems = []
nearest_system = None
player = None
camera = None
launch = False


def main():
    init()
    loop()


def init():
    global screen, fonts, resolution, camera
    resx, resy = settings.get_resolution()
    resolution = [resx, resy]
    # Create camera
    camera = Camera([0, 0], 1, resolution)
    # Create the game screen
    screen = pygame.display.set_mode(resolution)
    # Set window info
    pygame.display.set_icon(screen)
    pygame.display.set_caption('Solaris')
    # Generate fonts
    pygame.font.init()
    for i in range(0, 10):
        fonts.append(pygame.font.SysFont('Arial', i*10))
    # Make the main menu
    global action_listener
    action_listener = ActionListener()
    global current_menu
    current_menu = Menu.main_menu(fonts, resolution, action_listener)

    global star_systems, nearest_system
    star_systems = Bodies.generate_systems(10, action_listener)
    nearest_system = star_systems[0]

    global player
    player = Bodies.Player([500, 500], (255, 100, 100), 3, [0, 0], action_listener)

    global current_hud
    current_hud = HUD.test_hud(fonts, resolution, action_listener)


def loop():
    game_clock = pygame.time.Clock()
    while running is True:
        game_clock.tick(60)
        window_event_handler()
        if display_menu is True:
            current_menu.render(screen)
            pygame.display.flip()
        else:
            update()
            render()


# Update game logic
def update():
    key_listener()
    global nearest_system, star_systems, player

    for star in star_systems:
        star.update(player)

    if player is not None:
        # Find nearest star
        current_dist = Utils.get_distance(nearest_system.pos, player.pos)
        for star in star_systems:
            star.update(player)
            if Utils.get_distance(star.pos, player.pos) < current_dist:
                nearest_system = star
        # Apply gravity from nearest system
        nearest_system.trajectory_predict(0, player.pos, player.vel)

        player.update()
        player.predict_trajectory(nearest_system, 500)


# Draw elements to the screen
def render():

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for star in star_systems:
        star.render(screen, camera)

    if player is not None:
        player.render(screen, camera)

    current_hud.elements[0].text = 'Zoom level: ' + str(round(camera.zoom, 2))
    current_hud.render(screen)

    pygame.display.flip()


# Listen for key presses during the game
def key_listener():
    global key_limiter, display_menu, current_menu
    keys_down = pygame.key.get_pressed()
    all_inactive = True
    for key in keys_down:
        if key == 1:
            all_inactive = False
            break
    if all_inactive is True:
        key_limiter = False

    # Pause the game
    if keys_down[pygame.K_ESCAPE] == 1:
        if key_limiter is False:
            key_limiter = True
            action_listener.run('pause')

    # Control the player
    global player
    if player is not None:
        if keys_down[pygame.K_UP] == 1:
            player.vel[1] -= player.speed
        if keys_down[pygame.K_DOWN] == 1:
            player.vel[1] += player.speed
        if keys_down[pygame.K_LEFT] == 1:
            player.vel[0] -= player.speed
        if keys_down[pygame.K_RIGHT] == 1:
            player.vel[0] += player.speed

    # Launch the player
    if player is None:
        global launch
        if keys_down[pygame.K_SPACE] == 1:
            launch = True
        else:
            launch = False

    # Change camera zoom
    global camera
    if keys_down[pygame.K_PERIOD]:
        camera.change_zoom(True)
    if keys_down[pygame.K_COMMA]:
        camera.change_zoom(False)


# Allows objects outside this module to run commands
class ActionListener:
    def __init__(self):
        self.command = ''

    def run(self, command, params=None):
        global current_menu, display_menu, running, player, camera, current_hud, launch, star_systems
        if command == 'play':
            display_menu = False
        elif command == 'quit':
            running = False
        elif command == 'options':
            current_menu = Menu.options_menu(fonts, resolution, action_listener)
        elif command == 'mainmenu':
            current_menu = Menu.main_menu(fonts, resolution, action_listener)
        elif command == 'resolution':
            current_menu = Menu.resolution_menu(fonts, resolution, action_listener)
        elif command == 'changeres':
            param = params[0]
            settings.set_resolution(param)
            current_menu = Menu.confirm_res_change(fonts, resolution, action_listener)
        elif command == 'pause':
            display_menu = True
            current_menu = Menu.pause_menu(fonts, resolution, action_listener)
        elif command == 'controls':
            display_menu = True
            current_menu = Menu.controls_menu(fonts, resolution, action_listener)
        elif command == 'deleteplayer':
            player = None
        elif command == 'spawnplayer':
            player = Bodies.Player(params[0], params[1], params[2], params[3], action_listener)
        elif command == 'gensystem':
            star_systems = Bodies.generate_systems(10, action_listener)
            player = Bodies.Player([500, 500], (255, 100, 100), 3, [0, 0], action_listener)
            camera = Camera([0, 0], 1, resolution)
            display_menu = False
        elif command == 'camerafollow':
            camera.pos = [(params[0][0] - resolution[0]/2), (params[0][1] - resolution[1]/2)]
        elif command == 'launchplayer':
            if launch is True:
                planet = params[0]
                mouse_pos = pygame.mouse.get_pos()
                pos = [planet.pos[0], planet.pos[1]]
                direction = Utils.normalize([mouse_pos[0] - resolution[0]/2, mouse_pos[1] - resolution[1]/2])
                player = Bodies.Player(pos, (255, 100, 100), 3, direction, action_listener)
                planet.is_player = False
                launch = False


class Camera:
    def __init__(self, pos, zoom, res):
        self.pos = pos
        self.zoom = zoom
        self.resolution = res

    def pos_to_camera(self, pos):
        new_x = round(((pos[0] - self.pos[0]) * self.zoom) + (self.resolution[0]/2) * (1 - self.zoom))
        new_y = round(((pos[1] - self.pos[1]) * self.zoom) + (self.resolution[1]/2) * (1 - self.zoom))
        new_pos = [new_x, new_y]
        return new_pos

    def change_zoom(self, positive):
        step = 0.05 * self.zoom
        if positive is True:
            self.zoom += step
        else:
            self.zoom -= step
        if self.zoom < 0.01:
            self.zoom = 0.01


def window_event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            return





if __name__ == '__main__':
    main()
