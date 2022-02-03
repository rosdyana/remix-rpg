from click import style
import pygame
import pygame.math
from pygame.math import Vector2
from entity import Entity
from utils import import_folder
from settings import weapon_data, magic_data


class Player(Entity):
	def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, destroy_magic):
		super().__init__(groups)
		self.image = pygame.image.load(
			"../graphics/test/player.png").convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0, -30)
		self.obstacle_sprites = obstacle_sprites

		# graphics setup
		self.import_player_assets()
		self.status = "down"

		# Movement attributes
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		# Weapon attributes
		self.create_attack = create_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.destroy_attack = destroy_attack
		self.can_switch_weapon = True
		self.weapon_switch_time = 0
		self.switch_duration_cooldown = 200

		# Magic attributes
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None
		self.create_magic = create_magic
		self.destroy_magic = destroy_magic

		# Stats
		self.stats = {
			"health": 100,
			"energy": 50,
			"energy_recovery": 0.05,
			"attack": 10,
			"magic": 4,
			"speed": 5,
		}

		self.health = self.stats["health"]
		self.energy = self.stats["energy"]
		self.exp = 0
		self.speed = self.stats["speed"]

		self.vulnerable =True
		self.hurt_time = None
		self.Invurnebility_duration = 500

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
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[
					self.magic_index]['strength']
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style, strength, cost)

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()

				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0

				self.weapon = list(weapon_data.keys())[self.weapon_index]

			if keys[pygame.K_w] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()

				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0

				self.magic = list(magic_data.keys())[self.magic_index]

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time > self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
				self.attacking = False
				self.destroy_attack()
				self.destroy_magic()

		if not self.can_switch_weapon:
			if (current_time - self.weapon_switch_time >= self.switch_duration_cooldown):
				self.can_switch_weapon = True

		if not self.can_switch_magic:
			if (current_time - self.magic_switch_time >= self.switch_duration_cooldown):
				self.can_switch_magic = True

		if not self.vulnerable:
			if current_time - self.hurt_time > self.Invurnebility_duration:
				self.vulnerable = True
			

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

	def get_full_weapon_damage(self):
		return self.stats["attack"] + weapon_data[self.weapon]["damage"]

	def get_full_magic_damage(self):
		return self.stats["magic"] + magic_data[self.magic]["strength"]

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center=self.hitbox.center)

		# Flicker effect
		if not self.vulnerable:
			self.image.set_alpha(self.flicker_alpha_value())
		else:
			self.image.set_alpha(255)

	def energy_recovery(self):
		if self.energy < self.stats["energy"]:
			self.energy += self.stats["energy_recovery"]
		else:
			self.energy = self.stats["energy"]
		

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.energy_recovery()
