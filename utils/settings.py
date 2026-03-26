import pygame

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

GRID_SIZES = [5, 6, 5, 7, 8, 8, 9, 10]


def set_level_size(level_index: int, screen_w=WIDTH, screen_h=HEIGHT):
    grid_size = GRID_SIZES[level_index]

    # Rovnake proporcie pre vsetky rezimy
    GRID_HEIGHT_RATIO = 0.60
    PANEL_HEIGHT_RATIO = 0.25

    # vypocty
    cell_size = int((screen_h * GRID_HEIGHT_RATIO) / grid_size)
    grid_width = grid_size * cell_size
    grid_height = grid_size * cell_size
    console_width = grid_width
    panel_height = int(screen_h * PANEL_HEIGHT_RATIO)

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
MENU_IMG = "Images/MENU.jpg"

BUTTON_COLOR = (100, 160, 80)      # Zelena
BUTTON_HOVER = (120, 200, 100)     # Svetlejsia zelena
BUTTON_SHADOW = (60, 120, 50)      # Tmavsi zeleny tien
TEXT_COLOR = (255, 255, 255)       # Biela
TEXT_COLOR_DARK = (30, 30, 40)     # Tmava pre svetle pozadia

# Popup okno
POPUP_BG = (180, 220, 160)         # Svetlo zelena
POPUP_BORDER = (80, 140, 60)       # Tmava zelena okraj

# Grid farby - zelena/hneda tema pre deti
GRASS_GREEN = (120, 180, 100)
BOARD_OUT = (139, 90, 43)          # Hneda okraj gridu
CELL_EDGE = (160, 120, 60)         # Svetlejsia hneda hranica
GRID_BG = (240, 245, 255)          # Svetlo modre pozadie gridu
GRID_SHADOW = (100, 80, 60)        # Tmava hneda tien

# UI - zelena/hneda tema
UI_BG = (180, 220, 160)            # Svetlo zelene telo
UI_HEADER = (120, 180, 100)        # Zelena horna lista
UI_BORDER = (80, 140, 60)          # Tmavsia zelena okraj
UI_ACCENT = (100, 200, 100)        # Zelena LED
UI_ACCENT_GLOW = (150, 255, 150)   # Svetlo zelene ziarenie

# Konzola - zelena/hneda tema
CONSOLE_BG = (200, 230, 180)       # Svetlo zelene pozadie
CONSOLE_BORDER = (100, 160, 80)    # Tmavsia zelena okraj
HEADER_BG = (120, 180, 100)        # Zelena hlavicka
TEXT_COLOR_K = (40, 80, 40)        # Tmava zelena text
LED_ON = (100, 200, 100)           # Zelena LED
LED_OFF = (150, 200, 150)          # Svetlo zelena LED
LED_GLOW = (120, 255, 120)         # Zelene ziarenie

# Panel - hneda/zelena tema
PANEL_BG = (180, 160, 120)         # Svetlo hnede pozadie
PANEL_BORDER = (139, 90, 43)       # Hnedy okraj

# --- Tlacidla ---
START_BUTTON_COLOR = (100, 160, 80)    # Zelene
START_BUTTON_HOVER = (120, 200, 100)   # Svetlejsie zelene
START_BUTTON_SHADOW = (60, 120, 50)    # Tmavsie zelene
START_TEXT_COLOR = (255, 255, 255)     # Biela

# Draggable tlacidla - zelena/hneda tema
DRAG_BUTTON_BG = (140, 180, 120)       # Svetlo zelena
DRAG_BUTTON_HOVER = (160, 200, 140)    # Svetlejsie zelena
DRAG_BUTTON_BORDER = (100, 140, 80)    # Tmavsia zelena okraj
DRAG_BUTTON_SHADOW = (80, 120, 60)     # Tmava zelena tien

FONT_BTN = pygame.font.SysFont("Consolas", 22)

# Konstanty pre konzolu
CONSOLE_SLOT_HEIGHT = 50
CONSOLE_BUTTON_WIDTH = 100
CONSOLE_BUTTON_HEIGHT = 50
CONSOLE_COLUMN_SPACING = 20
CONSOLE_INDENT_WIDTH = 30
CONSOLE_PADDING = 20
# Stabilna sirka pre vypocet stlpcov v konzole.
# Musi pokryt najdlhsi prikaz (napr. "IF obstacle right" ma sirku 190).
CONSOLE_LAYOUT_BUTTON_WIDTH = 190
# Stabilny pocet indent krokov rezervovanych pre layout.
# Levely nepodporuju vnoreny FOR, takze maximalny prakticky indent je 2
# (for body + break obstacle pod IF).
CONSOLE_LAYOUT_MAX_INDENT = 2

# Mapovanie pohybovych prikazov
MOVE_COMMANDS = {
    "move_up": "UP",
    "move_down": "DOWN",
    "move_left": "LEFT",
    "move_right": "RIGHT"
}

# Moznosti pre FOR cyklus
FOR_OPTIONS = [("FOR 2x", 2), ("FOR 3x", 3), ("FOR 4x", 4), ("FOR 5x", 5), ("FOR 6x", 6)]
FOR_POPUP_WIDTH = 160

# Limit znakov pre 1 riadok v textovej konzole
TEXT_CONSOLE_MAX_CHARS = 20
