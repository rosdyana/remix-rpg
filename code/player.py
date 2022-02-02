import pygame
import pygame.math
from pygame.sprite import Sprite
from pygame.math import Vector2

from utils import import_folder
from settings import weapon_data


class Player(Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load(
            "../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -30)

        # graphics setup
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement attribute
        self.direction = Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Weapon attribute
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = 0
        self.switch_duration_cooldown = 200

        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.stats = {
            "health": 100,
            "energy": 50,
            "attack": 10,
            "magic": 4,
            "speed": 5,
        }

        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 1
        self.speed = self.stats["speed"]

    def import_player_assets(self):
        character_path = "../graphics/player"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_attack": [],
            "left_attack": [],
            "up_attack": [],
            "down_attack": [],
        }

        for animation in self.animations.keys():
            full_path = character_path + "/" + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            # Movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            # Attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # Spell input
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time > self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

            if not self.can_switch_weapon:
                if (
                        current_time - self.weapon_switch_time
                        >= self.switch_duration_cooldown
                ):
                    self.can_switch_weapon = True

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
