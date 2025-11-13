import pygame
from settings import START_BUTTON_COLOR, START_BUTTON_HOVER, START_BUTTON_SHADOW, BORDER, START_TEXT_COLOR, UI_ACCENT

def draw_start_button(screen, level_config, mouse_pos):
    grid_h  = level_config["GRID_HEIGHT"]
    panel_h = level_config["PANEL_HEIGHT"]
    console_x = level_config["GRID_WIDTH"]

    w = 300
    h = 150

    x = console_x + 150
    y = grid_h + (panel_h - h) // 2

    rect = pygame.Rect(x, y, w, h)

    hovered = rect.collidepoint(mouse_pos)
    base = START_BUTTON_HOVER if hovered else START_BUTTON_COLOR

    # Tieň
    pygame.draw.rect(screen, START_BUTTON_SHADOW, rect.move(3, 3), border_radius=10)

    # Tlačidlo
    pygame.draw.rect(screen, base, rect, border_radius=10)
    pygame.draw.rect(screen, BORDER, rect, width=2, border_radius=10)

    
    # Text
    font = pygame.font.SysFont("Consolas", 24, bold=True)
    txt = font.render("START", True, START_TEXT_COLOR)
    screen.blit(txt, txt.get_rect(center=rect.center))

    return rect

