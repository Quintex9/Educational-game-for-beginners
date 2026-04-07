# Basic popup functions

import pygame
from UI.star_emoji import get_star_font


def draw_popup(screen, title, lines, button_text="OK", width=500, height=None):
    screen_width, screen_height = screen.get_size()

    title_font = pygame.font.SysFont("Consolas", 32, bold=True)
    text_font = pygame.font.SysFont("Consolas", 18)
    emoji_text_font = get_star_font(18)
    button_font = pygame.font.SysFont("Consolas", 20, bold=True)

    padding = 40
    min_width = 300

    title_width = title_font.size(title)[0]
    max_line_width = 0
    for line in lines:
        if not line:
            continue
        line_font = emoji_text_font if "⭐" in line else text_font
        line_width = line_font.size(line)[0]
        max_line_width = max(max_line_width, line_width)

    button_text_width = button_font.size(button_text)[0]
    button_width = max(120, button_text_width + 20)
    max_content_width = max(title_width, max_line_width, button_width)

    if width == 500:
        width = max(min_width, max_content_width + padding * 2)
    else:
        width = max(width, max_content_width + padding * 2)

    if height is None:
        title_height = 50
        line_height = 30
        button_height = 50
        height = title_height + len(lines) * line_height + button_height + padding * 2

    popup_x = (screen_width - width) // 2
    popup_y = (screen_height - height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, width, height)

    pygame.draw.rect(screen, (220, 180, 60), popup_rect, border_radius=15)
    pygame.draw.rect(screen, (180, 120, 20), popup_rect, width=4, border_radius=15)

    title_surf = title_font.render(title, True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 30))
    screen.blit(title_surf, title_rect)

    y_offset = popup_rect.y + 70
    for line in lines:
        line_font = emoji_text_font if "⭐" in line else text_font
        line_surf = line_font.render(line, True, (0, 0, 0))
        line_rect = line_surf.get_rect(center=(popup_rect.centerx, y_offset))
        screen.blit(line_surf, line_rect)
        y_offset += 30

    button_width = 120
    button_height = 45
    button_x = popup_rect.centerx - button_width // 2
    button_y = popup_rect.bottom - button_height - 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    mouse_pos = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(mouse_pos)
    button_color = (255, 180, 60) if hovered else (255, 160, 40)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
    pygame.draw.rect(screen, (220, 140, 20), button_rect, width=3, border_radius=8)

    button_text_surf = button_font.render(button_text, True, (255, 255, 255))
    button_text_rect = button_text_surf.get_rect(center=button_rect.center)
    screen.blit(button_text_surf, button_text_rect)

    return popup_rect, button_rect


def draw_limit_warning_popup(screen):
    title = "Dosiahnutý limit!"
    lines = [
        "Konzola je plná.",
        "Nemôžeš pridať ďalšie príkazy.",
        "",
        "Môžeš zresetovať konzolu",
        "pomocou tlačidla RESET.",
    ]
    return draw_popup(screen, title, lines, "OK")


def draw_error_popup(screen, error_message):
    title = "Chyba!"
    lines = error_message.split("\n")
    return draw_popup(screen, title, lines, "OK")
