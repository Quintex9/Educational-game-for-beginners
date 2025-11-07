import pygame
from settings import set_level_size, FULLSCREEN, SCALE
class Window:
    def __init__(self, background_path: str | None = None):
        self.fullscreen = FULLSCREEN
        self.scale = SCALE
        self.background_path = background_path

        # zistenie rozmerov
        rozmery = set_level_size(0, fullscreen=self.fullscreen, scale=self.scale)
        self.width = rozmery["SCREEN_WIDTH"]
        self.height = rozmery["SCREEN_HEIGHT"]

        # režim zobrazenia
        self.mode = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.width, self.height), self.mode)

        # pozadie
        self.background = None
        if self.background_path:
            self.load_background()

    def load_background(self):
        #Načíta pozadie a prispôsobí ho aktuálnym rozmerom.
        if not self.background_path:
            self.background = None
            return
        bg = pygame.image.load(self.background_path)
        self.background = pygame.transform.scale(bg, (self.width, self.height))

    def resize(self, new_width, new_height):
        #Reaguje na zmenu veľkosti (pri maximalizácii)
        self.width, self.height = new_width, new_height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        if self.background_path:
            self.load_background()

    def draw_background(self, color=None):
        if color:
            self.screen.fill(color)
        elif self.background:
            self.screen.blit(self.background, (0, 0))
