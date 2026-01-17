import pygame
from settings import (BUTTON_COLOR, BUTTON_HOVER, BUTTON_SHADOW, POPUP_BG, POPUP_BORDER, 
                     TEXT_COLOR, TEXT_COLOR_DARK)

def draw_button(screen, rect, text, font, hovered):
    # Veľmi jemný tieň
    shadow_rect = rect.move(2, 2)
    pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=12)
    
    # Jednoduché tlačidlo bez gradientu
    color = BUTTON_HOVER if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)
    
    # Jemnejší okraj
    border_color = (130, 180, 240) if hovered else (90, 140, 210)
    pygame.draw.rect(screen, border_color, rect, width=1, border_radius=12)
    
    # Text bez tieňa
    txt = font.render(text, True, TEXT_COLOR)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

def draw_showlevels(screen: pygame.Surface, mouse_pos):
    screen_width, screen_height = screen.get_size()
    
    font_button = pygame.font.SysFont("Consolas", 28, bold=True)
    font_title = pygame.font.SysFont("Consolas", 38, bold=True)

    popup_width, popup_height = 550, 600
    popup_rect = pygame.Rect(
        (screen_width - popup_width) // 2,
        (screen_height - popup_height) // 2,
        popup_width,
        popup_height
    )
    
    # Pozadie popup okna
    pygame.draw.rect(screen, POPUP_BG, popup_rect, border_radius=20)
    
    # Okraj popup okna
    pygame.draw.rect(screen, POPUP_BORDER, popup_rect, width=4, border_radius=20)
    
    # Vnútorný okraj pre hĺbku
    inner_rect = popup_rect.inflate(-10, -10)
    pygame.draw.rect(screen, (200, 210, 230), inner_rect, width=2, border_radius=15)

    # Nadpis s tieňom
    title_text = font_title.render("Vyber level", True, TEXT_COLOR_DARK)
    title_shadow = font_title.render("Vyber level", True, (180, 190, 210))
    title_rect = title_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 70))
    screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
    screen.blit(title_text, title_rect)

    # Level tlačidlá
    level_names = ["Level 1", "Level 2", "Level 3", "Level 4"]
    buttons = []

    for i, lvl in enumerate(level_names):
        rect = pygame.Rect(0, 0, 220, 65)
        rect.center = (popup_rect.centerx, popup_rect.top + 150 + i * 75)
        hovered = rect.collidepoint(mouse_pos)
        draw_button(screen, rect, lvl, font_button, hovered)
        buttons.append((lvl, rect))

    # Späť tlačidlo
    back_rect = pygame.Rect(0, 0, 220, 65)
    back_rect.center = (popup_rect.centerx, popup_rect.bottom - 70)
    hovered = back_rect.collidepoint(mouse_pos)
    draw_button(screen, back_rect, "Späť", font_button, hovered)
    buttons.append(("Späť", back_rect))
    
    return buttons
