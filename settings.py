import pygame

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FULLSCREEN = False

GRID_SIZES = [5, 6, 5, 7, 8]

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

BUTTON_COLOR = (100, 160, 80)      # Zelená
BUTTON_HOVER = (120, 200, 100)     # Svetlejšia zelená
BUTTON_SHADOW = (60, 120, 50)      # Tmavší zelený tieň
TEXT_COLOR = (255, 255, 255)        # Biela
TEXT_COLOR_DARK = (30, 30, 40)      # Tmavá pre svetlé pozadia

# Popup okno
POPUP_BG = (180, 220, 160)          # Svetlo zelená
POPUP_BORDER = (80, 140, 60)       # Tmavá zelená okraj

# Grid farby - zelená/hnedá téma pre deti
GRASS_GREEN = (120, 180, 100)
BOARD_OUT = (139, 90, 43)          # Hnedá okraj gridu
CELL_EDGE = (160, 120, 60)         # Svetlejšia hnedá hranica
GRID_BG = (240, 245, 255)          # Svetlo modré pozadie gridu
GRID_SHADOW = (100, 80, 60)        # Tmavá hnedá tieň gridu

# UI - zelená/hnedá téma
UI_BG = (180, 220, 160)            # Svetlo zelené telo
UI_HEADER = (120, 180, 100)        # Zelená horná lišta
UI_BORDER = (80, 140, 60)          # Tmavšia zelená okraj
UI_ACCENT = (100, 200, 100)        # Zelená LED
UI_ACCENT_GLOW = (150, 255, 150)   # Svetlo zelené žiarenie

# Konzola - zelená/hnedá téma
CONSOLE_BG = (200, 230, 180)       # Svetlo zelené pozadie
CONSOLE_BORDER = (100, 160, 80)    # Tmavšia zelená okraj
HEADER_BG = (120, 180, 100)        # Zelená hlavička
TEXT_COLOR_K = (40, 80, 40)        # Tmavá zelená text
LED_ON = (100, 200, 100)           # Zelená LED
LED_OFF = (150, 200, 150)          # Svetlo zelená LED
LED_GLOW = (120, 255, 120)         # Zelené žiarenie

# Panel - hnedá/zelená téma
PANEL_BG = (180, 160, 120)         # Svetlo hnedé pozadie
PANEL_BORDER = (139, 90, 43)       # Hnedý okraj

# --- Tlačidlá ---
START_BUTTON_COLOR = (100, 160, 80)    # Zelené
START_BUTTON_HOVER = (120, 200, 100)   # Svetlejšie zelené
START_BUTTON_SHADOW = (60, 120, 50)    # Tmavšie zelené
START_TEXT_COLOR = (255, 255, 255)      # Biela

# Draggable tlačidlá - zelená/hnedá téma
DRAG_BUTTON_BG = (140, 180, 120)       # Svetlo zelená
DRAG_BUTTON_HOVER = (160, 200, 140)    # Svetlejšie zelená
DRAG_BUTTON_BORDER = (100, 140, 80)    # Tmavšia zelená okraj
DRAG_BUTTON_SHADOW = (80, 120, 60)     # Tmavá zelená tieň

FONT_BTN = pygame.font.SysFont("Consolas", 22)

# Konštanty pre konzolu
CONSOLE_SLOT_HEIGHT = 50
CONSOLE_BUTTON_WIDTH = 100
CONSOLE_BUTTON_HEIGHT = 50
CONSOLE_COLUMN_SPACING = 20
CONSOLE_INDENT_WIDTH = 30
CONSOLE_PADDING = 20

# Mapovanie pohybových príkazov
MOVE_COMMANDS = {
    "move_up": "UP",
    "move_down": "DOWN",
    "move_left": "LEFT",
    "move_right": "RIGHT"
}

# Možnosti pre FOR cyklus
FOR_OPTIONS = [("FOR 2x", 2), ("FOR 3x", 3), ("FOR 4x", 4), ("FOR 5x", 5), ("FOR 6x", 6)]
FOR_POPUP_WIDTH = 160


