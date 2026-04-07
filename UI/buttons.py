import pygame
from UI.star_emoji import draw_star_emoji
from utils.settings import (
    CONSOLE_BORDER,
    HEADER_BG,
    START_BUTTON_COLOR,
    START_BUTTON_HOVER,
    START_BUTTON_SHADOW,
    START_TEXT_COLOR,
)


def _draw_button(screen, rect, text, font_size, mouse_pos, border_radius=12):
    hovered = rect.collidepoint(mouse_pos)
    shadow_rect = rect.move(2, 2)
    pygame.draw.rect(screen, START_BUTTON_SHADOW, shadow_rect, border_radius=border_radius)
    pygame.draw.rect(
        screen,
        START_BUTTON_HOVER if hovered else START_BUTTON_COLOR,
        rect,
        border_radius=border_radius,
    )
    border_color = (60, 160, 40) if hovered else (80, 140, 60)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=border_radius)
    font = pygame.font.SysFont("Consolas", font_size, bold=True)
    txt = font.render(text, True, START_TEXT_COLOR)
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect


def _draw_console_button(screen, rect, text, font_size, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg_color = (90, 150, 70) if hovered else (70, 130, 50)
    border_color = (110, 170, 90) if hovered else (90, 150, 70)

    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)

    font = pygame.font.SysFont("Consolas", font_size, bold=True)
    txt = font.render(text, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect


def _get_console_buttons_area(screen, level_config):
    grid_w = level_config["GRID_WIDTH"]
    console_w = screen.get_width() - grid_w
    header_h = 70
    return pygame.Rect(grid_w, header_h, console_w, 50)


def _console_button_rect(screen, level_config, button_index, total_buttons):
    area = _get_console_buttons_area(screen, level_config)
    padding = 10
    spacing = 8
    btn_w = (area.width - 2 * padding - (total_buttons - 1) * spacing) // total_buttons
    btn_h = area.height - 2 * padding
    x = area.x + padding + button_index * (btn_w + spacing)
    y = area.y + padding
    return pygame.Rect(x, y, btn_w, btn_h)


def draw_start_button(screen, level_config, mouse_pos):
    grid_h = level_config["GRID_HEIGHT"]
    panel_h = level_config["PANEL_HEIGHT"]
    available_left = level_config["GRID_WIDTH"] + 20
    available_right = screen.get_width() - 20
    available_w = max(220, available_right - available_left)
    btn_w = min(340, available_w)
    btn_h = 110
    x = available_left + (available_w - btn_w) // 2
    y = grid_h + (panel_h - btn_h) // 2
    rect = pygame.Rect(x, y, btn_w, btn_h)
    return _draw_button(screen, rect, "START", 32, mouse_pos, border_radius=15)


def draw_console_buttons_area(screen, level_config, has_mode=False):
    area = _get_console_buttons_area(screen, level_config)
    pygame.draw.rect(screen, HEADER_BG, area)
    pygame.draw.line(screen, CONSOLE_BORDER, (area.x, area.bottom), (area.right, area.bottom), width=2)


def draw_stars_info_button(screen, level_config, mouse_pos, has_mode=False):
    total = 4 if has_mode else 3
    index = 3 if has_mode else 2
    rect = _console_button_rect(screen, level_config, index, total)

    hovered = rect.collidepoint(mouse_pos)
    bg_color = (90, 150, 70) if hovered else (70, 130, 50)
    border_color = (110, 170, 90) if hovered else (90, 150, 70)

    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)

    star_size = min(rect.width, rect.height) - 6
    draw_star_emoji(screen, rect.center, star_size)
    return rect


def draw_menu_button(screen, level_config, mouse_pos, has_mode=False):
    total = 4 if has_mode else 3
    index = 2 if has_mode else 1
    rect = _console_button_rect(screen, level_config, index, total)
    return _draw_console_button(screen, rect, "MENU", 16, mouse_pos)


def draw_reset_button(screen, level_config, mouse_pos, has_mode=False):
    total = 4 if has_mode else 3
    index = 1 if has_mode else 0
    rect = _console_button_rect(screen, level_config, index, total)
    return _draw_console_button(screen, rect, "RESET", 16, mouse_pos)


def draw_mode_toggle_button(screen, level_config, mouse_pos, text_mode):
    rect = _console_button_rect(screen, level_config, 0, 4)
    text = "TEXT" if not text_mode else "DRAG"
    return _draw_console_button(screen, rect, text, 16, mouse_pos)
