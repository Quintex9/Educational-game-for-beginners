# Handlers for selection popups (FOR, IF, MOVE)

import pygame
from game_logic.console_logic import update_console_indentation
from utils.popup_position import compute_selection_popup_rect
from utils.settings import FOR_OPTIONS, FOR_POPUP_WIDTH, MOVE_COMMANDS

#kontrola pravej strany
def _layout_exceeds_console(commands, console_rect):
    return any(cmd.rect.right > console_rect.right for cmd in commands)


def handle_selection_popup_click(game_state, mx, my, selection_active, command_type, options, popup_width):
    # Generic handler for popup option clicks.
    if selection_active is None or selection_active >= len(game_state.console_commands):
        return False, None

    cmd = game_state.console_commands[selection_active]

    surface = pygame.display.get_surface()
    bounds_rect = surface.get_rect() if surface is not None else pygame.Rect(0, 0, 10000, 10000)
    popup_rect = compute_selection_popup_rect(
        cmd.rect,
        popup_width,
        len(options) * 40 + 10,
        bounds_rect,
    )

    for j, (text, value) in enumerate(options):
        option_rect = pygame.Rect(
            popup_rect.x + 5,
            popup_rect.y + 5 + j * 40,
            popup_rect.width - 10,
            35,
        )
        if option_rect.collidepoint(mx, my):
            if command_type == "for":
                cmd.loop_count = value
                cmd.label = f"FOR {value}x"
            elif command_type == "move":
                cmd.command = value
                cmd.label = text
            elif command_type == "if":
                cmd.condition = value
                cmd.label = f"IF {text}"
                cmd.rect.width = 190
            return True, value

    # Click outside closes popup.
    if not popup_rect.collidepoint(mx, my):
        return True, None

    return False, None


def handle_for_selection_click(game_state, mx, my, console_rect):
    # Handle FOR popup clicks.
    if game_state.level_num < 2 or game_state.for_selection_active is None:
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command == "for_start":
                game_state.for_selection_active = i
                return True
        return False

    cmd = game_state.console_commands[game_state.for_selection_active]
    if cmd.command != "for_start":
        game_state.for_selection_active = None
        return True

    clicked, selected_value = handle_selection_popup_click(
        game_state,
        mx,
        my,
        game_state.for_selection_active,
        "for",
        FOR_OPTIONS,
        FOR_POPUP_WIDTH,
    )
    if clicked:
        if selected_value is not None:
            update_console_indentation(game_state.console_commands, console_rect)
        game_state.for_selection_active = None
        return True
    return False


def handle_if_selection_click(game_state, mx, my, console_rect):
    # Handle IF popup clicks.
    if game_state.level_num < 3 or game_state.if_selection_active is None:
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command == "if":
                game_state.if_selection_active = i
                return True
        return False

    if_index = game_state.if_selection_active
    cmd = game_state.console_commands[if_index]
    if cmd.command != "if":
        game_state.if_selection_active = None
        return True

    options = [
        ("obstacle down", "obstacle_down"),
        ("obstacle right", "obstacle_right"),
        ("obstacle left", "obstacle_left"),
        ("obstacle up", "obstacle_up"),
    ]

    prev_label = cmd.label
    prev_condition = cmd.condition
    prev_width = cmd.rect.width

    clicked, selected_value = handle_selection_popup_click(
        game_state, mx, my, if_index, "if", options, 180
    )
    if not clicked:
        return False

    # Zavrety popup bez vybratia hodnoty
    if selected_value is None:

        # Odstránenie IF
        if cmd.condition is None:
            game_state.console_commands.pop(if_index)
            if if_index < len(game_state.console_commands) and game_state.console_commands[if_index].command == "break_obstacle":
                game_state.console_commands.pop(if_index)
            update_console_indentation(game_state.console_commands, console_rect)
        game_state.if_selection_active = None
        return True

    direction = selected_value.replace("obstacle_", "")
    inserted_break = False
    break_cmd = None
    prev_break_direction = None

    if if_index + 1 < len(game_state.console_commands) and game_state.console_commands[if_index + 1].command == "break_obstacle":
        break_cmd = game_state.console_commands[if_index + 1]
        prev_break_direction = getattr(break_cmd, "break_direction", None)
        break_cmd.break_direction = direction
    else:
        from UI.draggable_button import draggableButton

        break_cmd = draggableButton(0, 0, 160, 50, "break obstacle", "break_obstacle")
        break_cmd.condition = None
        break_cmd.loop_count = 2
        break_cmd.break_direction = direction
        game_state.console_commands.insert(if_index + 1, break_cmd)
        inserted_break = True

    update_console_indentation(game_state.console_commands, console_rect)

    #Keby IF na kraji spôsobí overflow, rollback a ukáž limit popup
    if _layout_exceeds_console(game_state.console_commands, console_rect):
        cmd.label = prev_label
        cmd.condition = prev_condition
        cmd.rect.width = prev_width

        if inserted_break:
            game_state.console_commands.pop(if_index + 1)
        elif break_cmd is not None:
            break_cmd.break_direction = prev_break_direction

        update_console_indentation(game_state.console_commands, console_rect)
        game_state.show_limit_warning = True

    game_state.if_selection_active = None
    return True


def handle_move_selection_click(game_state, mx, my, console_rect):
    # Handle move command popup clicks.
    if game_state.move_selection_active is None:
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command in MOVE_COMMANDS:
                game_state.move_selection_active = i
                return True
        return False

    cmd = game_state.console_commands[game_state.move_selection_active]
    if cmd.command not in MOVE_COMMANDS:
        game_state.move_selection_active = None
        return True

    options = [(MOVE_COMMANDS[move_cmd], move_cmd) for move_cmd in MOVE_COMMANDS if move_cmd != cmd.command]

    clicked, selected_value = handle_selection_popup_click(
        game_state,
        mx,
        my,
        game_state.move_selection_active,
        "move",
        options,
        120,
    )
    if clicked:
        if selected_value is not None and game_state.level_num >= 2:
            update_console_indentation(game_state.console_commands, console_rect)
        game_state.move_selection_active = None
        return True
    return False
