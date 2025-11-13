import pygame
from settings import PANEL_BG, PANEL_BORDER

def draw_panel(screen, level_config):
    panel_h = level_config["PANEL_HEIGHT"]
    grid_h  = level_config["GRID_HEIGHT"]
    grid_w  = level_config["GRID_WIDTH"]

    rect = pygame.Rect(0, grid_h, grid_w + level_config["CONSOLE_WIDTH"], panel_h)

    pygame.draw.rect(screen, PANEL_BG, rect)
    pygame.draw.rect(screen, PANEL_BORDER, rect, width=2)

    return rect

