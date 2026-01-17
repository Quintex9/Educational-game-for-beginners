
#Notifikácie a popup okná pre hru

import pygame
from level_data import LEVEL_DATA

def draw_popup(screen, title, lines, button_text="OK", width=500, height=None):

    # Vykreslí popup okno s titulom, textom a tlačidlom

    screen_width, screen_height = screen.get_size()
    
    # Vypočíta výšku na základe počtu riadkov
    if height is None:
        title_height = 50
        line_height = 30
        button_height = 50
        padding = 40
        height = title_height + len(lines) * line_height + button_height + padding * 2
    
    # Centruje popup na obrazovke
    popup_x = (screen_width - width) // 2
    popup_y = (screen_height - height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, width, height)
    
    # Pozadie popup okna
    pygame.draw.rect(screen, (40, 50, 60), popup_rect, border_radius=15)
    pygame.draw.rect(screen, (70, 90, 110), popup_rect, width=3, border_radius=15)
    
    # TIEŇ
    shadow_rect = popup_rect.move(5, 5)
    shadow_surf = pygame.Surface((width, height))
    shadow_surf.set_alpha(100)
    shadow_surf.fill((0, 0, 0))
    screen.blit(shadow_surf, shadow_rect)
    
    # Titul
    title_font = pygame.font.SysFont("Consolas", 32, bold=True)
    title_surf = title_font.render(title, True, (240, 245, 250))
    title_rect = title_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 30))
    screen.blit(title_surf, title_rect)
    
    # Textové riadky
    text_font = pygame.font.SysFont("Consolas", 18)
    y_offset = popup_rect.y + 70
    for line in lines:
        text_surf = text_font.render(line, True, (200, 210, 220))
        text_rect = text_surf.get_rect(center=(popup_rect.centerx, y_offset))
        screen.blit(text_surf, text_rect)
        y_offset += 30
    
    # Tlačidlo OK
    button_width = 120
    button_height = 45
    button_x = popup_rect.centerx - button_width // 2
    button_y = popup_rect.bottom - button_height - 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # TIEŇ tlačidla
    button_shadow = button_rect.move(2, 2)
    pygame.draw.rect(screen, (0, 0, 0, 100), button_shadow, border_radius=8)
    
    # Tlačidlo
    mouse_pos = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(mouse_pos)
    button_color = (80, 150, 220) if hovered else (60, 120, 180)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
    pygame.draw.rect(screen, (100, 170, 240), button_rect, width=2, border_radius=8)
    
    # Text tlačidla
    button_font = pygame.font.SysFont("Consolas", 20, bold=True)
    button_text_surf = button_font.render(button_text, True, (240, 245, 250))
    button_text_rect = button_text_surf.get_rect(center=button_rect.center)
    screen.blit(button_text_surf, button_text_rect)
    
    return popup_rect, button_rect

def get_level_info(level_num):
    # Vráti informácie o leveli pre popup
    if level_num not in LEVEL_DATA:
        return f"Level {level_num}", ["Informácie nie sú dostupné"]
    
    level_data = LEVEL_DATA[level_num]
    obstacles_count = len(level_data.get("obstacles", []))
    goal = level_data.get("goal", (0, 0))
    
    title = f"Level {level_num}"
    lines = []
    
    if level_num == 1:
        lines.append("Vitaj v prvom leveli!")
        lines.append("Tvoj cieľ je dostať sa na pozíciu (3, 3).")
        lines.append(f"Na ceste sú {obstacles_count} prekážky.")
        lines.append("Použij príkazy UP, DOWN, LEFT, RIGHT.")
    elif level_num == 2:
        lines.append("Level 2 - FOR cykly!")
        lines.append("Teraz môžeš použiť FOR cykly.")
        lines.append(f"Tvoj cieľ: pozícia {goal}")
        lines.append(f"Pozor na {obstacles_count} prekážok!")
        lines.append("Pretiahni FOR do konzoly a vyber počet opakovaní.")
    elif level_num == 3:
        lines.append("Level 3 - Zložitejšia cesta!")
        lines.append(f"Cieľ: pozícia {goal}")
        lines.append(f"Na ceste je {obstacles_count} prekážok.")
        lines.append("Využij FOR cykly na efektívnejšie riešenie.")
    elif level_num == 4:
        lines.append("Level 4 - Finálny level!")
        lines.append(f"Cieľ: pozícia {goal}")
        lines.append(f"Pozor na {obstacles_count} prekážok!")
        lines.append("Dokážeš to?")
    else:
        lines.append(f"Cieľ: pozícia {goal}")
        lines.append(f"Prekážky: {obstacles_count}")
    
    return title, lines

def draw_level_info_popup(screen, level_num):
    """Vykreslí popup s informáciami o leveli"""
    title, lines = get_level_info(level_num)
    return draw_popup(screen, title, lines, "Začať")

def draw_victory_popup(screen, level_num):
    """Vykreslí popup pri výhre"""
    title = f"Level {level_num} dokončený!"
    lines = [
        "Gratulujeme!",
        "Úspešne si dokončil level.",
        "",
        "Môžeš pokračovať na ďalší level"
    ]
    return draw_popup(screen, title, lines, "OK")

def draw_limit_warning_popup(screen):
    """Vykreslí popup s upozornením o dosiahnutom limite príkazov"""
    title = "Dosiahnutý limit!"
    lines = [
        "Konzola je plná.",
        "Nemôžeš pridať viac príkazov.",
        "",
        "Môžeš zresetovať konzolu",
        "pomocou tlačidla RESET."
    ]
    return draw_popup(screen, title, lines, "OK")
