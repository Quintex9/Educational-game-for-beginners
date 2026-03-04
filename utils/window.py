import pygame
from utils.settings import set_level_size
from utils.paths import resource_path


class Window:
    def __init__(self, background_path: str | None = None):
        self.background_path = background_path

        # pevne zobrazenie (bez moznosti resize)
        rozmery = set_level_size(0)
        self.width = rozmery["SCREEN_WIDTH"]
        self.height = rozmery["SCREEN_HEIGHT"]
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.background = None
        if self.background_path:
            self.load_background()

    def load_background(self):
        if not self.background_path:
            self.background = None
            return
        bg = pygame.image.load(resource_path(self.background_path))
        self.background = pygame.transform.scale(bg, (self.width, self.height))

    def draw_background(self, color=None):
        if color:
            self.screen.fill(color)
        elif self.background:
            self.screen.blit(self.background, (0, 0))
