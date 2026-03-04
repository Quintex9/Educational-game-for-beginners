import pygame
from utils.settings import PANEL_BG, PANEL_BORDER
from UI.draggable_button import draggableButton

panel_buttons = []
PANEL_POS = (0, 0)

BTN_W = 150
BTN_H = 50
BTN_PADDING = 10

# Level -> (columns, [(label, command), ...])
LEVEL_PANEL_CONFIG = {
    1: (2, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
    ]),
    2: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
    ]),
    3: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("IF", "if"),
    ]),
    4: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
        ("IF", "if"),
    ]),
    5: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
    ]),
    6: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
        ("IF", "if"),
    ]),
    7: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
        ("IF", "if"),
    ]),
    8: (3, [
        ("UP", "move_up"),
        ("DOWN", "move_down"),
        ("LEFT", "move_left"),
        ("RIGHT", "move_right"),
        ("FOR", "for_start"),
        ("END", "for_end"),
        ("IF", "if"),
    ]),
}


def _build_buttons(panel_rect, cols, items):
    created = []
    x0 = panel_rect.x + BTN_PADDING
    y0 = panel_rect.y + BTN_PADDING

    for i, (label, cmd) in enumerate(items):
        c = i % cols
        r = i // cols
        x = x0 + c * (BTN_W + BTN_PADDING)
        y = y0 + r * (BTN_H + BTN_PADDING)
        created.append(draggableButton(x, y, BTN_W, BTN_H, label, cmd))

    return created


def buttons_for_level(level, panel_rect):
    global panel_buttons
    panel_buttons.clear()

    config = LEVEL_PANEL_CONFIG.get(level)
    if not config:
        return

    cols, items = config
    panel_buttons.extend(_build_buttons(panel_rect, cols, items))


def draw_panel(screen, level_config):
    global PANEL_POS

    panel_h = level_config["PANEL_HEIGHT"]
    grid_h = level_config["GRID_HEIGHT"]
    grid_w = level_config["GRID_WIDTH"]
    panel_w = grid_w + level_config["CONSOLE_WIDTH"]

    PANEL_POS = (0, grid_h)
    px, py = PANEL_POS

    rect = pygame.Rect(px, py, panel_w, panel_h)

    pygame.draw.rect(screen, PANEL_BG, rect)
    pygame.draw.rect(screen, PANEL_BORDER, rect, width=3)
    pygame.draw.line(screen, (160, 140, 100), (px, py), (px + panel_w, py), width=2)

    return rect
