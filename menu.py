import pygame
from settings import set_level_size, MENU_IMG, FULLSCREEN, SCALE

rozmery = set_level_size(0, fullscreen=FULLSCREEN, scale=SCALE)
SCREEN_WIDTH = rozmery["SCREEN_WIDTH"]
SCREEN_HEIGHT = rozmery["SCREEN_HEIGHT"]

background = pygame.image.load(MENU_IMG)
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

def draw_menu(screen):
    screen.blit(background,(0,0))