import pygame
from camera import Camera
from animation_player import AnimationPlayer
from weapon import Weapon
from settings import *
from tile import Tile
from magic import Magic
from player import Player
from debug import debug
from utils import import_csv_layout, import_folder
from ui import UI
from enemy import Enemy
from random import randint, choice
from upgrade_menu import UpgradeMenu


class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		self.game_paused = False

		# sprite group setup
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.attack_sprites = pygame.sprite.Group()

		self.current_attack = None
		self.current_magic = None

		# sprite setup
		self.create_map()

		self.ui = UI()

		self.upgrade_menu = UpgradeMenu(self.player)

		self.animation_player = AnimationPlayer()
		self.magic = Magic(self.animation_player)

	def create_map(self):
		layouts = {
			"boundary": import_csv_layout("../map/map_FloorBlocks.csv"),
			"grass": import_csv_layout("../map/map_Grass.csv"),
			"object": import_csv_layout("../map/map_Objects.csv"),
			"entities": import_csv_layout("../map/map_Entities.csv"),
		}

		graphics = {
			"grass": import_folder("../graphics/Grass"),
			"object": import_folder("../graphics/Objects"),
		}
		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != "-1":
						x = col_index * TILE_SIZE
						y = row_index * TILE_SIZE
						if style == "boundary":
							Tile(
								(x, y),
								[self.obstacle_sprites],
								"invisible",
							)
						if style == "grass":
							random_grass_image = choice(
								graphics["grass"])
							Tile(
								(x, y),
								[self.visible_sprites, self.obstacle_sprites,
								 self.attackable_sprites],
								"grass",
								random_grass_image,
							)
						if style == "object":
							surface = graphics["object"][int(col)]
							Tile(
								(x, y),
								[self.visible_sprites, self.obstacle_sprites],
								"object",
								surface,
							)
						if style == "entities":
							if col == "394":
								self.player = Player(
									(x, y),
									[self.visible_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic,
									self.destroy_magic
								)
							else:
								if col == "390":
									monster_name = "bamboo"
								elif col == "391":
									monster_name = "spirit"
								elif col == "392":
									monster_name = "raccoon"
								else:
									monster_name = "squid"
								Enemy(
									monster_name,
									(x, y),
									[self.visible_sprites, self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_xp)

	def create_attack(self):
		self.current_attack = Weapon(
			self.player, [self.visible_sprites, self.attack_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def create_magic(self, style, strength, cost):
		if style == "heal":
			self.magic.heal(self.player, cost, strength,
							[self.visible_sprites])
		if style == "flame":
			self.magic.flame(self.player, cost, [
							 self.visible_sprites, self.attack_sprites])

	def destroy_magic(self):
		if self.current_magic:
			self.current_magic.kill()
		self.current_magic = None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(
					attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0, 75)
							for _ in range(randint(3, 6)):
								self.animation_player.create_grass_particles(
									pos - offset, [self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(
								self.player, attack_sprite.sprite_type)

	def damage_player(self, amount, attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(
				attack_type, self.player.rect.center, [self.visible_sprites])

	def trigger_death_particles(self, pos, particle_type):
		self.animation_player.create_particles(
			particle_type, pos, [self.visible_sprites])

	def add_xp(self, amount):
		self.player.exp += amount

	def toggle_menu(self):
		self.game_paused = not self.game_paused

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)

		if self.game_paused:
			self.upgrade_menu.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()
