import pygame
from settings import START_BUTTON_COLOR, START_BUTTON_HOVER, START_BUTTON_SHADOW, START_TEXT_COLOR

def _draw_button(screen, rect, text, font_size, mouse_pos, border_radius=12):
    #Generická funkcia pre vykreslenie tlačidla
    hovered = rect.collidepoint(mouse_pos)
    shadow_rect = rect.move(2, 2)
    pygame.draw.rect(screen, START_BUTTON_SHADOW, shadow_rect, border_radius=border_radius)
    pygame.draw.rect(screen, START_BUTTON_HOVER if hovered else START_BUTTON_COLOR, rect, border_radius=border_radius)
    border_color = (60, 160, 40) if hovered else (80, 140, 60) if border_radius == 12 else ((255, 180, 120) if hovered else (255, 150, 100))
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=border_radius)
    font = pygame.font.SysFont("Consolas", font_size, bold=True)
    txt = font.render(text, True, START_TEXT_COLOR)
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect

def draw_start_button(screen, level_config, mouse_pos):
    grid_h, panel_h, console_x = level_config["GRID_HEIGHT"], level_config["PANEL_HEIGHT"], level_config["GRID_WIDTH"]
    rect = pygame.Rect(console_x + 150, grid_h + (panel_h - 120) // 2, 320, 120)
    return _draw_button(screen, rect, "START", 32, mouse_pos, border_radius=15)

def draw_menu_button(screen, level_config, mouse_pos):
    grid_w, console_w, header_h = level_config["GRID_WIDTH"], level_config["CONSOLE_WIDTH"], 70
    rect = pygame.Rect(grid_w + console_w - 115, (header_h - 45) // 2, 100, 45)
    return _draw_button(screen, rect, "MENU", 18, mouse_pos)

def draw_reset_button(screen, level_config, mouse_pos):
    grid_w, console_w, header_h = level_config["GRID_WIDTH"], level_config["CONSOLE_WIDTH"], 70
    menu_x = grid_w + console_w - 115
    rect = pygame.Rect(menu_x - 110, (header_h - 45) // 2, 100, 45)
    return _draw_button(screen, rect, "RESET", 18, mouse_pos)
