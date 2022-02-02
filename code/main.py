import pygame, sys
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

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
