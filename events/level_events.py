# Hlavné eventy pre level

import pygame
from UI.panel import panel_buttons
from game_logic.console_logic import (
    expand_for_loops, 
    update_console_indentation, 
    create_console_command,
    setup_console_command_position,
    would_exceed_console_limit,
    validate_for_loops
)
from events.text_console import handle_text_console_keyboard, handle_text_console_click, reset_text_console_input, start_text_mode_execution
from events.selection_handlers import handle_for_selection_click, handle_if_selection_click, handle_move_selection_click

def _validate_for_end_command(commands, new_command):
    #Validácia pre FOR/END príkazy pri pridaní
    if new_command == "for_start":
        in_loop = False
        for cmd in commands:
            if cmd.command == "for_start":
                in_loop = True
            elif cmd.command == "for_end":
                in_loop = False
        if in_loop:
            return "Vnorené cykly nie sú povolené!\n\nNemôžeš použiť FOR\nv rámci iného FOR cyklu."
    
    elif new_command == "for_end":
        for_count = sum(1 for cmd in commands if cmd.command == "for_start")
        end_count = sum(1 for cmd in commands if cmd.command == "for_end")
        if for_count <= end_count:
            return "Nemôžeš pridať END!\n\nEND musí mať\nsvoj zodpovedajúci FOR."
        
        last_for_index = next((i for i in range(len(commands)-1, -1, -1) 
                              if commands[i].command == "for_start"), None)
        if last_for_index is not None:
            if not commands[last_for_index+1:]:
                return "FOR cyklus je prázdny!\n\nMedzi FOR a END musí\nbyť aspoň jeden príkaz."
    return None

def run_command_queue(game_state, commands, expand_loops_required):
    # Pridá príkazy do celkového zoznamu pre hodnotenie
    game_state.total_commands_list.extend(commands.copy())
    game_state.total_commands_used += len(commands)
    
    expanded_commands = expand_for_loops(commands) if expand_loops_required else commands.copy()
    game_state.command_queue = expanded_commands.copy()
    game_state.console_commands.clear()
    game_state.executing_commands = True
    game_state.last_command_time = pygame.time.get_ticks() - game_state.command_delay

def _start_drag_mode_execution(game_state):
    if not game_state.console_commands or game_state.executing_commands:
        return False

    if game_state.level_num >= 2:
        is_valid, error_msg = validate_for_loops(game_state.console_commands)
        if not is_valid:
            game_state.show_error = True
            game_state.error_message = error_msg
            return True

    run_command_queue(game_state, game_state.console_commands, expand_loops_required=(game_state.level_num >= 2))
    return True

def _handle_start_click(game_state):
    if 5 <= game_state.level_num <= 8 and game_state.text_mode:
        return start_text_mode_execution(game_state)
    return _start_drag_mode_execution(game_state)

def _clear_runtime_execution_state(game_state):
    game_state.command_queue.clear()
    game_state.executing_commands = False
    game_state.for_selection_active = None
    game_state.if_selection_active = None
    game_state.move_selection_active = None

def _handle_popup_button_click(game_state, popup_button_rect):
    """Spracuje kliknutie na popup tlačidlo"""
    if not popup_button_rect:
        return False
    if game_state.show_victory and game_state.next_level_num is not None:
        next_level = game_state.next_level_num
        game_state.state = f"Level {next_level}"
        panel_buttons.clear()
        game_state.initialize_level(next_level)
        return True
    for flag in ['show_level_info', 'show_victory', 'show_limit_warning', 'show_error', 'show_stars_info']:
        if getattr(game_state, flag, False):
            setattr(game_state, flag, False)
            if flag == 'show_error':
                game_state.error_message = ""
            break
    return True

def _handle_mode_toggle_click(game_state, mode_toggle_button_rect):
    """Spracuje kliknutie na prepínač režimu"""
    if not mode_toggle_button_rect:
        return False
    
    # Ak prepnú z textového režimu na drag&drop, už nepoužili len textový režim
    if game_state.text_mode:
        game_state.used_text_mode_only = False
    
    game_state.text_mode = not game_state.text_mode
    game_state.console_commands.clear()
    reset_text_console_input(game_state)
    _clear_runtime_execution_state(game_state)
    return True

def _handle_reset_click(game_state, reset_button_rect):
    """Spracuje kliknutie na RESET tlačidlo"""
    if not reset_button_rect:
        return False
    
    # Zvýši počet resetov
    game_state.reset_count += 1
    
    if 5 <= game_state.level_num <= 8 and game_state.text_mode:
        reset_text_console_input(game_state)
        game_state.console_commands.clear()
    else:
        game_state.console_commands.clear()
    _clear_runtime_execution_state(game_state)
    game_state.show_error = False
    game_state.error_message = ""
    return True

def handle_level_events(event, game_state, console_rect, button_rect, reset_button_rect, menu_button_rect, dragging_button, popup_rect=None, popup_button_rect=None, mode_toggle_button_rect=None, stars_info_button_rect=None):
    # Spracuje eventy v level stave
    
    # Pre levely 5-8 v textovom režime - textová konzola
    if 5 <= game_state.level_num <= 8 and game_state.text_mode:
        if event.type == pygame.KEYDOWN and game_state.text_console_active:
            handle_text_console_keyboard(event, game_state)
            return dragging_button, None

    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        
        if popup_button_rect and popup_button_rect.collidepoint(mx, my):
            if _handle_popup_button_click(game_state, popup_button_rect):
                return dragging_button, None
        
        # Ak je popup zobrazený, ignoruj ostatné kliknutia
        if popup_rect and popup_rect.collidepoint(mx, my):
            return dragging_button, None
        
        if mode_toggle_button_rect and mode_toggle_button_rect.collidepoint(mx, my):
            if _handle_mode_toggle_click(game_state, mode_toggle_button_rect):
                return dragging_button, None
        
        if stars_info_button_rect and stars_info_button_rect.collidepoint(mx, my):
            # Ked je otvorene info o levele, tlacidlo hviezdiciek je docasne neaktivne.
            if game_state.show_level_info:
                return dragging_button, None
            game_state.show_stars_info = True
            return dragging_button, None
        
        handle_text_console_click(game_state, console_rect, mx, my)
        
        if reset_button_rect.collidepoint(mx, my):
            if _handle_reset_click(game_state, reset_button_rect):
                return dragging_button, None
        
        if menu_button_rect.collidepoint(mx, my):
            game_state.reset_to_menu()
            return None, None

        # START click handling
        if (button_rect.collidepoint(mx, my) and
            game_state.for_selection_active is None and
            game_state.if_selection_active is None and
            game_state.move_selection_active is None and
            not game_state.executing_commands and not game_state.level_completed):
            if _handle_start_click(game_state):
                return dragging_button, None

        # Drag&drop handling (len ak nie je popup a nie je textový režim)
        can_drag = (not menu_button_rect.collidepoint(mx, my) and 
                   not reset_button_rect.collidepoint(mx, my) and
                   not game_state.executing_commands and not game_state.level_completed and
                   not (5 <= game_state.level_num <= 8 and game_state.text_mode))
        
        if can_drag:
            if not any(cmd.rect.collidepoint(mx, my) for cmd in game_state.console_commands):
                for btn in panel_buttons:
                    if btn.start_drag((mx, my)):
                        dragging_button = btn
                        break
            
            # Kontrola výberov (FOR, IF, MOVE)
            if (game_state.level_num >= 2 and game_state.move_selection_active is None and 
                game_state.if_selection_active is None):
                if handle_for_selection_click(game_state, mx, my, console_rect):
                    return dragging_button, None
            
            if (game_state.level_num >= 3 and game_state.move_selection_active is None and 
                game_state.for_selection_active is None):
                if handle_if_selection_click(game_state, mx, my, console_rect):
                    return dragging_button, None
            
            if (game_state.for_selection_active is None and game_state.if_selection_active is None):
                if handle_move_selection_click(game_state, mx, my, console_rect):
                    return dragging_button, None
        
        return dragging_button, None
    
    elif event.type == pygame.MOUSEMOTION:
        if dragging_button:
            dragging_button.drag(event.pos)
        return dragging_button, None
    
    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging_button:
            dragging_button.stop_drag()
            if not popup_rect and console_rect.collidepoint(dragging_button.rect.center):
                if would_exceed_console_limit(game_state.console_commands, console_rect, game_state.level_num):
                    game_state.show_limit_warning = True
                else:
                    new_btn = create_console_command(dragging_button)
                    if game_state.level_num >= 2 and new_btn.command in ["for_start", "for_end"]:
                        error_msg = _validate_for_end_command(game_state.console_commands, new_btn.command)
                        if error_msg:
                            game_state.show_error = True
                            game_state.error_message = error_msg
                            dragging_button.reset_position()
                            dragging_button = None
                            return dragging_button, None
                    
                    game_state.console_commands.append(new_btn)
                    if game_state.level_num >= 2:
                        update_console_indentation(game_state.console_commands, console_rect)
                        if new_btn.command == "for_start":
                            game_state.for_selection_active = len(game_state.console_commands) - 1
                        elif new_btn.command == "if" and game_state.level_num >= 3:
                            game_state.if_selection_active = len(game_state.console_commands) - 1
                    else:
                        setup_console_command_position(new_btn, console_rect, len(game_state.console_commands) - 1)
                        if new_btn.command == "if" and game_state.level_num >= 3:
                            game_state.if_selection_active = len(game_state.console_commands) - 1
            dragging_button.reset_position()
            dragging_button = None
        return dragging_button, None
    
    return dragging_button, None
