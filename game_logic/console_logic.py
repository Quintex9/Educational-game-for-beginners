# Console logic - indentation, for loops, popup helpers

from UI.draggable_button import draggableButton
from utils.settings import (
    CONSOLE_BUTTON_WIDTH,
    CONSOLE_LAYOUT_BUTTON_WIDTH,
    CONSOLE_LAYOUT_MAX_INDENT,
    CONSOLE_COLUMN_SPACING,
    CONSOLE_INDENT_WIDTH,
    CONSOLE_PADDING,
    CONSOLE_SLOT_HEIGHT,
)


def _calculate_positions(commands, console_rect, indent_levels):
    start_x = console_rect.x + CONSOLE_PADDING
    start_y = console_rect.y + CONSOLE_PADDING

    if not commands:
        return

    available_height = console_rect.height - CONSOLE_PADDING * 2
    max_per_col = max(1, available_height // CONSOLE_SLOT_HEIGHT)
    total_columns = (len(commands) + max_per_col - 1) // max_per_col

    # Build columns first, then size each column by its real widest button+indent.
    columns = [[] for _ in range(total_columns)]
    for i, cmd in enumerate(commands):
        column = i // max_per_col
        row = i % max_per_col
        columns[column].append((i, row, cmd))

    column_start_x = []
    next_start_x = start_x
    for entries in columns:
        column_start_x.append(next_start_x)
        content_width = max(
            indent_levels[idx] * CONSOLE_INDENT_WIDTH + cmd.rect.width for idx, _, cmd in entries
        )
        next_start_x += content_width + CONSOLE_COLUMN_SPACING

    for col_idx, entries in enumerate(columns):
        base_x = column_start_x[col_idx]
        for idx, row, cmd in entries:
            cmd.rect.x = base_x + indent_levels[idx] * CONSOLE_INDENT_WIDTH
            cmd.rect.y = start_y + row * CONSOLE_SLOT_HEIGHT


def update_console_indentation(commands, console_rect):
    indent_level = 0
    indent_levels = []
    i = 0

    while i < len(commands):
        cmd = commands[i]

        if cmd.command == "for_start":
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)
            indent_level += 1

        elif cmd.command == "for_end":
            indent_level = max(0, indent_level - 1)
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)

        elif cmd.command == "if":
            # IF itself has current indentation, but must not shift all following commands.
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)

            # If immediate next command is break_obstacle, indent only that one by +1.
            if i + 1 < len(commands) and commands[i + 1].command == "break_obstacle":
                i += 1
                break_cmd = commands[i]
                break_cmd.indent_level = indent_level + 1
                indent_levels.append(indent_level + 1)

        else:
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)

        i += 1

    _calculate_positions(commands, console_rect, indent_levels)


def expand_for_loops(commands):
    result, i = [], 0
    while i < len(commands):
        if commands[i].command == "for_start":
            loop_count, loop_commands, i = commands[i].loop_count, [], i + 1
            while i < len(commands) and commands[i].command != "for_end":
                loop_commands.append(commands[i])
                i += 1
            if i < len(commands):
                i += 1
            result.extend(loop_commands * loop_count)
        else:
            if commands[i].command != "for_end":
                result.append(commands[i])
            i += 1
    return result


def setup_console_command_position(cmd, console_rect, index):
    start_x = console_rect.x + CONSOLE_PADDING
    start_y = console_rect.y + CONSOLE_PADDING
    max_per_col = max(1, (console_rect.height - CONSOLE_PADDING * 2) // CONSOLE_SLOT_HEIGHT)
    col_width = CONSOLE_BUTTON_WIDTH + CONSOLE_COLUMN_SPACING
    cmd.rect.x = start_x + (index // max_per_col) * col_width
    cmd.rect.y = start_y + (index % max_per_col) * CONSOLE_SLOT_HEIGHT


def create_console_command(dragging_button):
    new_btn = draggableButton(
        dragging_button.rect.x,
        dragging_button.rect.y,
        100,
        50,
        dragging_button.label,
        dragging_button.command,
    )
    new_btn.loop_count = dragging_button.loop_count
    new_btn.condition = getattr(dragging_button, "condition", None)

    if new_btn.command == "for_start":
        new_btn.loop_count = 2
        new_btn.label = "FOR"
    elif new_btn.command == "if":
        new_btn.label = "IF"
        new_btn.condition = None
    return new_btn


def validate_for_loops(commands):
    #kontrola, ci je command list prazdny
    if not commands:
        return True, ""

    i = 0
    while i < len(commands):
        cmd = commands[i]

        if cmd.command == "for_start":
            i += 1
            loop_commands = []
            found_end = False

            while i < len(commands):
                if commands[i].command == "for_end":
                    found_end = True
                    i += 1
                    break
                if commands[i].command == "for_start":
                    return False, "Vnorené cykly nie sú povolene!\n\nNemožno použiť FOR\nv rámci iného FOR cyklu."

                loop_commands.append(commands[i])
                i += 1

            if not found_end:
                return False, "FOR cyklus nie je uzavretý!\n\nKaždý FOR cyklus musí\nbyť uzavretý pomocou END."

            if len(loop_commands) == 0:
                return False, "FOR cyklus je prázdný!\n\nMedzi FOR a END musí\nbyť aspoň jeden príkaz."
        else:
            i += 1

    for_count = 0
    end_count = 0
    for cmd in commands:
        if cmd.command == "for_start":
            for_count += 1
        elif cmd.command == "for_end":
            end_count += 1
            if end_count > for_count:
                return False, "Prílis vela END príkazov!\n\nKaždý END musí mať\nsvoj zodpovedajúci FOR."

    if for_count != end_count:
        return False, "Nesprávny počet FOR a END!\n\nPočet FOR a END príkazov\nmusí byť rovnaký."

    return True, ""


def would_exceed_console_limit(commands, console_rect, level_num):
    start_x = console_rect.x + CONSOLE_PADDING
    available_height = console_rect.height - CONSOLE_PADDING * 2
    max_commands_per_column = max(1, available_height // CONSOLE_SLOT_HEIGHT)
    new_index = len(commands)

    if level_num >= 2:
        indent_level = sum(1 for cmd in commands if cmd.command == "for_start") - sum(
            1 for cmd in commands if cmd.command == "for_end"
        )
        indent_level = max(0, indent_level)

        layout_button_width = max(CONSOLE_BUTTON_WIDTH, CONSOLE_LAYOUT_BUTTON_WIDTH)
        layout_indent = max(0, CONSOLE_LAYOUT_MAX_INDENT)
        column_width = layout_button_width + layout_indent * CONSOLE_INDENT_WIDTH + CONSOLE_COLUMN_SPACING
        current_column = new_index // max_commands_per_column
        x_pos = start_x + indent_level * CONSOLE_INDENT_WIDTH + current_column * column_width
    else:
        layout_button_width = max(CONSOLE_BUTTON_WIDTH, CONSOLE_LAYOUT_BUTTON_WIDTH)
        column_width = layout_button_width + CONSOLE_COLUMN_SPACING
        column = new_index // max_commands_per_column
        x_pos = start_x + column * column_width

    layout_button_width = max(CONSOLE_BUTTON_WIDTH, CONSOLE_LAYOUT_BUTTON_WIDTH)
    return x_pos + layout_button_width > console_rect.right
