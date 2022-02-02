import pygame
import pygame.math
from pygame.sprite import Sprite
from pygame.math import Vector2

class Player(Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction = 0


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move(self.speed)
