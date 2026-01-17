import pygame
from settings import START_BUTTON_COLOR, START_BUTTON_HOVER, START_BUTTON_SHADOW, START_TEXT_COLOR

def draw_menu_button(screen, level_config, mouse_pos):
    grid_w  = level_config["GRID_WIDTH"]
    console_w = level_config["CONSOLE_WIDTH"]
    header_h = 70

    w = 100
    h = 45

    # Pozícia vpravo v headeri konzoly
    x = grid_w + console_w - w - 15
    y = (header_h - h) // 2

    rect = pygame.Rect(x, y, w, h)

    hovered = rect.collidepoint(mouse_pos)

    # Veľmi jemný tieň
    shadow_rect = rect.move(2, 2)
    pygame.draw.rect(screen, START_BUTTON_SHADOW, shadow_rect, border_radius=12)

    # Jednoduché tlačidlo bez gradientu
    color = START_BUTTON_HOVER if hovered else START_BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)

    # Jemnejší okraj
    border_color = (130, 180, 240) if hovered else (90, 140, 210)
    pygame.draw.rect(screen, border_color, rect, width=1, border_radius=12)
    
    # Text bez tieňa
    font = pygame.font.SysFont("Consolas", 18, bold=True)
    txt = font.render("MENU", True, START_TEXT_COLOR)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

    return rect
