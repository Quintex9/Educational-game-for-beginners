import os
import pygame

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FULLSCREEN = False
SCALE = 1.0

GRID_SIZES = [5,6,7,7]

def set_level_size(level_index: int, fullscreen: bool = FULLSCREEN, scale: float = SCALE):
    grid_size = GRID_SIZES[level_index]
    
    if fullscreen:
        screen_width = WIDTH
        screen_height = HEIGHT
        cell_size = int((screen_height * 0.6) / grid_size)
        grid_width = grid_size * cell_size
        grid_height = grid_size * cell_size
        console_width = int(screen_width * 0.25)
        panel_height = int(screen_height * 0.2)
    else:
        cell_size = int((HEIGHT * 0.6) / grid_size)
        grid_width = grid_size * cell_size
        grid_height = grid_size * cell_size
        console_width = int(WIDTH * 0.25) # 0.25 - konzola bude tvoriť cca 25% šírky obrazovky
        panel_height = int(HEIGHT * 0.2)
    
        screen_width = grid_width + console_width
        screen_height = grid_height + panel_height
    
    return {
        "GRID_SIZE": grid_size,
        "CELL_SIZE": cell_size,
        "GRID_WIDTH": grid_width,
        "GRID_HEIGHT": grid_height,
        "CONSOLE_WIDTH": console_width,
        "PANEL_HEIGHT": panel_height,
        "SCREEN_WIDTH": screen_width,
        "SCREEN_HEIGHT": screen_height
    }
    
MENU_IMG = "Images/menuBG.jpg"