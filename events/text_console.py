# Eventy a logika pre textovú konzolu

import pygame
from utils.settings import TEXT_CONSOLE_MAX_CHARS
from UI.draggable_button import draggableButton
from game_logic.console_logic import validate_for_loops

def _count_for_loops(lines, up_to_index):
    """Počíta aktívne FOR cykly do daného indexu"""
    count = 0
    for i in range(up_to_index):
        line = lines[i].strip().lower()
        if line.startswith("for"):
            count += 1
        elif line == "end":
            count = max(0, count - 1)
    return count

def _find_last_for_index(lines, before_index):
    """Nájde index posledného FOR pred daným indexom"""
    for i in range(before_index - 1, -1, -1):
        if lines[i].strip().lower().startswith("for"):
            return i
    return None

def validate_text_command(text, line_index, all_lines):
    """Validuje príkaz v texte - vráti (is_valid, error_message)"""
    text = text.strip().lower()
    if not text:
        return True, None
    
    ERROR_MSG = "\n\nMôžeš resetovať konzolu\nalebo vymazať obsah pomocou BACKSPACE."
    
    # Validácia FOR
    if text.startswith("for"):
        count = _parse_for_count(text)
        if count < 2 or count > 6:
            return False, f"Neplatný počet opakovaní FOR: {count}\n\nPovolené hodnoty: 2-6{ERROR_MSG}"
        if _count_for_loops(all_lines, line_index) > 0:
            return False, f"Vnorené FOR cykly nie sú povolené!{ERROR_MSG}"
        return True, None
    
    # Povolené príkazy
    if text not in ["up", "down", "left", "right", "end"]:
        return False, f"Neplatný príkaz: {text}\n\nPovolené príkazy:\nup, down, left, right, for 2x-6x, end{ERROR_MSG}"
    
    # Validácia END
    if text == "end":
        if _count_for_loops(all_lines, line_index) == 0:
            return False, f"END bez príslušného FOR!{ERROR_MSG}"
        last_for = _find_last_for_index(all_lines, line_index)
        if last_for is not None:
            # Skontroluje, či medzi FOR a END sú nejaké príkazy
            has_commands = any(
                all_lines[i].strip().lower() not in ["", "for", "end"] 
                for i in range(last_for + 1, line_index)
            )
            if not has_commands:
                return False, f"FOR cyklus je prázdny!\n\nMedzi FOR a END musí\nbyť aspoň jeden príkaz.{ERROR_MSG}"
    
    return True, None

def _parse_for_count(text):
    """Extrahuje počet opakovaní z 'for 2x' formátu"""
    parts = text.split()
    if len(parts) > 1:
        try:
            count = int(parts[1].rstrip('xX'))
            return max(2, min(6, count))  # Clamp na 2-6
        except ValueError:
            pass
    return 2

def parse_text_to_commands(text):
    """Parsuje text na console_commands"""
    MOVE_COMMANDS = {"up": ("UP", "move_up"), "down": ("DOWN", "move_down"), 
                     "left": ("LEFT", "move_left"), "right": ("RIGHT", "move_right")}
    commands = []
    
    for line in text.strip().split('\n'):
        line_stripped = line.strip().lower()
        if not line_stripped:
            continue
        
        if line_stripped in MOVE_COMMANDS:
            label, cmd = MOVE_COMMANDS[line_stripped]
            commands.append(draggableButton(0, 0, 100, 50, label, cmd))
        elif line_stripped.startswith("for"):
            count = _parse_for_count(line_stripped)
            btn = draggableButton(0, 0, 100, 50, f"FOR {count}x", "for_start")
            btn.loop_count = count
            commands.append(btn)
        elif line_stripped == "end":
            commands.append(draggableButton(0, 0, 100, 50, "END", "for_end"))
    
    return commands

def _get_selection_range(game_state):
    """Vráti (start, end) výberu textu alebo (None, None)"""
    if game_state.text_console_selection_start is None or game_state.text_console_selection_end is None:
        return None, None
    return (min(game_state.text_console_selection_start, game_state.text_console_selection_end),
            max(game_state.text_console_selection_start, game_state.text_console_selection_end))

def _selected_text_length(game_state):
    start, end = _get_selection_range(game_state)
    return (end - start) if start is not None else 0

def _can_insert_chars(game_state, chars_to_insert):
    return (len(game_state.text_console_input) - _selected_text_length(game_state) + chars_to_insert) <= TEXT_CONSOLE_MAX_CHARS

def _clear_text_selection(game_state):
    game_state.text_console_selection_start = None
    game_state.text_console_selection_end = None

def _delete_selected_text(game_state):
    start, end = _get_selection_range(game_state)
    if start is None:
        return False
    game_state.text_console_input = game_state.text_console_input[:start] + game_state.text_console_input[end:]
    game_state.text_console_cursor_pos = start
    _clear_text_selection(game_state)
    return True

def _insert_text(game_state, inserted_text):
    if not _can_insert_chars(game_state, len(inserted_text)):
        return False

    _delete_selected_text(game_state)
    text = game_state.text_console_input
    pos = game_state.text_console_cursor_pos
    game_state.text_console_input = text[:pos] + inserted_text + text[pos:]
    game_state.text_console_cursor_pos += len(inserted_text)
    return True

def _validate_line_on_newline(game_state, line_index):
    """Validuje riadok pri prechode na nový riadok (medzera alebo Enter)"""
    lines = game_state.text_console_input.split('\n')
    
    if line_index < len(lines):
        current_line = lines[line_index]
        is_valid, error = validate_text_command(current_line, line_index, lines)
        if not is_valid:
            game_state.show_error = True
            game_state.error_message = error
        else:
            game_state.show_error = False
            game_state.error_message = ""

def _auto_indent_after_for(game_state):
    """Automaticky odsadí nový riadok po 'for' - volá sa len pri Enter"""
    text_before_cursor = game_state.text_console_input[:game_state.text_console_cursor_pos]
    lines = text_before_cursor.split('\n')
    
    # Skontroluje, či predchádzajúci riadok je "for" alebo "for 2x", atď.
    if len(lines) >= 2:
        prev_line = lines[-2].strip().lower()
        if prev_line.startswith("for"):
            # Skontroluje, či nový riadok už nie je odsadený
            current_line = lines[-1] if len(lines) > 0 else ""
            # Ak riadok už začína odsadením (4 medzery), nepridáva znovu
            if not current_line.startswith("    ") and _can_insert_chars(game_state, 4):
                # Pridá odsadenie (4 medzery) na začiatok nového riadku
                current_pos = game_state.text_console_cursor_pos
                game_state.text_console_input = (
                    game_state.text_console_input[:current_pos] + 
                    "    " + 
                    game_state.text_console_input[current_pos:]
                )
                game_state.text_console_cursor_pos += 4

def _auto_indent_for_end(game_state):
    """Automaticky nastaví 'end' na úroveň zodpovedajúceho 'for'"""
    text_before_cursor = game_state.text_console_input[:game_state.text_console_cursor_pos]
    lines = text_before_cursor.split('\n')
    
    if len(lines) > 0:
        current_line_full = lines[-1]
        current_line = current_line_full.strip().lower()
        # Skontroluje, či aktuálny riadok je "end"
        if current_line == "end":
            # Nájde zodpovedajúci "for" a zistí jeho úroveň odsadenia
            for_count = 0
            for i in range(len(lines) - 1, -1, -1):
                line_stripped = lines[i].strip().lower()
                if line_stripped == "end":
                    for_count += 1
                elif line_stripped.startswith("for"):
                    if for_count == 0:
                        # Našli sme zodpovedajúci "for"
                        for_line = lines[i]
                        indent_count = len(for_line) - len(for_line.lstrip())
                        end_stripped = current_line_full.strip()
                        new_end_line = " " * indent_count + end_stripped
                        
                        # Vypočítame pozície v texte
                        line_start_pos = sum(len(lines[j]) + 1 for j in range(len(lines) - 1))  # +1 pre \n
                        line_end_pos = line_start_pos + len(current_line_full)
                        
                        # Nahradíme aktuálny riadok
                        game_state.text_console_input = (
                            game_state.text_console_input[:line_start_pos] +
                            new_end_line +
                            game_state.text_console_input[line_end_pos:]
                        )
                        # Aktualizujeme pozíciu kurzora
                        game_state.text_console_cursor_pos = line_start_pos + len(new_end_line)
                        break
                    else:
                        for_count -= 1

def handle_text_console_keyboard(event, game_state):
    """Spracuje klávesnicové vstupy pre textovú konzolu"""
    if event.key == pygame.K_BACKSPACE:
        if not _delete_selected_text(game_state) and game_state.text_console_cursor_pos > 0:
            text = game_state.text_console_input
            game_state.text_console_input = text[:game_state.text_console_cursor_pos - 1] + text[game_state.text_console_cursor_pos:]
            game_state.text_console_cursor_pos -= 1
    elif event.key == pygame.K_DELETE:
        if not _delete_selected_text(game_state) and game_state.text_console_cursor_pos < len(game_state.text_console_input):
            text = game_state.text_console_input
            game_state.text_console_input = text[:game_state.text_console_cursor_pos] + text[game_state.text_console_cursor_pos + 1:]
    elif event.key == pygame.K_LEFT:
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_SHIFT:
            if game_state.text_console_selection_start is None:
                game_state.text_console_selection_start = game_state.text_console_cursor_pos
            if game_state.text_console_cursor_pos > 0:
                game_state.text_console_cursor_pos -= 1
            game_state.text_console_selection_end = game_state.text_console_cursor_pos
        else:
            _clear_text_selection(game_state)
            if game_state.text_console_cursor_pos > 0:
                game_state.text_console_cursor_pos -= 1
    elif event.key == pygame.K_RIGHT:
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_SHIFT:
            if game_state.text_console_selection_start is None:
                game_state.text_console_selection_start = game_state.text_console_cursor_pos
            if game_state.text_console_cursor_pos < len(game_state.text_console_input):
                game_state.text_console_cursor_pos += 1
            game_state.text_console_selection_end = game_state.text_console_cursor_pos
        else:
            _clear_text_selection(game_state)
            if game_state.text_console_cursor_pos < len(game_state.text_console_input):
                game_state.text_console_cursor_pos += 1
    elif event.key == pygame.K_a and (pygame.key.get_mods() & pygame.KMOD_CTRL):
        game_state.text_console_selection_start = 0
        game_state.text_console_selection_end = len(game_state.text_console_input)
        game_state.text_console_cursor_pos = len(game_state.text_console_input)
    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
        text_before = game_state.text_console_input[:game_state.text_console_cursor_pos]
        prev_line_index = len(text_before.split('\n')) - 1
        if prev_line_index >= 0:
            _validate_line_on_newline(game_state, prev_line_index)
        if _insert_text(game_state, '\n'):
            _auto_indent_after_for(game_state)
    elif event.key == pygame.K_SPACE:
        text_before = game_state.text_console_input[:game_state.text_console_cursor_pos]
        current_line_index = len(text_before.split('\n')) - 1
        if current_line_index >= 0:
            _validate_line_on_newline(game_state, current_line_index)
        _auto_indent_for_end(game_state)
        _insert_text(game_state, ' ')
    elif event.key not in (pygame.K_TAB, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL):
        if event.unicode and _insert_text(game_state, event.unicode):
            text_before = game_state.text_console_input[:game_state.text_console_cursor_pos]
            lines_before = text_before.split('\n')
            if lines_before and lines_before[-1].strip().lower() == "end":
                _auto_indent_for_end(game_state)

def handle_text_console_click(game_state, console_rect, mx, my):
    """Spracuje kliknutie na textovú konzolu"""
    if not (5 <= game_state.level_num <= 8 and game_state.text_mode):
        return False
    padding = 15
    text_area_rect = pygame.Rect(
        console_rect.x + padding, console_rect.y + padding,
        console_rect.width - 2 * padding, console_rect.height - 2 * padding
    )
    game_state.text_console_active = text_area_rect.collidepoint(mx, my)
    return True

def reset_text_console_input(game_state):
    game_state.text_console_input = ""
    game_state.text_console_cursor_pos = 0
    _clear_text_selection(game_state)

def start_text_mode_execution(game_state):
    if not game_state.text_console_input.strip() or game_state.executing_commands:
        return False

    lines = game_state.text_console_input.strip().split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        is_valid, error_msg = validate_text_command(stripped, i, lines)
        if not is_valid:
            game_state.show_error = True
            game_state.error_message = error_msg
            return True

    game_state.console_commands = parse_text_to_commands(game_state.text_console_input)
    is_valid, error_msg = validate_for_loops(game_state.console_commands)
    if not is_valid:
        game_state.show_error = True
        game_state.error_message = error_msg
        return True

    from events.level_events import run_command_queue
    run_command_queue(game_state, game_state.console_commands, expand_loops_required=True)
    game_state.text_console_input = ""
    game_state.text_console_cursor_pos = 0
    _clear_text_selection(game_state)
    return True
