import pygame
import math
from random import randint
import Utils


class Body:
    def __init__(self, radius, color, action_listener=None, gravity=1, has_player_gravity=False, parent=None, orbit_radius=0, pos=None, is_player=False, counter=0):
        self.pos = pos
        if pos is None:
            self.pos = [0, 0]
        self.radius = radius
        self.color = color
        self.has_gravity = has_player_gravity
        self.gravity = gravity
        self.parent = parent
        self.orbit_radius = orbit_radius
        self.counter = counter
        self.children = []
        self.is_player = is_player
        self.action_listener = action_listener

    def tick_pos(self, counter):
        xoffset = self.orbit_radius * math.cos(counter)
        yoffset = -self.orbit_radius * math.sin(counter)
        new_pos = [self.parent.pos[0] + xoffset, self.parent.pos[1] + yoffset]
        return new_pos

    def update(self, player):

        if self.is_player is True:
            # Follow with camera
            self.action_listener.run('camerafollow', [self.pos])
            # Launch player
            self.action_listener.run('launchplayer', [self])

        # Run child code
        for child in self.children:
            child.update(player)

        # Hit detect for the player
        if player is not None:
            if self.action_listener is not None and self.hit_detect(player.pos) is True and player.interaction_timeout == 0:
                self.is_player = True
                self.action_listener.run('deleteplayer')

        # Orbit parent
        if self.parent is not None:
            self.counter += self.parent.gravity / (self.orbit_radius ** 2)
            self.pos = self.tick_pos(self.counter)

    # Calculate position and gravity on an object in the future
    def trajectory_predict(self, ticks_in_future, obj_pos, obj_vel):

        if self.has_gravity is True:
            if self.parent is None:
                self.apply_gravity(self.pos, obj_pos, obj_vel)
            else:
                counter = self.counter + (self.parent.gravity / (self.orbit_radius ** 2)) * ticks_in_future
                pos = self.tick_pos(counter)
                self.apply_gravity(pos, obj_pos, obj_vel)

        for child in self.children:
            child.trajectory_predict(ticks_in_future, obj_pos, obj_vel)

    def hit_detect(self, obj_pos):
        dist_x = abs(self.pos[0] - obj_pos[0])
        dist_y = abs(self.pos[1] - obj_pos[1])
        linear_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if linear_dist <= self.radius:
            return True

    def apply_gravity(self, self_pos, obj_pos, obj_vel):
        dist_x = abs(self_pos[0] - obj_pos[0])
        dist_y = abs(self_pos[1] - obj_pos[1])
        linear_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if linear_dist == 0:
            linear_dist = 1
        dist_x_normalized = dist_x / linear_dist
        dist_y_normalized = dist_y / linear_dist
        grav_force = self.gravity * (1 / (linear_dist**2))
        x_grav_force = grav_force * dist_x_normalized
        y_grav_force = grav_force * dist_y_normalized
        if obj_pos[0] > self_pos[0]:
            x_grav_force *= -1
        if obj_pos[1] > self_pos[1]:
            y_grav_force *= -1
        obj_vel[0] += x_grav_force
        obj_vel[1] += y_grav_force

    def render(self, screen, camera):
        # Draw orbit path
        if self.parent is not None and self.orbit_radius > 0:
            parent_pos = camera.pos_to_camera(self.parent.pos)
            size = round(self.orbit_radius * camera.zoom)
            if size > 1:
                pygame.draw.circle(screen, (100, 100, 100), parent_pos, size, 1)

        # Draw body
        pos = camera.pos_to_camera(self.pos)
        size = round(self.radius * camera.zoom)
        # Check if the body is on screen
        if -size <= pos[0] <= camera.resolution[0] + size and -size <= pos[1] <= camera.resolution[1] + size:
            pygame.draw.circle(screen, self.color, pos, size)

        # Render children
        for child in self.children:
            child.render(screen, camera)

        if self.is_player is True:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 100, 100), pos, mouse_pos, 1)


class Player:
    def __init__(self, pos, color, radius, vel, action_listener):
        self.pos = pos
        self.color = color
        self.radius = radius
        if vel is None:
            vel = [0, 0]
        self.vel = vel
        self.speed = 0.01
        self.trail = []
        self.trajectory_markers = []
        self.action_listener = action_listener
        self.interaction_timeout = 200

    def update(self):
        if self.interaction_timeout > 0:
            self.interaction_timeout -= 1

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.make_trail()
        if len(self.trail) > 1000:
            self.trail.pop(0)

    def render(self, screen, camera):
        color = self.color
        if self.interaction_timeout > 0:
            color = (255, 255, 255)

        for body in self.trail:
            body.render(screen, camera)

        for body in self.trajectory_markers:
            body.render(screen, camera)

        pos = camera.pos_to_camera(self.pos)
        size = round(self.radius * camera.zoom)
        pygame.draw.circle(screen, color, pos, size)
        self.action_listener.run('camerafollow', [self.pos])

    def make_trail(self):
        pos = [self.pos[0], self.pos[1]]
        self.trail.append(Body(0, (100, 100, 100), None, 0, False, None, 0, pos))

    def predict_trajectory(self, host_body, ticks):
        self.trajectory_markers = []
        obj_pos = [self.pos[0], self.pos[1]]
        obj_vel = [self.vel[0], self.vel[1]]
        for i in range(1, ticks):
            host_body.trajectory_predict(i, obj_pos, obj_vel)
            obj_pos[0] += obj_vel[0]
            obj_pos[1] += obj_vel[1]
            if i % 5 == 0:
                pos = [obj_pos[0], obj_pos[1]]
                self.trajectory_markers.append(Body(0, (100, 100, 100), None, 0, False, None, 0, pos))
    
    
def generate_system(pos, action_listener):
    # Make star
    star_size = randint(30, 100)
    star = Body(star_size, random_color(), action_listener, star_size * 10, True, None, 0, pos)

    # Make planets
    num_planets = randint(3, 10)
    for i in range(1, num_planets):
        planet_size = randint(5, 20)
        new_planet = Body(planet_size, random_color(), action_listener, planet_size * 8, True, star, i * randint(200, 400), None, False, randint(0, 100))
        star.children.append(new_planet)

        # Make Moons
        num_moons = randint(0, 5)
        for j in range(1, num_moons):
            moon_size = randint(2, 5)
            new_moon = Body(moon_size, random_color(), action_listener, 1, False, new_planet, j * randint(20, 30), None, False, randint(0, 100))
            new_planet.children.append(new_moon)
    return star


def generate_systems(number, action_listener):
    # Make a several systems that are spaced apart from each other
    stars = [generate_system([0, 0], action_listener)]
    counter = 0
    while len(stars) < number:
        counter += 1
        star = generate_system([randint(-4000 * counter, 4000 * counter), randint(-4000 * counter, 4000 * counter)], action_listener)
        too_close = False
        for existing_star in stars:
            if Utils.get_distance(existing_star.pos, star.pos) < 3000:
                too_close = True
        if too_close is False:
            stars.append(star)
    return stars
    
    
def random_color():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return color
