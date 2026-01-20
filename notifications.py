
#Notifikácie a popup okná pre hru

import pygame
from level_data import LEVEL_DATA

def draw_popup(screen, title, lines, button_text="OK", width=500, height=None):

    # Vykreslí popup okno s titulom, textom a tlačidlom

    screen_width, screen_height = screen.get_size()
    
    # Fonty pre výpočet šírky textu
    title_font = pygame.font.SysFont("Consolas", 32, bold=True)
    text_font = pygame.font.SysFont("Consolas", 18)
    button_font = pygame.font.SysFont("Consolas", 20, bold=True)
    
    # Vypočíta šírku na základe najdlhšieho textu
    padding = 40  # Padding na oboch stranách
    min_width = 300  # Minimálna šírka
    
    # Šírka titulu
    title_width = title_font.size(title)[0]
    
    # Šírka najdlhšieho riadku textu
    max_line_width = 0
    for line in lines:
        if line:  # Preskočí prázdne riadky
            line_width = text_font.size(line)[0]
            max_line_width = max(max_line_width, line_width)
    
    # Šírka tlačidla (text + padding)
    button_text_width = button_font.size(button_text)[0]
    button_width = max(120, button_text_width + 20)  # Minimálna šírka tlačidla 120
    
    # Najväčšia šírka z titulu, textu a tlačidla
    max_content_width = max(title_width, max_line_width, button_width)
    
    # Ak nie je zadaná šírka, vypočíta ju automaticky
    if width == 500:  # Default hodnota
        width = max(min_width, max_content_width + padding * 2)
    else:
        # Ak je zadaná šírka, použije ju, ale skontroluje, či je dostatočná
        width = max(width, max_content_width + padding * 2)
    
    # Vypočíta výšku na základe počtu riadkov
    if height is None:
        title_height = 50
        line_height = 30
        button_height = 50
        height = title_height + len(lines) * line_height + button_height + padding * 2
    
    # Centruje popup na obrazovke
    popup_x = (screen_width - width) // 2
    popup_y = (screen_height - height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, width, height)
    
    # Pozadie popup okna - výrazná žltá
    pygame.draw.rect(screen, (255, 220, 100), popup_rect, border_radius=15)
    pygame.draw.rect(screen, (220, 160, 40), popup_rect, width=4, border_radius=15)  # Tmavšia oranžová okraj
    
    # TIEŇ - tmavá oranžová/hnedá
    shadow_rect = popup_rect.move(6, 6)
    shadow_surf = pygame.Surface((width, height))
    shadow_surf.set_alpha(150)
    shadow_surf.fill((180, 120, 40))  # Tmavá oranžová tieň
    screen.blit(shadow_surf, shadow_rect)
    
    # Titul - tmavá oranžová
    title_surf = title_font.render(title, True, (0,0,0))  # Tmavá oranžová
    title_rect = title_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 30))
    screen.blit(title_surf, title_rect)
    
    # Textové riadky - tmavá hnedá
    y_offset = popup_rect.y + 70
    for line in lines:
        text_surf = text_font.render(line, True, (0,0,0))  
        text_rect = text_surf.get_rect(center=(popup_rect.centerx, y_offset))
        screen.blit(text_surf, text_rect)
        y_offset += 30
    
    # Tlačidlo OK
    button_width = 120
    button_height = 45
    button_x = popup_rect.centerx - button_width // 2
    button_y = popup_rect.bottom - button_height - 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # TIEŇ tlačidla - tmavá oranžová
    button_shadow = button_rect.move(3, 3)
    shadow_btn_surf = pygame.Surface((button_width, button_height))
    shadow_btn_surf.set_alpha(180)
    shadow_btn_surf.fill((200, 140, 40))  # Tmavá oranžová tieň
    screen.blit(shadow_btn_surf, button_shadow)
    
    # Tlačidlo - výrazná oranžová
    mouse_pos = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(mouse_pos)
    button_color = (255, 180, 60) if hovered else (255, 160, 40)  # Svetlejšia oranžová pri hover
    pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
    pygame.draw.rect(screen, (220, 140, 20), button_rect, width=3, border_radius=8)  # Tmavá oranžová okraj
    
    # Text tlačidla - biela pre kontrast
    button_font = pygame.font.SysFont("Consolas", 20, bold=True)
    button_text_surf = button_font.render(button_text, True, (255, 255, 255))  # Biela text
    button_text_rect = button_text_surf.get_rect(center=button_rect.center)
    screen.blit(button_text_surf, button_text_rect)
    
    return popup_rect, button_rect

def get_level_info(level_num):
    #Vráti informácie o leveli pre popup
    if level_num not in LEVEL_DATA:
        return f"Level {level_num}", ["Informácie nie sú dostupné"]
    
    level_data = LEVEL_DATA[level_num]
    obstacles_count = len(level_data.get("obstacles", []))
    goal = level_data.get("goal", (0, 0))
    
    info_texts = {
        1: ["Vitaj v prvom leveli!", f"Tvoj cieľ je dostať sa na pozíciu {goal}.", 
            f"Na ceste sú {obstacles_count} prekážky.", "Použij príkazy UP, DOWN, LEFT, RIGHT."],
        2: ["Level 2 - FOR cykly!", "For cyklus sa používa na opakovanie príkazov.",
            "Slúži na skrátenie zápisu príkazov.", "Pretiahni FOR do konzoly a vyber počet opakovaní."],
        3: ["Level 3 - IF podmienka", "IF sa používa na podmienkové vykonávanie príkazov.",
            "Pomocou IF môžeš skontrolovať, či je na danom mieste prekážka.", "Použij príkazy UP, DOWN, LEFT, RIGHT, IF."],
        4: ["Level 4 - Zložitejšia cesta!", f"Cieľ: pozícia {goal}",
            f"Na ceste je {obstacles_count} prekážok.", "Využij FOR cykly a IF/ELSE na efektívnejšie riešenie."],
        5: ["Level 5 - Finálny level!", f"Cieľ: pozícia {goal}",
            f"Pozor na {obstacles_count} prekážok!", "Dokážeš to?"]
    }
    
    return f"Level {level_num}", info_texts.get(level_num, [f"Cieľ: pozícia {goal}", f"Prekážky: {obstacles_count}"])

def draw_level_info_popup(screen, level_num):
    """Vykreslí popup s informáciami o leveli"""
    title, lines = get_level_info(level_num)
    return draw_popup(screen, title, lines, "Začať")

def draw_victory_popup(screen, level_num, next_level_num=None):
    """Vykreslí popup pri výhre"""
    title = f"Level {level_num} dokončený!"
    
    # Skontroluje, či existuje ďalší level
    if next_level_num is not None:
        lines = [
            "Gratulujeme!",
            "Úspešne si dokončil level.",
            "",
            f"Môžeš pokračovať na Level {next_level_num}"
        ]
        button_text = f"Level {next_level_num}"
    else:
        lines = [
            "Gratulujeme!",
            "Úspešne si dokončil všetky levely!",
            "",
            "Hra dokončená!"
        ]
        button_text = "OK"
    
    return draw_popup(screen, title, lines, button_text)

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

def draw_error_popup(screen, error_message):
    #Vykreslí popup s error správou
    title = "Chyba!"
    lines = error_message.split("\n")
    return draw_popup(screen, title, lines, "OK")
