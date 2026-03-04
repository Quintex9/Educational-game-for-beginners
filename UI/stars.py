# Stars and scoring

from UI.star_emoji import draw_star_emoji
from rendering.popups import draw_popup


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
        if has_for and command_count <= 8 and reset_count == 0:
            return 3
        if (has_for and command_count <= 12) or (not has_for and command_count <= 15):
            return 2
        return 1

    if level_num == 3:
        if has_if and command_count <= 10 and reset_count == 0:
            return 3
        if (has_if and command_count <= 15) or (not has_if and command_count <= 20):
            return 2
        return 1

    if level_num == 4:
        if has_for and has_if and command_count <= 12 and reset_count == 0:
            return 3
        if ((has_for or has_if) and command_count <= 18) or (not has_for and not has_if and command_count <= 25):
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
    title = f"Level {level_num} dokonceny!"

    if next_level_num is not None:
        lines = ["Gratulujeme!", "Uspesne si dokoncil level.", ""]
        button_text = f"Level {next_level_num}"
    else:
        lines = ["Gratulujeme!", "Uspesne si dokoncil vsetky levely!", "", "Hra dokoncena!"]
        button_text = "OK"

    popup_rect, button_rect = draw_popup(screen, title, lines, button_text)
    stars_y = button_rect.y - 50
    draw_stars(screen, stars, popup_rect.centerx, stars_y)
    return popup_rect, button_rect


def draw_stars_info_popup(screen, level_num):
    title = "⭐ Hodnotenie hviezdickami"

    if 5 <= level_num <= 8:
        lines = [
            "⭐ ⭐ ⭐ - Pouzi LEN textovy rezim",
            "⭐ ⭐ - Pouzi textovy + drag&drop",
            "⭐ - Pouzi len drag&drop",
            "",
            "Tip: Prepni na textovy rezim",
            "pomocou tlacidla TEXT/DRAG",
        ]
    elif level_num == 1:
        lines = [
            "⭐ ⭐ ⭐ - <=6 prikazov, 0 resetov",
            "⭐ ⭐ - <=10 prikazov, <=1 reset",
            "⭐ - Viac ako 10 prikazov",
            "",
            "Tip: Pouzi efektivne riesenie",
        ]
    elif level_num == 2:
        lines = [
            "⭐ ⭐ ⭐ - FOR cyklus + <=8 prikazov",
            "⭐ ⭐ - FOR + <=12 prikazov",
            "   alebo bez FOR + <=15 prikazov",
            "⭐ - Viac prikazov",
            "",
            "Tip: Pouzi FOR cyklus!",
        ]
    elif level_num == 3:
        lines = [
            "⭐ ⭐ ⭐ - IF podmienka + <=10 prikazov",
            "⭐ ⭐ - IF + <=15 prikazov",
            "   alebo bez IF + <=20 prikazov",
            "⭐ - Viac prikazov",
            "",
            "Tip: Pouzi IF podmienku!",
        ]
    elif level_num == 4:
        lines = [
            "⭐ ⭐ ⭐ - FOR + IF + <=12 prikazov",
            "⭐ ⭐ - FOR alebo IF + <=18 prikazov",
            "   alebo bez FOR/IF + <=25 prikazov",
            "⭐ - Viac prikazov",
            "",
            "Tip: Kombinuj FOR a IF!",
        ]
    else:
        lines = [
            "Hodnotenie sa pocita podla",
            "poctu prikazov a optimalizacie.",
        ]

    return draw_popup(screen, title, lines, "OK", width=450)
