import pygame
from settings import PANEL_BG, PANEL_BORDER, FONT_BTN
from UI.draggable_button import draggableButton


panel_buttons = []

PANEL_POS = (0, 0)


def level1_buttons(panel_rect):
    btn_w = 150
    btn_h = 50
    padding = 10

    buttons = [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
    ]

    created = []
    cols = 2   # počet stĺpcov
    x0 = panel_rect.x + padding
    y0 = panel_rect.y + padding

    for i, (label, cmd) in enumerate(buttons):
        c = i % cols      # stĺpec
        r = i // cols     # riadok

        x = x0 + c * (btn_w + padding)
        y = y0 + r * (btn_h + padding)

        created.append(draggableButton(x, y, btn_w, btn_h, label, cmd))

    return created


def level2_buttons(panel_rect):
    btn_w = 150
    btn_h = 50
    padding = 10

    buttons = [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
    ]

    created = []

    cols = 3
    x0 = panel_rect.x + padding
    y0 = panel_rect.y + padding

    for i, (label, cmd) in enumerate(buttons):
        c = i % cols
        r = i // cols

        x = x0 + c * (btn_w + padding)
        y = y0 + r * (btn_h + padding)

        created.append(draggableButton(x, y, btn_w, btn_h, label, cmd))

    return created



def level3_buttons(panel_rect):
    btn_w = 150
    btn_h = 50
    padding = 10

    buttons = [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
        ("IF", "if"),
        ("ELSE", "else"),
    ]

    created = []

    cols = 4
    x0 = panel_rect.x + padding
    y0 = panel_rect.y + padding

    for i, (label, cmd) in enumerate(buttons):
        c = i % cols
        r = i // cols

        x = x0 + c * (btn_w + padding)
        y = y0 + r * (btn_h + padding)

        created.append(draggableButton(x, y, btn_w, btn_h, label, cmd))

    return created



def buttons_for_level(level, panel_rect):
    """Naplní globálny list panel_buttons podľa levelu (bez zmeny referencie)."""
    global panel_buttons

    # KĽÚČOVÉ: nemeníme referenciu, len obsah
    panel_buttons.clear()

    if level == 1:
        panel_buttons.extend(level1_buttons(panel_rect))
    elif level == 2:
        panel_buttons.extend(level2_buttons(panel_rect))
    elif level == 3:
        panel_buttons.extend(level3_buttons(panel_rect))


def draw_panel(screen, level_config):
    global PANEL_POS

    panel_h = level_config["PANEL_HEIGHT"]
    grid_h  = level_config["GRID_HEIGHT"]
    grid_w  = level_config["GRID_WIDTH"]
    panel_w = grid_w + level_config["CONSOLE_WIDTH"]

    PANEL_POS = (0, grid_h)
    px, py = PANEL_POS

    rect = pygame.Rect(px, py, panel_w, panel_h)

    pygame.draw.rect(screen, PANEL_BG, rect)
    pygame.draw.rect(screen, PANEL_BORDER, rect, width=2)

    # TLAČIDLÁ UŽ TU NEKRESLÍME – kreslím ich v main.py
    return rect
