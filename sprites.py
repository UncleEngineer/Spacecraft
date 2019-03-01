import pygame, math
from settings import *
import random

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # you can do this in python 3
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(game.player_img, (50, 40))
        # this ori_img is for the rotate rendering if i directly change image from rotated image something weird happen
        self.ori_img = self.image
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        self.rot = 0

    def get_keys(self):
        self.rot_speed = 0
        # 마찰력
        self.vel *= 0.998
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rot_speed = ROT_SPEED
        if keys[pygame.K_RIGHT]:
            self.rot_speed = -ROT_SPEED
        if keys[pygame.K_UP]:
            max = pygame.math.Vector2(MAX_SPEED, 0).rotate(-self.rot-90)
            if self.vel.length() > max.length() :
                self.vel.scale_to_length(MAX_SPEED)
            else:
                self.vel += pygame.math.Vector2(ACC, 0).rotate(-self.rot-90)
            #self.vel += pygame.math.Vector2(ACC, 0).rotate(-self.rot-90)
        if keys[pygame.K_DOWN]:
            self.vel += pygame.math.Vector2(-ACC / 3, 0).rotate(-self.rot-90)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotozoom(self.ori_img, self.rot, 1)
        self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # i was tried to making player always keep in screen
        # but this code is bug somehow player stuck in edge of screen
        '''
        if self.rect.centerx > self.game.map.width:
            self.rect.centerx = 0
        elif  self.rect.centery > self.game.map.height:
            self.rect.centery = 0
        elif  self.rect.centerx < 0:
            self.rect.centerx = self.game.map.width
        elif  self.rect.centery < 0:
            self.rect.centery = self.game.map.height
        '''

class Planet(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y, rot_speed, width, height, orbit_to = None, orbit_speed = None):
        # too much things to optimize here..
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pygame.transform.scale(image, (width, height))
        self.ori_img = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.rot = 0
        self.rot_speed = rot_speed
        self.pos = pygame.math.Vector2(x, y)
        self.orbit_to = orbit_to
        self.orbit_speed = orbit_speed
        if self.orbit_to and self.orbit_speed:
            self.radius = self.pos.distance_to(self.orbit_to.pos)
            self.theta = self.pos.angle_to(self.orbit_to.pos)

    def update(self):
        self.ori_rect = self.rect
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.ori_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.ori_rect.center
        if self.orbit_to and self.orbit_speed:
            # this code is seriously hard to understand
            # this code use 삼각함수 to get next position of circle movement
            x = self.radius * math.cos(self.theta) + self.orbit_to.rect.centerx
            y = self.radius * math.sin(self.theta) + self.orbit_to.rect.centery
            self.rect.centerx = x
            self.rect.centery = y
            # have to change theta (angle of trangle to orbit planet)
            self.theta = (self.theta + self.orbit_speed * self.game.dt) % 360


        # by the way there is one little annoying bug at almost after 360 of orbit image just rollback... idk why..
