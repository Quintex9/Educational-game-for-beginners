# Základné popup funkcie

import pygame
import math

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
    
    # Pozadie popup okna - tmavšia farba pre lepšiu viditeľnosť hviezdičiek
    pygame.draw.rect(screen, (220, 180, 60), popup_rect, border_radius=15)
    pygame.draw.rect(screen, (180, 120, 20), popup_rect, width=4, border_radius=15)  # Tmavšia oranžová okraj
    
    # Titul - tmavá oranžová
    title_surf = title_font.render(title, True, (0,0,0))  # Tmavá oranžová
    title_rect = title_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 30))
    screen.blit(title_surf, title_rect)
    
    # Textové riadky - tmavá hnedá
    y_offset = popup_rect.y + 70
    for line in lines:
        # Skontroluje, či riadok obsahuje emoji hviezdičky a nahradí ich nakreslenými
        if "⭐" in line:
            # Rozdelí riadok na časti pred a po hviezdičkách
            parts = line.split("⭐")
            x_pos = popup_rect.centerx
            # Vypočíta šírku všetkého textu bez hviezdičiek
            total_text_width = sum(text_font.size(part)[0] for part in parts)
            star_count = line.count("⭐")
            star_size = 18
            star_spacing = 4
            total_stars_width = star_count * star_size + (star_count - 1) * star_spacing if star_count > 0 else 0
            total_width = total_text_width + total_stars_width
            
            # Začne kresliť zľava
            x_start = popup_rect.centerx - total_width // 2
            
            current_x = x_start
            for i, part in enumerate(parts):
                if part:  # Ak je text pred hviezdičkami
                    part_surf = text_font.render(part, True, (0, 0, 0))
                    screen.blit(part_surf, (current_x, y_offset))
                    current_x += part_surf.get_width()
                
                # Ak nie sme na poslednom časti, nakreslí hviezdičku
                if i < len(parts) - 1:
                    # Vykreslí malú hviezdičku
                    star_center = (current_x + star_size // 2, y_offset + 9)
                    outer_radius = star_size // 2 - 1
                    inner_radius = outer_radius * 0.4
                    points = []
                    for j in range(10):
                        angle = (j * math.pi / 5) - math.pi / 2
                        if j % 2 == 0:
                            radius = outer_radius
                        else:
                            radius = inner_radius
                        px = star_center[0] + radius * math.cos(angle)
                        py = star_center[1] + radius * math.sin(angle)
                        points.append((int(px), int(py)))
                    # Jasnejšie zlaté hviezdičky pre lepšiu viditeľnosť na tmavšom pozadí
                    pygame.draw.polygon(screen, (255, 230, 50), points)
                    pygame.draw.polygon(screen, (255, 200, 0), points, width=2)
                    current_x += star_size + star_spacing
        else:
            # Normálny text bez hviezdičiek
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
