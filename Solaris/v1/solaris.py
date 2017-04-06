import pygame
import math

# Global vars
RUNNING = True
game_over = False
win_game = False
BACKGROUND = None
screen = None
ui_text = None
title_text = None
menu_text = None
game_over_text = None
screen_size = [1200, 800]
screen_center = [round(screen_size[0]/2), round(screen_size[1]/2)]
planets_visited = []

player_level = 0
player_planet = None
player_fuel = 100
player_planet_timeout = 0
ORBIT_RADIUS = 70
planets = []
player = None
sim_speed = 40
setting_changed = False
trajectory_indicator_length = 300

GRAVITATIONAL_CONSTANT = 1
SUN_MASS = 1
SUN_RADIUS = 10

menu_screen = True


def main():
    init_game()
    global RUNNING
    game_clock = pygame.time.Clock()
    while RUNNING is True:
        if game_over is True:
            game_over_screen()
        elif menu_screen is True:
            disp_menu()
        elif win_game is True:
            win_game_screen()
        else:
            main_loop()
        window_event_handler()
        # Limit the speed of the game
        game_clock.tick(sim_speed)


def disp_menu():
    play_active, quit_active = menu_event_handler()
    active_color = (150, 255, 150)
    play_color = (255, 255, 255)
    quit_color = (255, 255, 255)
    if play_active is True:
        play_color = active_color
    if quit_active is True:
        quit_color = active_color

    screen.blit(BACKGROUND, (0, 0))
    title = title_text.render('Solaris', False, (255, 255, 255))
    title_rect = title.get_rect(center=(screen_center[0], screen_center[1] - 150))
    play_button = menu_text.render('Play', False, play_color)
    play_rect = play_button.get_rect(center=(screen_center[0], screen_center[1]))
    quit_button = menu_text.render('Quit', False, quit_color)
    quit_rect = quit_button.get_rect(center=(screen_center[0], screen_center[1]+60))
    screen.blit(title, title_rect)
    screen.blit(play_button, play_rect)
    screen.blit(quit_button, quit_rect)
    pygame.display.flip()


def menu_event_handler():
    quit_active = False
    play_active = False
    mouse_pos = pygame.mouse.get_pos()
    # Check if hovering over play button
    if screen_center[0] - 50 < mouse_pos[0] < screen_center[0] + 50:
        if screen_center[1] - 30 < mouse_pos[1] < screen_center[1] + 30:
            play_active = True
    # Check if hovering over quit button
    if screen_center[0] - 50 < mouse_pos[0] < screen_center[0] + 50:
        if screen_center[1]+60 - 30 < mouse_pos[1] < screen_center[1]+60 + 30:
            quit_active = True

    mouse_keys_down = pygame.mouse.get_pressed()
    if mouse_keys_down[0] == 1:
        if quit_active is True:
            global RUNNING
            RUNNING = False
        if play_active is True:
            global menu_screen, player_planet_timeout
            menu_screen = False
            gen_planets()
            player_planet_timeout = 200
    return play_active, quit_active


def init_game():
    global screen_size, screen, BACKGROUND, planets
    # Creat the game screen
    screen = pygame.display.set_mode(screen_size)
    # Set window info
    pygame.display.set_icon(screen)
    pygame.display.set_caption('Aliens')
    pygame.display.flip()
    # Make the background of the game
    BACKGROUND = pygame.Surface(screen.get_size())
    BACKGROUND.fill((0, 0, 0))
    # Init the font module for drawing text
    init_text()


def init_text():
    pygame.font.init()
    global ui_text, game_over_text, menu_text, title_text
    ui_text = pygame.font.SysFont('Arial', 20)
    game_over_text = pygame.font.SysFont('Arial', 100)
    menu_text = pygame.font.SysFont('Arial', 40)
    title_text = pygame.font.SysFont('Arial', 60)


def gen_planets():
    global planets
    planets = []
    planets.append(Planet(1, [135, 108, 67], 5))
    planets.append(Planet(2, [51, 117, 175], 5, True))
    planets.append(Planet(3, [162, 56, 23], 5))
    planets.append(Planet(4, [184, 222, 100], 5))
    planets.append(Planet(5, [200, 200, 255], 5))


def main_loop():
    global planets, player, player_level, player_planet, player_planet_timeout, planets_visited

    # Planet stuff
    for planet in planets:
        planet.tick()
        if planet.is_player is True:
            if planet.level not in planets_visited:
                planets_visited.append(planet.level)
            player_planet = planet
            player_level = planet.level
        # Check for player collision
        if player_planet_timeout > 0:
            player_planet_timeout -= 1
        if player is not None and player_planet_timeout == 0:
            if planet.hit_detect(player.pos) is True:
                player = None
                planet.is_player = True

    # Player stuff
    if player is not None:
        player_level = 0 # Var used to show color of occupied ring
        player.tick()
    render()
    event_handler()
    
    # Win condition check
    if len(planets) == len(planets_visited):
        global win_game
        win_game = True


def render():
    global screen_center, screen, BACKGROUND, planets, player_level, player, player_planet, planets_visited
    screen.blit(BACKGROUND, (0, 0))
    # Draw sun
    pygame.draw.circle(screen, (200, 200, 0), screen_center, SUN_RADIUS)
    # Draw orbital rings
    for i in range(1, 6):
        color = (100, 100, 100)
        if i in planets_visited:
            color = (240, 230, 140)
        if i == player_level:
            color = (100, 200, 100)
        pygame.draw.circle(screen, color, screen_center, ORBIT_RADIUS * i, 1)
    # Render planet stuff
    for planet in planets:
        # Draw planet
        pygame.draw.circle(screen, planet.color, planet.pos, planet.radius)
        # Mouse interaction
        if planet.is_player is True:
            if player is None:
                # Draw line to mouse
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.line(screen, (200, 200, 200), planet.pos, mouse_pos, 1)
                # Draw predicted firing trajectory
                step_pos = [planet.pos[0], planet.pos[1]]
                velx = (mouse_pos[0] - player_planet.pos[0]) * 0.01
                vely = (mouse_pos[1] - player_planet.pos[1]) * 0.01
                vel = [velx, vely]
                for i in range(0, trajectory_indicator_length):
                    pos, vel = next_step(step_pos, vel)
                    if i % 5 == 0:
                        pygame.draw.circle(screen, (255, 255, 255), (round(pos[0]), round(pos[1])), 0)
            else:
                planet.is_player = False

    # Render player
    if player is not None:
        pygame.draw.circle(screen, (100, 255, 100), (round(player.pos[0]), round(player.pos[1])), 2)
        # Render path prediction
        step_pos = [player.pos[0], player.pos[1]]
        vel = [player.velx, player.vely]
        for i in range(0, trajectory_indicator_length):
            pos, vel = next_step(step_pos, vel)
            if i % 5 == 0:
                pygame.draw.circle(screen, (255, 255, 255), (round(pos[0]), round(pos[1])), 0)

    draw_ui()

    # Commit render to screen
    pygame.display.flip()


def draw_ui():
    global screen, sim_speed, planets_visited, player_fuel
    planets_visited_text = ui_text.render('planets visited: ' + str(len(planets_visited)) + ' / ' + str(len(planets)), False, (255, 255, 255))
    screen.blit(planets_visited_text, (5, 0))
    # Sim speed notification
    sim_speed_display = ui_text.render('sim speed: ' + str(sim_speed) + ' (-/=)', False, (255, 255, 255))
    screen.blit(sim_speed_display, (5, 20))
    # Trajectory
    traj_ind_text = ui_text.render('trajectory indicator length: ' + str(trajectory_indicator_length) + ' (9/0)', False, (255, 255, 255))
    screen.blit(traj_ind_text, (5, 40))
    fuel_gauge = ui_text.render('fuel: ' + str(round(player_fuel, 3)) + ' (arrow keys)', False, (255, 255, 255))
    screen.blit(fuel_gauge, (5, 60))


def event_handler():
    keys_down = pygame.key.get_pressed()

    global sim_speed, setting_changed, player, player_planet_timeout, trajectory_indicator_length, player_fuel
    # Reset settings chang toggle
    all_keys_rest = True
    for key in keys_down:
        if key == 1:
            all_keys_rest = False
            break
    if all_keys_rest is True:
        setting_changed = False

    # Sim Speed
    if keys_down[pygame.K_EQUALS] == 1:
        if setting_changed is False:
            sim_speed += 20
            setting_changed = True
    if keys_down[pygame.K_MINUS] == 1:
        if setting_changed is False:
            sim_speed -= 20
            setting_changed = True
    if sim_speed < 20:
        sim_speed = 20
    if sim_speed > 400:
        sim_speed = 400

    # Trajectory indicator
    if keys_down[pygame.K_0] == 1:
        if setting_changed is False:
            trajectory_indicator_length += 50
            setting_changed = True
    elif keys_down[pygame.K_9] == 1:
        if setting_changed is False:
            trajectory_indicator_length -= 50
            setting_changed = True

    if trajectory_indicator_length < 0:
        trajectory_indicator_length = 0

    # Player movement
    if player is not None and player_fuel > 0:
        fuel_used = False
        if keys_down[pygame.K_LEFT] == 1:
            player.velx -= 0.01
            fuel_used = True
        if keys_down[pygame.K_RIGHT] == 1:
            player.velx += 0.01
            fuel_used = True
        if keys_down[pygame.K_UP] == 1:
            player.vely -= 0.01
            fuel_used = True
        if keys_down[pygame.K_DOWN] == 1:
            player.vely += 0.01
            fuel_used = True
        if fuel_used is True:
            player_fuel -= 0.1

    # Mouse keys
    mouse_keys_down = pygame.mouse.get_pressed()
    # Spawn player
    if mouse_keys_down[0] == 1:
        if player is None and player_planet_timeout == 0:
            mouse_pos = pygame.mouse.get_pos()
            velx = (mouse_pos[0] - player_planet.pos[0])*0.01
            vely = (mouse_pos[1] - player_planet.pos[1])*0.01
            player = Player(player_planet, player_planet.pos, velx, vely)
            player_planet_timeout = 500


def window_event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global RUNNING
            RUNNING = False
            return


class Planet:
    def __init__(self, level, color, radius, is_player=False, mass=0.5):
        self.level = level
        self.radius = radius
        self.counter = 0
        self.color = color
        self.xoffset = ORBIT_RADIUS * level
        self.yoffset = 0
        self.pos = []
        self.is_player = is_player
        self.mass = mass
        self.visited = False

    def tick(self):
        self.counter += 1
        self.xoffset = round(math.cos(self.counter/(100*self.level)) * ORBIT_RADIUS * self.level)
        self.yoffset = -round(math.sin(self.counter/(100*self.level)) * ORBIT_RADIUS * self.level)
        self.pos = [screen_center[0] + self.xoffset, screen_center[1] + self.yoffset]
        if self.is_player:
            self.visited = True
        # if player is not None and player_planet_timeout == 0:
        #     self.apply_player_gravity()

    def hit_detect(self, pos):
        hit_x = False
        hit_y = False
        if self.pos[0] - self.radius < pos[0] < self.pos[0] + self.radius:
            hit_x = True
        if self.pos[1] - self.radius < pos[1] < self.pos[1] + self.radius:
            hit_y = True
        if hit_x is True and hit_y is True:
            return True
        else:
            return False


class Player:
    def __init__(self, home_planet, pos, velx, vely):
        self.home_planet = home_planet
        self.pos = pos
        self.velx = velx
        self.vely = vely

    def tick(self):
        self.check_sun_collision()
        # Calc gravitational acceleration
        dist_x = abs(screen_center[0] - self.pos[0])
        dist_y = abs(screen_center[1] - self.pos[1])
        linear_dist = math.sqrt(dist_x**2 + dist_y**2)
        dist_x_normalized = dist_x / linear_dist
        dist_y_normalized = dist_y / linear_dist
        grav_force = GRAVITATIONAL_CONSTANT*(SUN_MASS/linear_dist)
        x_grav_force = grav_force * dist_x_normalized
        y_grav_force = grav_force * dist_y_normalized
        if self.pos[0] > screen_center[0]:
            x_grav_force = x_grav_force * -1
        if self.pos[1] > screen_center[1]:
            y_grav_force = y_grav_force * -1
        self.velx += x_grav_force
        self.vely += y_grav_force
        self.pos[0] += self.velx
        self.pos[1] += self.vely

    def check_sun_collision(self):
        dist_x = abs(screen_center[0] - self.pos[0])
        dist_y = abs(screen_center[1] - self.pos[1])
        linear_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if linear_dist <= SUN_RADIUS*2:
            global game_over
            game_over = True


def next_step(step_pos, vel):
    # Calc gravitational acceleration
    dist_x = abs(screen_center[0] - step_pos[0])
    dist_y = abs(screen_center[1] - step_pos[1])
    linear_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
    dist_x_normalized = dist_x / linear_dist
    dist_y_normalized = dist_y / linear_dist
    grav_force = GRAVITATIONAL_CONSTANT * (SUN_MASS / linear_dist)
    x_grav_force = grav_force * dist_x_normalized
    y_grav_force = grav_force * dist_y_normalized
    if step_pos[0] > screen_center[0]:
        x_grav_force = x_grav_force * -1
    if step_pos[1] > screen_center[1]:
        y_grav_force = y_grav_force * -1
    vel[0] += x_grav_force
    vel[1] += y_grav_force
    step_pos[0] += vel[0]
    step_pos[1] += vel[1]
    return step_pos, vel


def game_over_screen():
    window_event_handler()
    global screen
    game_over_splash = game_over_text.render('GAME OVER', False, (255, 255, 255))
    game_over_rect = game_over_splash.get_rect(center=(screen_center[0], screen_center[1]))
    screen.blit(game_over_splash, game_over_rect)
    pygame.display.flip()
    

def win_game_screen():
    window_event_handler()
    global screen
    game_win_splash = game_over_text.render('YOU WIN!', False, (255, 255, 255))
    game_win_rect = game_win_splash.get_rect(center=(screen_center[0], screen_center[1]))
    screen.blit(game_win_splash, game_win_rect)
    pygame.display.flip()

if __name__ == '__main__':
    main()
