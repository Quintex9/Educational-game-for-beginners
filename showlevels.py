import pygame

from settings import BUTTON_COLOR, BUTTON_HOVER, BUTTON_SHADOW, POPUP_BG, POPUP_BORDER, TEXT_COLOR

def draw_showlevels(screen: pygame.Surface, mouse_pos):
    screen_width, screen_height = screen.get_size()
    
    font_button = pygame.font.SysFont("Arial", 30, bold=True)
    font_title = pygame.font.SysFont("Arial", 40, bold=True)

    popup_width, popup_height = 500, 500
    popup_rect = pygame.Rect(
        (screen_width - popup_width) // 2,
        (screen_height - popup_height) // 2,
        popup_width,
        popup_height
    )

    pygame.draw.rect(screen, POPUP_BG, popup_rect, border_radius=16)
    pygame.draw.rect(screen, POPUP_BORDER, popup_rect, 3, border_radius=16)

    # Nadpis
    title_text = font_title.render("Vyber level", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 60))
    screen.blit(title_text, title_rect)

    # Level tlačidlá
    level_names = ["Level 1", "Level 2", "Level 3", "Level 4"]
    buttons = []

    for i, lvl in enumerate(level_names):
        rect = pygame.Rect(0, 0, 180, 60)
        rect.center = (popup_rect.centerx, popup_rect.top + 130 + i * 70)
        
        shadow_rect = rect.move(6,6)
        pygame.draw.rect(screen,BUTTON_SHADOW,shadow_rect,border_radius=8)
        
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=8)
        
        txt = font_button.render(lvl, True, TEXT_COLOR)
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)
        buttons.append((lvl, rect))

    # Späť
    back_rect = pygame.Rect(0, 0, 180, 60)
    back_rect.center = (popup_rect.centerx, popup_rect.bottom - 60)
    
    shadow_rect = back_rect.move(6,6)
    pygame.draw.rect(screen,BUTTON_SHADOW,shadow_rect,border_radius=8)
    
    color = BUTTON_HOVER if back_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, back_rect, border_radius=8)
    
    back_txt = font_button.render("Späť", True, TEXT_COLOR)
    screen.blit(back_txt, back_txt.get_rect(center=back_rect.center))

    buttons.append(("Späť", back_rect))
    return buttons
