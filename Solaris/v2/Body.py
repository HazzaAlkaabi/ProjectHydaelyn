import pygame


class Body:
    def __init__(self, radius, color, pos, parent=None, orbit_radius=0):
        self.radius = radius
        self.color = color
        self.pos = pos
        self.parent = parent
        self.counter = 0
        self.orbit_radius = orbit_radius

    def tick(self):
        self.counter += 1
        if self.parent is not None:
            pass

    def render(self, SCREEN):
        pygame.draw.circle(SCREEN, self.color, (round(self.pos[0]), round(self.pos[1])), self.radius)
