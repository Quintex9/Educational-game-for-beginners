# Hviezdičky a hodnotenie

import pygame
import math
from rendering.popups import draw_popup

def calculate_stars(game_state):
    """Vypočíta počet hviezdičiek na základe výkonu"""
    level_num = game_state.level_num
    
    # Pre levely 5-8: hodnotenie podľa režimu
    if 5 <= level_num <= 8:
        if game_state.text_mode and game_state.used_text_mode_only:
            return 3  # Použili len textový režim
        elif game_state.text_mode:
            return 2  # Použili textový režim, ale aj drag&drop
        else:
            return 1  # Použili len drag&drop
    
    # Pre levely 1-4: hodnotenie podľa optimalizácie
    # Použije celkový počet príkazov použitých počas celého levelu
    command_count = game_state.total_commands_used
    reset_count = game_state.reset_count
    
    # Počíta použitie FOR a IF z celkového zoznamu príkazov
    commands = game_state.total_commands_list
    has_for = any(cmd.command == "for_start" for cmd in commands)
    has_if = any(cmd.command == "if" for cmd in commands)
    
    if level_num == 1:
        # Level 1: základný, bez FOR/IF
        if command_count <= 6 and reset_count == 0:
            return 3
        elif command_count <= 10 and reset_count <= 1:
            return 2
        else:
            return 1
    
    elif level_num == 2:
        # Level 2: ideálne na FOR
        if has_for and command_count <= 8 and reset_count == 0:
            return 3
        elif (has_for and command_count <= 12) or (not has_for and command_count <= 15):
            return 2
        else:
            return 1
    
    elif level_num == 3:
        # Level 3: vyžaduje IF
        if has_if and command_count <= 10 and reset_count == 0:
            return 3
        elif (has_if and command_count <= 15) or (not has_if and command_count <= 20):
            return 2
        else:
            return 1
    
    elif level_num == 4:
        # Level 4: zložitejší, ideálne FOR + IF
        if has_for and has_if and command_count <= 12 and reset_count == 0:
            return 3
        elif ((has_for or has_if) and command_count <= 18) or (not has_for and not has_if and command_count <= 25):
            return 2
        else:
            return 1
    
    # Fallback pre ostatné levely
    return 1

def draw_stars(screen, stars, center_x, y):
    """Vykreslí hviezdičky pomocou pygame"""
    star_size = 40
    spacing = 10
    total_width = 3 * star_size + 2 * spacing
    start_x = center_x - total_width // 2
    
    for i in range(3):
        x = start_x + i * (star_size + spacing)
        
        # Zlatá hviezdička ak je získaná, sivá ak nie
        if i < stars:
            fill_color = (255, 215, 0)  # Zlatá
            border_color = (255, 200, 0)
        else:
            fill_color = (150, 150, 150)  # Sivá
            border_color = (120, 120, 120)
        
        # Nakreslí hviezdu priamo pomocou pygame
        center = (x + star_size // 2, y + star_size // 2)
        outer_radius = star_size // 2 - 4
        inner_radius = outer_radius // 2
        
        points = []
        for j in range(10):
            angle = (j * math.pi / 5) - math.pi / 2
            if j % 2 == 0:
                radius = outer_radius
            else:
                radius = inner_radius
            px = center[0] + radius * math.cos(angle)
            py = center[1] + radius * math.sin(angle)
            points.append((int(px), int(py)))
        
        pygame.draw.polygon(screen, fill_color, points)
        pygame.draw.polygon(screen, border_color, points, width=2)

def draw_victory_popup(screen, level_num, next_level_num=None, stars=0):
    """Vykreslí popup pri výhre s hviezdičkami"""
    title = f"Level {level_num} dokončený!"
    
    # Skontroluje, či existuje ďalší level
    if next_level_num is not None:
        lines = ["Gratulujeme!", "Úspešne si dokončil level.", ""]
        button_text = f"Level {next_level_num}"
    else:
        lines = ["Gratulujeme!", "Úspešne si dokončil všetky levely!", "", "Hra dokončená!"]
        button_text = "OK"
    
    popup_rect, button_rect = draw_popup(screen, title, lines, button_text)
    
    # Vykreslí hviezdičky nad tlačidlom
    stars_y = button_rect.y - 50
    draw_stars(screen, stars, popup_rect.centerx, stars_y)
    
    return popup_rect, button_rect

def draw_stars_info_popup(screen, level_num):
    """Vykreslí popup s informáciami o tom, ako získať hviezdičky"""
    title = "⭐ Hodnotenie hviezdičkami"
    
    if 5 <= level_num <= 8:
        lines = [
            "⭐ ⭐ ⭐ - Použij LEN textový režim",
            "⭐ ⭐ - Použij textový + drag&drop",
            "⭐ - Použij len drag&drop",
            "",
            "Tip: Prepni na textový režim",
            "pomocou tlačidla TEXT/DRAG"
        ]
    elif level_num == 1:
        lines = [
            "⭐ ⭐ ⭐ - ≤6 príkazov, 0 resetov",
            "⭐ ⭐ - ≤10 príkazov, ≤1 reset",
            "⭐ - Viac ako 10 príkazov",
            "",
            "Tip: Použij efektívne riešenie"
        ]
    elif level_num == 2:
        lines = [
            "⭐ ⭐ ⭐ - FOR cyklus + ≤8 príkazov",
            "⭐ ⭐ - FOR + ≤12 príkazov",
            "   alebo bez FOR + ≤15 príkazov",
            "⭐ - Viac príkazov",
            "",
            "Tip: Použij FOR cyklus!"
        ]
    elif level_num == 3:
        lines = [
            "⭐ ⭐ ⭐ - IF podmienka + ≤10 príkazov",
            "⭐ ⭐ - IF + ≤15 príkazov",
            "   alebo bez IF + ≤20 príkazov",
            "⭐ - Viac príkazov",
            "",
            "Tip: Použij IF podmienku!"
        ]
    elif level_num == 4:
        lines = [
            "⭐ ⭐ ⭐ - FOR + IF + ≤12 príkazov",
            "⭐ ⭐ - FOR alebo IF + ≤18 príkazov",
            "   alebo bez FOR/IF + ≤25 príkazov",
            "⭐ - Viac príkazov",
            "",
            "Tip: Kombinuj FOR a IF!"
        ]
    else:
        lines = [
            "Hodnotenie sa počíta podľa",
            "počtu príkazov a optimalizácie."
        ]
    
    return draw_popup(screen, title, lines, "OK", width=450)
