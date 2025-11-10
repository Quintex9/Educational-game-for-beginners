import pygame
from settings import PANEL_BG, PANEL_BORDER

def draw_panel(screen: pygame.Surface, level_config: dict):
    
    panel_h = level_config["PANEL_HEIGHT"]
    grid_h = level_config["GRID_HEIGHT"]
    grid_w = level_config["GRID_WIDTH"]
    
    x = 0 
    panel_rect = pygame.Rect(x,grid_h,grid_w,panel_h)
    
    pygame.draw.rect(screen,PANEL_BG,panel_rect)
    pygame.draw.rect(screen, PANEL_BORDER, panel_rect,width=3)
    
    return panel_rect