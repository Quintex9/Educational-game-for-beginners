import pygame
from utils.settings import BUTTON_COLOR, BUTTON_HOVER, BUTTON_SHADOW, TEXT_COLOR

def _draw_buttons(screen: pygame.Surface, mouse_pos, button_texts):
    screen_width, screen_height = screen.get_size()
    
    font_button = pygame.font.SysFont("Consolas", 32, bold=True)

    buttons = []
    
    for i, text in enumerate(button_texts):
        #Veľkosť tlačidla
        btn_width, btn_height = 280, 80
        
        #Pozícia tlačidla
        btn_x = screen_width // 2 - btn_width // 2
        btn_y = screen_height // 2 - 30 + i * 95
        
        rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        hovered = rect.collidepoint(mouse_pos)
        
        # Veľmi jemný tieň
        shadow_rect = rect.move(2, 2)
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=15)
        
        # Jednoduché tlačidlo bez gradientu
        color = BUTTON_HOVER if hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=15)
        
        # Jemnejší okraj
        border_color = (60, 160, 40) if hovered else (80, 140, 60)
        pygame.draw.rect(screen, border_color, rect, width=1, border_radius=15)
        
        # Text bez tieňa - čistejší vzhľad
        txt = font_button.render(text, True, TEXT_COLOR)
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)
        
        buttons.append((text, rect))
        
    return buttons

def _draw_game_title(screen: pygame.Surface):
    screen_width, screen_height = screen.get_size()
    font_title = pygame.font.SysFont("couriernew", 72, bold=True)

    title = "GRID RUN"
    shadow = font_title.render(title, True, (20, 45, 20))
    text = font_title.render(title, True, (235, 255, 235))

    title_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 170))
    screen.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(text, title_rect)

def draw_menu(screen: pygame.Surface, mouse_pos):
    # Hlavne menu
    _draw_game_title(screen)
    return _draw_buttons(screen, mouse_pos, ["Štart", "Koniec"])

def draw_level_groups(screen: pygame.Surface, mouse_pos):
    # Vyber skupiny levelov po kliknuti na Start
    _draw_game_title(screen)
    return _draw_buttons(screen, mouse_pos, ["Začiatočník", "Pokročilý", "Späť"])

def draw_button(screen, rect, text, font, hovered):
    # Veľmi jemný tieň
    shadow_rect = rect.move(2, 2)
    pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=12)
    
    # Jednoduché tlačidlo bez gradientu
    color = BUTTON_HOVER if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)
    
    # Jemnejší okraj
    border_color = (60, 160, 40) if hovered else (80, 140, 60)
    pygame.draw.rect(screen, border_color, rect, width=1, border_radius=12)
    
    # Text bez tieňa
    txt = font.render(text, True, TEXT_COLOR)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

def draw_showlevels(screen: pygame.Surface, mouse_pos, level_group):
    screen_width, screen_height = screen.get_size()
    
    font_button = pygame.font.SysFont("Consolas", 28, bold=True)
    font_title = pygame.font.SysFont("Consolas", 38, bold=True)
    font_subtitle = pygame.font.SysFont("Consolas", 20, bold=True)

    popup_width, popup_height = 550, 700
    popup_rect = pygame.Rect(
        (screen_width - popup_width) // 2,
        (screen_height - popup_height) // 2,
        popup_width,
        popup_height
    )
    
    # Pozadie popup okna
    from utils.settings import POPUP_BG, POPUP_BORDER
    pygame.draw.rect(screen, POPUP_BG, popup_rect, border_radius=20)
    
    # Okraj popup okna
    pygame.draw.rect(screen, POPUP_BORDER, popup_rect, width=4, border_radius=20)
    
    # Vnútorný okraj pre hĺbku - svetlá zelená
    inner_rect = popup_rect.inflate(-10, -10)
    pygame.draw.rect(screen, (140, 200, 120), inner_rect, width=2, border_radius=15)

    # Nadpis s tieňom
    if level_group == "levels_1_4":
        title_label = "Začiatočník"
        subtitle_label = "Ľahšie levely, princíp drag & drop"
        level_names = ["Level 1", "Level 2", "Level 3", "Level 4"]
    else:
        title_label = "Pokročilý"
        subtitle_label = "Levely s drag & drop alebo textovým vstupom"
        level_names = ["Level 5", "Level 6", "Level 7", "Level 8"]

    title_text = font_title.render(title_label, True, (40, 80, 40))
    title_shadow = font_title.render(title_label, True, (100, 140, 100))
    subtitle_text = font_subtitle.render(subtitle_label, True, (40, 80, 40))
    subtitle_shadow = font_subtitle.render(subtitle_label, True, (100, 140, 100))
    title_rect = title_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 70))
    subtitle_rect = subtitle_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 125))
    screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
    screen.blit(title_text, title_rect)
    screen.blit(subtitle_shadow, (subtitle_rect.x + 1, subtitle_rect.y + 1))
    screen.blit(subtitle_text, subtitle_rect)

    # Level tlačidlá
    buttons = []

    for i, lvl in enumerate(level_names):
        rect = pygame.Rect(0, 0, 220, 65)
        rect.center = (popup_rect.centerx, popup_rect.top + 200 + i * 75)
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
