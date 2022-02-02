import pygame

from settings import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, pos, groups, sprite_type, surface=pygame.Surface(
            (TILE_SIZE, TILE_SIZE))
    ) -> None:
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == "object":
            self.rect = self.image.get_rect(
                topleft=(pos[0], pos[1] - TILE_SIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
