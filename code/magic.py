import pygame
from random import randint
from settings import TILE_SIZE


class Magic:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            "heal": pygame.mixer.Sound("../audio/heal.wav"),
            "flame": pygame.mixer.Sound("../audio/Fire.wav")
        }

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds["flame"].set_volume(0.3)
            self.sounds["flame"].play()
            player.energy -= cost
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILE_SIZE
                    x = player.rect.centerx + offset_x + \
                        randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + \
                        randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles(
                        'flame', (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * TILE_SIZE
                    x = player.rect.centerx + \
                        randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + offset_y + \
                        randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles(
                        'flame', (x, y), groups)

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds["heal"].set_volume(0.3)
            self.sounds["heal"].play()
            player.energy -= cost
            player.health += strength
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            offset = pygame.math.Vector2(0, -75)
            self.animation_player.create_particles(
                'aura', player.rect.center, groups)
            self.animation_player.create_particles(
                'heal', player.rect.center + offset, groups)
