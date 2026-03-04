# Handlery pre výbery (FOR, IF, MOVE)

import pygame
from game_logic.console_logic import update_console_indentation
from utils.settings import FOR_OPTIONS, FOR_POPUP_WIDTH, MOVE_COMMANDS

def handle_selection_popup_click(game_state, mx, my, selection_active, command_type, options, popup_width):
    #Generická funkcia pre spracovanie kliknutí na popup výbery
    if selection_active is not None:
        cmd = game_state.console_commands[selection_active]
        
        # Vytvorí popup rect
        popup_rect = pygame.Rect(
            cmd.rect.x + cmd.rect.width + 10,
            cmd.rect.y,
            popup_width,
            len(options) * 40 + 10
        )
        
        # Kontrola kliknutia na možnosti
        for j, (text, value) in enumerate(options):
            option_rect = pygame.Rect(
                popup_rect.x + 5,
                popup_rect.y + 5 + j * 40,
                popup_rect.width - 10,
                35
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
                    # Zväčší šírku tlačidla pre dlhší text
                    cmd.rect.width = 190
                return True, None
        
        # Klikol mimo popup - zatvorí výber
        if not popup_rect.collidepoint(mx, my):
            return True, None
    
    return False, selection_active

def handle_for_selection_click(game_state, mx, my, console_rect):
    #Spracuje kliknutie na FOR výber popup
    if game_state.level_num < 2 or game_state.for_selection_active is None:
        # Kontrola kliknutia na FOR príkaz v konzole
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command == "for_start":
                game_state.for_selection_active = i
                return True
        return False
    
    cmd = game_state.console_commands[game_state.for_selection_active]
    if cmd.command != "for_start":
        game_state.for_selection_active = None
        return True
    
    clicked, _ = handle_selection_popup_click(game_state, mx, my,
                                               game_state.for_selection_active, "for", FOR_OPTIONS, FOR_POPUP_WIDTH)
    if clicked:
        update_console_indentation(game_state.console_commands, console_rect)
        game_state.for_selection_active = None
        return True
    return False

def handle_if_selection_click(game_state, mx, my, console_rect):
    #Spracuje kliknutie na IF výber popup
    if game_state.level_num < 3 or game_state.if_selection_active is None:
        # Kontrola kliknutia na IF príkaz v konzole
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command == "if":
                game_state.if_selection_active = i
                return True
        return False
    
    cmd = game_state.console_commands[game_state.if_selection_active]
    if cmd.command != "if":
        game_state.if_selection_active = None
        return True
    
    options = [
        ("obstacle down", "obstacle_down"),
        ("obstacle right", "obstacle_right"),
        ("obstacle left", "obstacle_left"),
        ("obstacle up", "obstacle_up")
    ]
    clicked, selected_value = handle_selection_popup_click(game_state, mx, my,
                                               game_state.if_selection_active, "if", options, 180)
    if clicked:
        if_index = game_state.if_selection_active
        update_console_indentation(game_state.console_commands, console_rect)
        # Ak už existuje break_obstacle hneď za IF, aktualizuje jeho smer
        if (if_index + 1 < len(game_state.console_commands) and 
            game_state.console_commands[if_index + 1].command == "break_obstacle"):
            break_cmd = game_state.console_commands[if_index + 1]
            direction = cmd.condition.replace("obstacle_", "")
            break_cmd.break_direction = direction
            update_console_indentation(game_state.console_commands, console_rect)
        else:
            # Vytvorí nový break_obstacle príkaz a vloží ho za IF
            from UI.draggable_button import draggableButton
            break_cmd = draggableButton(0, 0, 160, 50, "break obstacle", "break_obstacle")
            break_cmd.condition = None
            break_cmd.loop_count = 2
            direction = cmd.condition.replace("obstacle_", "")
            break_cmd.break_direction = direction
            game_state.console_commands.insert(if_index + 1, break_cmd)
            update_console_indentation(game_state.console_commands, console_rect)
        game_state.if_selection_active = None
        return True
    return False

def handle_move_selection_click(game_state, mx, my, console_rect):
    #Spracuje kliknutie na výber pohybového príkazu
    if game_state.move_selection_active is None:
        # Kontrola kliknutia na pohybový príkaz v konzole
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command in MOVE_COMMANDS:
                game_state.move_selection_active = i
                return True
        return False
    
    cmd = game_state.console_commands[game_state.move_selection_active]
    if cmd.command not in MOVE_COMMANDS:
        game_state.move_selection_active = None
        return True
    
    # Vytvorí zoznam možností bez aktuálneho príkazu
    options = [(MOVE_COMMANDS[move_cmd], move_cmd) 
               for move_cmd in MOVE_COMMANDS if move_cmd != cmd.command]
    
    clicked, _ = handle_selection_popup_click(game_state, mx, my,
                                               game_state.move_selection_active, "move", options, 120)
    if clicked:
        if game_state.level_num >= 2:
            update_console_indentation(game_state.console_commands, console_rect)
        game_state.move_selection_active = None
        return True
    return False
