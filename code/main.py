import pygame
import sys
from settings import WATER_COLOR
from level import Level
from settings import WIDTH, HEIGHT, TITLE, DESCRIPTION, VERSION, FPS


class Game:
    def __init__(self) -> None:
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"{TITLE} - {DESCRIPTION} {VERSION}")
        self.clock = pygame.time.Clock()
        self.level = Level()
        bg_sound = pygame.mixer.Sound("../audio/main.ogg")
        bg_sound.set_volume(0.4)
        bg_sound.play(-1)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
