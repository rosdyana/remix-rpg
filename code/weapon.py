import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, style=None):
        super().__init__(groups)
        direction = player.status.split("_")[0]

        # Graphics
        if style != None:
            full_path = f"../graphics/particles/{style}/{style}.png"
        else:
            full_path = f"../graphics/weapons/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        # Placement
        if direction == 'right':
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(0, 15))
        elif direction == 'left':
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(0, 15))
        elif direction == 'up':
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(-15, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(-15, 0))
        else:
            self.rect = self.image.get_rect(center=player.rect.center)
