import os
import pygame

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FULLSCREEN = False
SCALE = 1.0

GRID_SIZES = [5, 6, 7, 8]

def set_level_size(level_index: int, screen_w=WIDTH, screen_h=HEIGHT, fullscreen: bool = FULLSCREEN):
    grid_size = GRID_SIZES[level_index]

    # Rovnaké proporcie pre všetky režimy
    GRID_HEIGHT_RATIO = 0.60
    CONSOLE_WIDTH_RATIO = 0.25
    PANEL_HEIGHT_RATIO = 0.25

    # výpočty (už podľa aktuálneho rozlíšenia)
    cell_size = int((screen_h * GRID_HEIGHT_RATIO) / grid_size)
    grid_width = grid_size * cell_size
    grid_height = grid_size * cell_size
    console_width = grid_width
    panel_height = int(screen_h * PANEL_HEIGHT_RATIO)

    # výsledná veľkosť okna
    if fullscreen:
        screen_width = screen_w
        screen_height = screen_h
    else:
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


# ---------- Farby ----------
MENU_IMG = "Images/menu.png"
BUTTON_COLOR = (255, 224, 102)
BUTTON_HOVER = (255, 239, 0)
BUTTON_SHADOW = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)
POPUP_BG = (255, 255, 240)
POPUP_BORDER = (80, 80, 80)
GRASS_GREEN = (190, 150, 0)
BOARD_OUT = (120, 95, 90)
CELL_EDGE = (0, 0, 0)
PANEL_BG = (150, 120, 110)
PANEL_BORDER = (100, 80, 75)