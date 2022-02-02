import pygame
from camera import Camera
from weapon import Weapon
from settings import *
from tile import Tile
from player import Player
from debug import debug
from utils import import_csv_layout, import_folder
from ui import UI
from enemy import Enemy
import random


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.current_magic = None

        # sprite setup
        self.create_map()

        self.ui = UI()

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
                            random_grass_image = random.choice(
                                graphics["grass"])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
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
                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites], self.obstacle_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        self.current_magic = Weapon(self.player, [self.visible_sprites], style)

    def destroy_magic(self):
        if self.current_magic:
            self.current_magic.kill()
        self.current_magic = None

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        self.visible_sprites.enemy_update(self.player)
