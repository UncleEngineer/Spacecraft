import pygame, math, sys
pygame.init()

class Planet:
    def __init__(self, x, y, orbit_to = None, orbit_speed = None):
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.orbit_to = orbit_to
        self.orbit_speed = orbit_speed
        if self.orbit_to and self.orbit_speed:
            self.radius = self.pos.distance_to(self.orbit_to.pos)
            self.theta = self.pos.angle_to(self.orbit_to.pos)

    def update(self):
        if self.orbit_to and self.orbit_speed:
            # this code use 삼각함수 to get next x and y position of circle movement
            x = self.radius * math.cos(self.theta) + self.orbit_to.pos.x
            y = self.radius * math.sin(self.theta) + self.orbit_to.pos.y
            # have to change theta (angle of trangle to orbit planet)
            self.theta = (self.theta + self.orbit_speed) % 360
            self.rect.centerx, self.rect.centery = (x, y)
            print(self.theta, self.rect.centerx, self.rect.centery)

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

earth = Planet(500, 500)
moon = Planet(400, 500, earth, 1)

while True:
    dt = clock.tick(1) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    moon.update()

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), moon.rect)
    pygame.display.flip()
