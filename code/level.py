import pygame
from camera import Camera
from settings import *
from tile import Tile
from player import Player
from debug import debug
from utils import import_csv_layout, import_folder
import random


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("../map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("../map/map_Grass.csv"),
            "object": import_csv_layout("../map/map_Objects.csv"),
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
                            random_grass_image = random.choice(graphics["grass"])
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
        self.player = Player(
            (1950, 1200), [self.visible_sprites], self.obstacle_sprites
        )

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
