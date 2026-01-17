import pygame

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FULLSCREEN = False

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
MENU_IMG = "Images/menuTestBG.png"

BUTTON_COLOR = (100, 150, 255)      # Modrá
BUTTON_HOVER = (120, 170, 255)      # Svetlejšia modrá
BUTTON_SHADOW = (60, 100, 180)      # Tmavší tieň
TEXT_COLOR = (255, 255, 255)        # Biela
TEXT_COLOR_DARK = (30, 30, 40)      # Tmavá pre svetlé pozadia

# Popup okno
POPUP_BG = (245, 248, 255)          # Svetlo modrá
POPUP_BORDER = (80, 120, 200)      # Modrý okraj

# Grid farby - prírodnejšie farby
GRASS_GREEN = (120, 180, 100)
BOARD_OUT = (100, 80, 60)          # Hnedá/tehlová farba
CELL_EDGE = (60, 50, 40)           # Jemnejšia hranica - hnedá
GRID_BG = (45, 55, 70)             # Tmavšie pozadie gridu
GRID_SHADOW = (30, 25, 20)         # Tmavý tieň gridu

# UI - Modernizované farby
UI_BG = (35, 40, 50)               # Tmavšie telo
UI_HEADER = (50, 60, 75)           # Horná lišta
UI_BORDER = (60, 75, 90)           # Okraj
UI_ACCENT = (100, 200, 255)        # Svetlo modrá LED
UI_ACCENT_GLOW = (150, 220, 255)   # Žiarenie LED

# Konzola
CONSOLE_BG = UI_BG
CONSOLE_BORDER = UI_BORDER
HEADER_BG = UI_HEADER
TEXT_COLOR_K = (220, 230, 240)     # Svetlo sivá
LED_ON = UI_ACCENT
LED_OFF = (50, 70, 85)
LED_GLOW = UI_ACCENT_GLOW

# Panel
PANEL_BG = UI_BG
PANEL_BORDER = UI_BORDER

# --- Tlačidlá ---
START_BUTTON_COLOR = (80, 150, 220)
START_BUTTON_HOVER = (100, 170, 240)
START_BUTTON_SHADOW = (40, 80, 120)
START_TEXT_COLOR = (255, 255, 255)

# Draggable tlačidlá
DRAG_BUTTON_BG = (60, 70, 85)
DRAG_BUTTON_HOVER = (80, 95, 115)
DRAG_BUTTON_BORDER = (100, 120, 140)
DRAG_BUTTON_SHADOW = (30, 35, 45)

FONT_BTN = pygame.font.SysFont("Consolas", 22)


