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

    PANEL_HEIGHT_RATIO = 0.25

    # výpočty 
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

BORDER = (100, 80, 60)

# UI
UI_BG = (40, 35, 33)      # tmavé telo konzoly
UI_HEADER    = (110, 90, 85)     # horná lišta konzoly
UI_BORDER    = (90, 70, 65)       # okraj
UI_ACCENT    = (90, 225, 215)    # LED

# Konzola
CONSOLE_BG     = UI_BG
CONSOLE_BORDER = UI_BORDER
HEADER_BG      = UI_HEADER
TEXT_COLOR_K   = (240, 235, 225)
LED_ON         = UI_ACCENT
LED_OFF        = (40, 80, 75)

# Panel
PANEL_BG       = UI_BG
PANEL_BORDER   = UI_BORDER

# --- Tlačidlá ---
START_BUTTON_COLOR   = (120, 100, 90)
START_BUTTON_HOVER   = (140, 120, 110)
START_BUTTON_SHADOW  = (55, 45, 42)
START_TEXT_COLOR     = (255, 255, 240)
BORDER         = UI_BORDER

FONT_BTN = pygame.font.SysFont("Consolas", 22)


