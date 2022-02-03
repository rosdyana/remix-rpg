from turtle import distance
import pygame
from utils import import_folder
from settings import *
from entity import Entity


class Enemy(Entity):
	def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp):
		super().__init__(groups)
		self.sprite_type = "enemy"
		
		# Graphics setup
		self.import_graphics(monster_name)
		self.status = "idle"
		self.image = self.animations[self.status][self.frame_index]

		# Movement
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0, -10)
		self.obstacle_sprites = obstacle_sprites

		# Stats
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']

		# Player interaction
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.add_xp = add_xp

		self.vulnerable = True
		self.hit_time = None
		self.invicibility_time = 300

		self.trigger_death_particles = trigger_death_particles

		# Sounds
		self.death_sound = pygame.mixer.Sound(f"../audio/death.wav")
		self.hit_sound = pygame.mixer.Sound(f"../audio/hit.wav")
		self.death_sound.set_volume(0.2)
		self.hit_sound.set_volume(0.2)
		self.attack_sounds = pygame.mixer.Sound(monster_info['attack_sound'])
		self.attack_sounds.set_volume(0.2)


	def import_graphics(self, monster_name):
		self.animations = {"idle": [], "move": [], "attack": []}
		main_path = f"../graphics/monsters/{monster_name}/"
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = "move"
		else:
			self.status = "idle"

	def get_player_distance_direction(self, player):
		enemy_vector = pygame.math.Vector2(self.rect.center)
		player_vector = pygame.math.Vector2(player.rect.center)
		distance = (player_vector - enemy_vector).magnitude()
		if distance > 0:
			direction = (player_vector - enemy_vector).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance, direction)

	def actions(self, player):
		if self.status == "attack":
			self.attack_sounds.play()
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage, self.attack_type)
		elif self.status == "move":
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		# Flicker effect with red color
		if not self.vulnerable:
			self.image.set_alpha(self.flicker_alpha_value())
		else:
			self.image.set_alpha(255)

	def cooldown(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True
		if not self.vulnerable:
			if current_time - self.hit_time >= self.invicibility_time:
				self.vulnerable = True

	def get_damage(self, player, attack_type):
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == "weapon":
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center, self.monster_name)
			self.add_xp(self.exp)
			self.death_sound.play()

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldown()
		self.check_death()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)