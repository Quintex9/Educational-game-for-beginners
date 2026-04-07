# Stars and scoring

from UI.star_emoji import draw_star_emoji
from rendering.popups import draw_popup
import pygame


def calculate_stars(game_state):
    level_num = game_state.level_num

    if 5 <= level_num <= 8:
        if game_state.text_mode and game_state.used_text_mode_only:
            return 3
        if game_state.text_mode:
            return 2
        return 1

    command_count = game_state.total_commands_used
    reset_count = game_state.reset_count
    commands = game_state.total_commands_list
    has_for = any(cmd.command == "for_start" for cmd in commands)
    has_if = any(cmd.command == "if" for cmd in commands)

    if level_num == 1:
        if command_count <= 6 and reset_count == 0:
            return 3
        if command_count <= 10 and reset_count <= 1:
            return 2
        return 1

    if level_num == 2:
        if has_for and command_count <= 14 and reset_count == 0:
            return 3
        if (has_for and command_count <= 19) or (not has_for and command_count <= 20):
            return 2
        return 1

    if level_num == 3:
        if has_if and command_count <= 12 and reset_count == 0:
            return 3
        if (has_if and command_count <= 15):
            return 2
        return 1

    if level_num == 4:
        if has_for and has_if and command_count <= 13 and reset_count == 0:
            return 3
        if (has_for and has_if and command_count <= 18) or (has_if and not has_for and command_count <= 25):
            return 2
        return 1

    return 1


def draw_stars(screen, stars, center_x, y):
    star_size = 38
    spacing = 10
    total_width = 3 * star_size + 2 * spacing
    start_x = center_x - total_width // 2

    for i in range(3):
        cx = start_x + i * (star_size + spacing) + star_size // 2
        cy = y + star_size // 2
        alpha = 255 if i < stars else 85
        draw_star_emoji(screen, (cx, cy), star_size, alpha=alpha)


def draw_victory_popup(screen, level_num, next_level_num=None, stars=0):
    title = f"Level {level_num} dokončený!"

    if next_level_num is not None:
        lines = ["Gratulujeme!", "Úspešne si dokončil level.", ""]
        button_text = f"Level {next_level_num}"
    else:
        lines = ["Gratulujeme!", "Úspešne si dokončil všetky levely!", ""]
        button_text = None  # bez základného tlačidla, nahradíme dvojicou MENU/KONIEC

    popup_rect, button_rect = draw_popup(screen, title, lines, button_text)
    
    # Pre level 8 (posledný level): vykresli aj dvojicu tlačidiel MENU a KONIEC
    # a vráť ich recty ako tretí prvok (alebo None inde).
    extra_button_rect = None
    if next_level_num is None and level_num == 8:
        button_font = pygame.font.SysFont("Consolas", 20, bold=True)
        btn_w, btn_h = 140, 45
        spacing = 24
        total_w = btn_w * 2 + spacing
        start_x = popup_rect.centerx - total_w // 2
        y = popup_rect.bottom - btn_h - 22
        
        # MENU tlačidlo (vľavo)
        menu_rect = pygame.Rect(start_x, y, btn_w, btn_h)
        # KONIEC tlačidlo (vpravo)
        quit_rect = pygame.Rect(start_x + btn_w + spacing, y, btn_w, btn_h)
        
        mouse_pos = pygame.mouse.get_pos()
        for rect, text in [(menu_rect, "MENU"), (quit_rect, "KONIEC")]:
            hovered = rect.collidepoint(mouse_pos)
            color = (255, 180, 60) if hovered else (255, 160, 40)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (220, 140, 20), rect, width=3, border_radius=8)
            txt = button_font.render(text, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=rect.center))
        
        # Použijeme tuple na odovzdanie oboch rectov cez jeden parameter
        extra_button_rect = (menu_rect, quit_rect)
        
        star_h = 38
        stars_y = y - star_h
        draw_stars(screen, stars, popup_rect.centerx, stars_y)
    else:
        # Vypočítaj pozíciu hviezd
        text_block_bottom_y = popup_rect.y + 70 + len(lines) * 30
        default_stars_y = text_block_bottom_y + 10
        if button_rect is not None:
            stars_y = min(button_rect.y - 55, default_stars_y)
        else:
            stars_y = default_stars_y
        draw_stars(screen, stars, popup_rect.centerx, stars_y)
    
    return popup_rect, button_rect, extra_button_rect


def draw_stars_info_popup(screen, level_num):
    title = "Hodnotenie hviezdičkami"

    if 5 <= level_num <= 8:
        lines = [
            "⭐ ⭐ ⭐ - Použi LEN textovy rezim",
            "⭐ ⭐ - Použi textovy + drag & drop",
            "⭐ - Použi len drag & drop",
        ]
    elif level_num == 1:
        lines = [
            "⭐ ⭐ ⭐ - najviac 6 príkazov, 0 resetov",
            "⭐ ⭐ - najviac 10 príkazov a najviac 1 reset",
            "⭐ - použi viac ako 10 príkazov",
            "",
            "Tip: Skús nájsť čo najlepšie riešenie.",
        ]
    elif level_num == 2:
        lines = [
            "⭐ ⭐ ⭐ - použi FOR cyklus, najviac 14 príkazov a 0 resetov",
            "⭐ ⭐ - použi FOR cyklus a najviac 19 príkazov",
            "   alebo bez FOR cyklu najviac 20 príkazov",
            "⭐ - použi viac príkazov",
            "",
            "Tip: Skús si pomôcť FOR cyklom!",
        ]
    elif level_num == 3:
        lines = [
            "⭐ ⭐ ⭐ - použi IF podmienku, najviac 12 príkazov a 0 resetov",
            "⭐ ⭐ - použi IF podmienku a najviac 15 príkazov",
            "⭐ - použi viac príkazov",
            "",
            "Tip: Skús si pomôcť IF podmienkou!",
        ]
    elif level_num == 4:
        lines = [
            "⭐ ⭐ ⭐ - použi FOR cyklus, IF podmienku, najviac 13 príkazov a 0 resetov",
            "⭐ ⭐ - použi FOR cyklus a IF podmienku a najviac 18 príkazov",
            "   alebo použi len IF podmienku a najviac 25 príkazov",
            "⭐ - použi viac príkazov",
            "",
            "Tip: Kombinuj FOR a IF!",
        ]
    else:
        lines = [
            "Hodnotenie sa pocita podla",
            "poctu prikazov a optimalizacie.",
        ]

    return draw_popup(screen, title, lines, "OK", width=450)
