
# Eventy a logika pre textovu konzolu
import pygame
from UI.draggable_button import draggableButton
from game_logic.console_logic import validate_for_loops
from utils.settings import TEXT_CONSOLE_MAX_CHARS


# ------------------------ Parser / validacia ------------------------------


#spočítanie for loops
def _count_for_loops(lines, up_to_index):
    count = 0
    for i in range(up_to_index):
        line = lines[i].strip().lower()
        if line.startswith("for"):
            count += 1
        elif line == "end":
            count = max(0, count - 1)
    return count

#vráti pozíciu posledného for/None
#Akceptuje len "for <cislo>x", vráti int alebo None
def _parse_for_count(text):
    normalized = " ".join(text.strip().lower().split())
    parts = normalized.split()
    if len(parts) != 2 or parts[0] != "for":
        return None
    suffix = parts[1]
    if len(suffix) < 2 or not suffix.endswith("x"):
        return None
    number_part = suffix[:-1]
    if not number_part.isdigit():
        return None
    return int(number_part)

# Akceptuje len "if obstacle down/right/left/up. Vráti kľúč kondície "
def _parse_if_condition(text):
    normalized = " ".join(text.strip().lower().split())
    if normalized.startswith("if obstacle "):
        direction = normalized.replace("if obstacle ", "", 1)
    else:
        return None

    direction_to_condition = {
        "down": "obstacle_down",
        "right": "obstacle_right",
        "left": "obstacle_left",
        "up": "obstacle_up",
    }
    return direction_to_condition.get(direction)

# Vráti 2 veci - is_valid a error
def validate_text_command(text, line_index, all_lines):
    text = text.strip().lower()
    if not text:
        return True, None

    error_suffix = "\n\nMôžeš resetovať konzolu\nalebo vymazať obsah pomocou BACKSPACE."

    if text.startswith("for"):
        count = _parse_for_count(text)
        if count is None:
            return False, f"Neplatný FOR príkaz!\n\nPouži format: for 2x až for 6x{error_suffix}"
        if count < 2 or count > 6:
            return False, f"Neplatný počet opakovaní FOR: {count}\n\nPovolené hodnoty: 2-6{error_suffix}"
        if _count_for_loops(all_lines, line_index) > 0:
            return False, f"Vnorené FOR cykly nie sú povolené!{error_suffix}"
        return True, None

    if text.startswith("if"):
        condition = _parse_if_condition(text)
        if condition is None:
            return (
                False,
                "Neplatný IF príkaz!\n\nPouži jednu z možností:\n"
                "if obstacle down, if obstacle up, if obstacle left, if obstacle right"
                + error_suffix,
            )
        return True, None

    if text == "break obstacle":
        if line_index == 0:
            return (
                False,
                "Príkaz 'break obstacle' musí byť priamo pod IF príkazom." + error_suffix,
            )
        prev_line = all_lines[line_index - 1].strip().lower()
        if _parse_if_condition(prev_line) is None:
            return (
                False,
                "Príkaz 'break obstacle' musí byť priamo pod IF príkazom." + error_suffix,
            )
        return True, None

    if text not in ["up", "down", "left", "right", "end"]:
        return (
            False,
            "Neplatný príkaz: "
            + text
            + "\n\nPovolené príkazy:\n"
            + "up, down, left, right, for 2x-6x, "
            + "if obstacle down/up/left/right, break obstacle, end"
            + error_suffix,
        )

    if text == "end":
        if _count_for_loops(all_lines, line_index) == 0:
            return False, f"END bez príslušného FOR!{error_suffix}"

        last_for = None
        for i in range(line_index - 1, -1, -1):
            if all_lines[i].strip().lower().startswith("for"):
                last_for = i
                break
        if last_for is not None:
            has_commands = any(
                all_lines[i].strip().lower() not in ["", "for", "end"]
                for i in range(last_for + 1, line_index)
            )
            if not has_commands:
                return (
                    False,
                    "FOR cyklus je prázdný!\n\nMedzi FOR a END musí\nbyť aspoň jeden príkaz." + error_suffix,
                )

    return True, None


def parse_text_to_commands(text):
    move_commands = {
        "up": ("UP", "move_up"),
        "down": ("DOWN", "move_down"),
        "left": ("LEFT", "move_left"),
        "right": ("RIGHT", "move_right"),
    }
    commands = []

    for line in text.strip().split("\n"):
        line_stripped = line.strip().lower()
        if not line_stripped:
            continue

        if line_stripped in move_commands:
            label, cmd = move_commands[line_stripped]
            commands.append(draggableButton(0, 0, 100, 50, label, cmd))

        elif line_stripped.startswith("for"):
            count = _parse_for_count(line_stripped)
            if count is None:
                continue
            btn = draggableButton(0, 0, 100, 50, f"FOR {count}x", "for_start")
            btn.loop_count = count
            commands.append(btn)

        elif line_stripped.startswith("if"):
            condition = _parse_if_condition(line_stripped)
            if condition:
                direction = condition.replace("obstacle_", "")
                if_btn = draggableButton(0, 0, 190, 50, f"IF obstacle {direction}", "if")
                if_btn.condition = condition
                commands.append(if_btn)

                break_btn = draggableButton(0, 0, 160, 50, "break obstacle", "break_obstacle")
                break_btn.break_direction = direction
                commands.append(break_btn)

        elif line_stripped == "break obstacle":
            # V textovom mode je tento riadok infomačný/očakávaný pod IF
            continue

        elif line_stripped == "end":
            commands.append(draggableButton(0, 0, 100, 50, "END", "for_end"))

    return commands


# -------------------- Editovanie textu -----------------------------
def _get_selection_range(game_state):
    if game_state.text_console_selection_start is None or game_state.text_console_selection_end is None:
        return None, None
    return (
        min(game_state.text_console_selection_start, game_state.text_console_selection_end),
        max(game_state.text_console_selection_start, game_state.text_console_selection_end),
    )


def _clear_text_selection(game_state):
    game_state.text_console_selection_start = None
    game_state.text_console_selection_end = None


def _delete_selected_text(game_state):
    start, end = _get_selection_range(game_state)
    if start is None:
        return False
    game_state.text_console_input = (
        game_state.text_console_input[:start] + game_state.text_console_input[end:]
    )
    game_state.text_console_cursor_pos = start
    _clear_text_selection(game_state)
    return True

# Checkovanie limitu riadku. Medzere sa nerátajú

def _can_insert_chars(game_state, inserted_text):
    start, end = _get_selection_range(game_state)
    if start is None:
        start = game_state.text_console_cursor_pos
        end = game_state.text_console_cursor_pos

    new_text = (
        game_state.text_console_input[:start]
        + inserted_text
        + game_state.text_console_input[end:]
    )
    return all(len(line.lstrip()) <= TEXT_CONSOLE_MAX_CHARS for line in new_text.split("\n"))


def _insert_text(game_state, inserted_text):
    if not _can_insert_chars(game_state, inserted_text):
        return False

    _delete_selected_text(game_state)
    text = game_state.text_console_input
    pos = game_state.text_console_cursor_pos
    game_state.text_console_input = text[:pos] + inserted_text + text[pos:]
    game_state.text_console_cursor_pos += len(inserted_text)
    return True


# ---------------------------------- UX automatiky ------------------------------------------
def _validate_line_on_newline(game_state, line_index):
    lines = game_state.text_console_input.split("\n")
    if line_index < len(lines):
        current_line = lines[line_index]
        is_valid, error = validate_text_command(current_line, line_index, lines)
        if not is_valid:
            game_state.show_error = True
            game_state.error_message = error
        else:
            game_state.show_error = False
            game_state.error_message = ""


#Po stlačení ENTER pridaj odsadenie pre FOR a pre IF doplni break obstacle
def on_enter_postprocess(game_state):
    text_before_cursor = game_state.text_console_input[:game_state.text_console_cursor_pos]
    lines = text_before_cursor.split("\n")

    if len(lines) >= 2:
        prev_line = lines[-2].strip().lower()
        # Nepridávaj odsadenie ak predchádzajúci riadok je "end"
        if prev_line == "end":
            return
        if _parse_for_count(prev_line) is not None:
            current_line = lines[-1] if lines else ""
            if not current_line.startswith("    ") and _can_insert_chars(game_state, "    "):
                current_pos = game_state.text_console_cursor_pos
                game_state.text_console_input = (
                    game_state.text_console_input[:current_pos]
                    + "    "
                    + game_state.text_console_input[current_pos:]
                )
                game_state.text_console_cursor_pos += 4

    text_before_cursor = game_state.text_console_input[:game_state.text_console_cursor_pos]
    lines = text_before_cursor.split("\n")
    if len(lines) < 2:
        return

    prev_line = lines[-2].strip().lower()
    current_line = lines[-1].strip().lower()
    if _parse_if_condition(prev_line) is None or current_line:
        return

    if _can_insert_chars(game_state, "break obstacle"):
        _insert_text(game_state, "break obstacle")


def _auto_indent_for_end(game_state):
    text = game_state.text_console_input
    pos = game_state.text_console_cursor_pos
    line_start_pos = text.rfind("\n", 0, pos) + 1
    line_end_pos = text.find("\n", line_start_pos)
    if line_end_pos == -1:
        line_end_pos = len(text)

    current_line_full = text[line_start_pos:line_end_pos]
    if not current_line_full:
        return

    # Odstráň odsadenie a skontroluj obsah
    stripped_line = current_line_full.lstrip()
    # Odstráň aj medzery na konci pre kontrolu
    stripped_for_check = stripped_line.rstrip()
    current_line = stripped_for_check.lower()
    
    # Kontrola či riadok (po odstránení odsadenia a medzier) je presne "end"
    # Alebo či sa práve píše "end" (začína "end")
    if current_line != "end" and not current_line.startswith("end"):
        return

    # Ak riadok má odsadenie a obsahuje "end", odstráň odsadenie OKAMŽITE
    if current_line_full.startswith(" ") or current_line_full.startswith("\t"):
        # Vypočítaj novú pozíciu kurzora
        indent_size = len(current_line_full) - len(stripped_line)
        new_cursor_pos = pos - indent_size
        
        # Ak je riadok presne "end" (s možnými medzerami), nastav ho na "end"
        if current_line == "end":
            new_line = "end"
        else:
            # Ak sa práve píše "end", odstráň len odsadenie
            new_line = stripped_line
        
        # Nahraď riadok verziou bez odsadenia
        game_state.text_console_input = (
            text[:line_start_pos]
            + new_line
            + text[line_end_pos:]
        )
        # Uprav pozíciu kurzora
        if pos >= line_end_pos:
            game_state.text_console_cursor_pos = line_start_pos + len(new_line)
        else:
            # Kurzor bol v riadku - uprav ho relatívne
            game_state.text_console_cursor_pos = max(line_start_pos, new_cursor_pos)


def _normalize_previous_end_after_newline(game_state):
    text = game_state.text_console_input
    pos = game_state.text_console_cursor_pos

    if pos <= 0 or pos > len(text):
        return
    if text[pos - 1] != "\n":
        return

    prev_line_end = pos - 1
    prev_line_start = text.rfind("\n", 0, prev_line_end) + 1
    prev_line = text[prev_line_start:prev_line_end]
    if prev_line.strip().lower() != "end":
        return

    new_prev_line = "end"
    game_state.text_console_input = (
        text[:prev_line_start]
        + new_prev_line
        + text[prev_line_end:]
    )
    game_state.text_console_cursor_pos = pos + (len(new_prev_line) - len(prev_line))


def handle_text_console_keyboard(event, game_state):
    if event.key == pygame.K_BACKSPACE:
        if not _delete_selected_text(game_state) and game_state.text_console_cursor_pos > 0:
            text = game_state.text_console_input
            pos = game_state.text_console_cursor_pos
            game_state.text_console_input = text[: pos - 1] + text[pos:]
            game_state.text_console_cursor_pos -= 1

    elif event.key == pygame.K_DELETE:
        if not _delete_selected_text(game_state) and game_state.text_console_cursor_pos < len(game_state.text_console_input):
            text = game_state.text_console_input
            pos = game_state.text_console_cursor_pos
            game_state.text_console_input = text[:pos] + text[pos + 1 :]

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

    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        _auto_indent_for_end(game_state)
        text_before = game_state.text_console_input[:game_state.text_console_cursor_pos]
        prev_line_index = len(text_before.split("\n")) - 1
        if prev_line_index >= 0:
            _validate_line_on_newline(game_state, prev_line_index)
        
        # Kontrola limitu pred vložením nového riadka
        lines = game_state.text_console_input.split("\n")
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        if len(non_empty_lines) >= 13:
            error_suffix = "\n\nMôžeš resetovať konzolu\nalebo vymazať obsah pomocou BACKSPACE."
            game_state.show_error = True
            game_state.error_message = (
                f"Presiahol si hranicu konzoly!\n\n"
                f"Maximálny počet príkazov je 13.\n"
                f"Tvoj kód ma už {len(non_empty_lines)} príkazov."
                + error_suffix
            )
            return
        
        if _insert_text(game_state, "\n"):
            on_enter_postprocess(game_state)
            _normalize_previous_end_after_newline(game_state)

    elif event.key == pygame.K_SPACE:
        # Pri medzere nevalidujeme riadok, inak sa popup zobrazi prilis skoro
        # pri pisani prikazov ako "if obstacle down".
        _auto_indent_for_end(game_state)
        _insert_text(game_state, " ")

    elif event.key not in (
        pygame.K_TAB,
        pygame.K_LSHIFT,
        pygame.K_RSHIFT,
        pygame.K_LCTRL,
        pygame.K_RCTRL,
    ):
        if event.unicode and _insert_text(game_state, event.unicode):
            # Kontrola či sa píše "end" - normalizuj odsadenie okamžite
            _auto_indent_for_end(game_state)


def handle_text_console_click(game_state, console_rect, mx, my):
    if not (5 <= game_state.level_num <= 8 and game_state.text_mode):
        return False
    padding = 15
    text_area_rect = pygame.Rect(
        console_rect.x + padding,
        console_rect.y + padding,
        console_rect.width - 2 * padding,
        console_rect.height - 2 * padding,
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

    lines = game_state.text_console_input.strip().split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        is_valid, error_msg = validate_text_command(stripped, i, lines)
        if not is_valid:
            game_state.show_error = True
            game_state.error_message = error_msg
            return True

    # Kontrola limitu počtu riadkov príkazov (max 13 riadkov)
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    if len(non_empty_lines) > 13:
        error_suffix = "\n\nMôžeš resetovať konzolu\nalebo vymazať obsah pomocou BACKSPACE."
        game_state.show_error = True
        game_state.error_message = (
            f"Presiahol si hranicu konzoly!\n\n"
            f"Maximálny počet príkazov je 13.\n"
            f"Tvoj kód ma {len(non_empty_lines)} príkazov."
            + error_suffix
        )
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
