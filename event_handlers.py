
# Obsluha eventov - kliknutia, pretiahnutia, atď.

import pygame
from UI.panel import panel_buttons
from console_logic import (
    expand_for_loops, 
    update_console_indentation, 
    create_console_command,
    setup_console_command_position,
    would_exceed_console_limit,
    validate_for_loops
)
from level_data import LEVEL_DATA

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

def handle_menu_events(event, game_state, buttons):
    # Spracuje eventy v menu a levels stave
    if event.type != pygame.MOUSEBUTTONDOWN:
        return False
    
    mx, my = event.pos
    for text, rect in buttons:
        if rect.collidepoint(mx, my):
            if game_state.state == "menu":
                if text == "Zoznam levelov":
                    game_state.state = "levels"
                elif text == "Koniec":
                    return True  # Ukonči hru
                    
            elif game_state.state == "levels":
                if text.startswith("Level"):
                    game_state.state = text
                    panel_buttons.clear()
                    level_num = int(text.split()[1])
                    game_state.initialize_level(level_num)
                elif text == "Späť":
                    game_state.state = "menu"
    
    return False

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
    
    from settings import FOR_OPTIONS, FOR_POPUP_WIDTH
    clicked, _ = handle_selection_popup_click(game_state, mx, my,
                                               game_state.for_selection_active, "for", FOR_OPTIONS, FOR_POPUP_WIDTH)
    if clicked:
        if game_state.for_selection_active is not None:
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
        if game_state.if_selection_active is not None:
            # Kontrola, či už existuje break_obstacle príkaz za IF
            if_index = game_state.if_selection_active
            # Aktualizuje odsadenie po zmene šírky IF tlačidla
            update_console_indentation(game_state.console_commands, console_rect)
            # Ak už existuje break_obstacle hneď za IF, aktualizuje jeho smer
            if (if_index + 1 < len(game_state.console_commands) and 
                game_state.console_commands[if_index + 1].command == "break_obstacle"):
                # Aktualizuje smer pre break_obstacle
                break_cmd = game_state.console_commands[if_index + 1]
                # Extrahuje smer z podmienky (obstacle_down -> down)
                direction = cmd.condition.replace("obstacle_", "")
                break_cmd.break_direction = direction
                # Aktualizuje odsadenie znovu
                update_console_indentation(game_state.console_commands, console_rect)
            else:
                # Vytvorí nový break_obstacle príkaz a vloží ho za IF
                from UI.draggable_button import draggableButton
                break_cmd = draggableButton(0, 0, 160, 50, "break obstacle", "break_obstacle")
                break_cmd.condition = None
                break_cmd.loop_count = 2
                # Extrahuje smer z podmienky (obstacle_down -> down)
                direction = cmd.condition.replace("obstacle_", "")
                break_cmd.break_direction = direction
                # Vloží za IF príkaz
                game_state.console_commands.insert(if_index + 1, break_cmd)
                # Aktualizuje odsadenie
                update_console_indentation(game_state.console_commands, console_rect)
            game_state.if_selection_active = None
        return True
    return False

def handle_move_selection_click(game_state, mx, my, console_rect):
    #Spracuje kliknutie na výber pohybového príkazu
    from settings import MOVE_COMMANDS
    
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
        if game_state.move_selection_active is not None:
            if game_state.level_num >= 2:
                update_console_indentation(game_state.console_commands, console_rect)
            game_state.move_selection_active = None
        return True
    return False

def handle_level_events(event, game_state, console_rect, button_rect, reset_button_rect, menu_button_rect, dragging_button, popup_rect=None, popup_button_rect=None):
    # Spracuje eventy v level stave
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        
        # Kontrola kliknutia na popup tlačidlo
        if popup_button_rect and popup_button_rect.collidepoint(mx, my):
            # Špeciálna logika pre victory popup - presmerovanie na ďalší level
            if game_state.show_victory and game_state.next_level_num is not None:
                # Presmeruje na ďalší level
                next_level = game_state.next_level_num
                game_state.state = f"Level {next_level}"
                panel_buttons.clear()
                game_state.initialize_level(next_level)
                return dragging_button, None
            
            # Normálne zatvorenie popup
            for flag in ['show_level_info', 'show_victory', 'show_limit_warning', 'show_error']:
                if getattr(game_state, flag, False):
                    setattr(game_state, flag, False)
                    if flag == 'show_error':
                        game_state.error_message = ""
                    break
            return dragging_button, None
        
        # Ak je popup zobrazený, ignoruj ostatné kliknutia
        if popup_rect and popup_rect.collidepoint(mx, my):
            return dragging_button, None
        
        # Kontrola kliknutia na RESET tlačidlo
        if reset_button_rect.collidepoint(mx, my):
            game_state.console_commands.clear()
            game_state.command_queue.clear()
            game_state.executing_commands = False
            game_state.for_selection_active = None
            game_state.if_selection_active = None
            game_state.move_selection_active = None

            game_state.show_error = False
            game_state.error_message = ""
            return dragging_button, None
        
        # Kontrola kliknutia na MENU tlačidlo
        if menu_button_rect.collidepoint(mx, my):
            game_state.reset_to_menu()
            return None, None
        
        # Kontrola panel tlačidiel (len ak nie je popup)
        if (not popup_rect and not menu_button_rect.collidepoint(mx, my) and 
            not reset_button_rect.collidepoint(mx, my) and
            not game_state.executing_commands and 
            not game_state.level_completed):
            
            # Skúsi pretiahnuť tlačidlo z panelu (len ak nebolo kliknutie na príkaz v konzole)
            if not any(cmd.rect.collidepoint(mx, my) for cmd in game_state.console_commands):
                for btn in panel_buttons:
                    if btn.start_drag((mx, my)):
                        dragging_button = btn
                        break
            
            # Kontrola FOR výberu (len ak nie je popup a nie je aktívny výber pohybu alebo IF)
            if (game_state.level_num >= 2 and not popup_rect and 
                game_state.move_selection_active is None and game_state.if_selection_active is None):
                if handle_for_selection_click(game_state, mx, my, console_rect):
                    return dragging_button, None
            
            # Kontrola IF výberu (len ak nie je popup a nie je aktívny výber pohybu alebo FOR)
            if (game_state.level_num >= 3 and not popup_rect and 
                game_state.move_selection_active is None and game_state.for_selection_active is None):
                if handle_if_selection_click(game_state, mx, my, console_rect):
                    return dragging_button, None
            
            # Kontrola výberu pohybového príkazu (len ak nie je popup a nie je aktívny výber FOR alebo IF)
            if (not popup_rect and game_state.for_selection_active is None and game_state.if_selection_active is None):
                if handle_move_selection_click(game_state, mx, my, console_rect):
                    return dragging_button, None
            
            # Kontrola START tlačidla (len ak nie je popup)
            if button_rect.collidepoint(mx, my) and not popup_rect:
                if game_state.console_commands and not game_state.executing_commands:
                    # Validácia FOR cyklov pred spustením (len pre level 2+)
                    if game_state.level_num >= 2:
                        is_valid, error_msg = validate_for_loops(game_state.console_commands)
                        if not is_valid:
                            game_state.show_error = True
                            game_state.error_message = error_msg
                            return dragging_button, None
                    
                    # Rozbalí for cykly pred vykonaním (len pre level 2 a vyššie)
                    if game_state.level_num >= 2:
                        expanded_commands = expand_for_loops(game_state.console_commands)
                    else:
                        expanded_commands = game_state.console_commands.copy()
                    game_state.command_queue = expanded_commands.copy()
                    game_state.console_commands.clear()
                    game_state.executing_commands = True
                    # Nastaví čas na minulý, aby prvý príkaz vykonával okamžite
                    game_state.last_command_time = pygame.time.get_ticks() - game_state.command_delay
        
        return dragging_button, None
    
    elif event.type == pygame.MOUSEMOTION:
        if dragging_button:
            dragging_button.drag(event.pos)
        return dragging_button, None
    
    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging_button:
            dragging_button.stop_drag()
            
            # Ak je popup zobrazený, ignoruj drop
            if not popup_rect and console_rect.collidepoint(dragging_button.rect.center):
                # Skontroluje, či by pridaním nového príkazu presiahla konzola limit
                if would_exceed_console_limit(game_state.console_commands, console_rect, game_state.level_num):
                    game_state.show_limit_warning = True
                else:
                    # Vytvorí nový príkaz v konzole
                    new_btn = create_console_command(dragging_button)
                    
                    # Validácia pre FOR a END príkazy (len pre level 2+)
                    if game_state.level_num >= 2 and new_btn.command in ["for_start", "for_end"]:
                        error_msg = _validate_for_end_command(game_state.console_commands, new_btn.command)
                        if error_msg:
                            game_state.show_error = True
                            game_state.error_message = error_msg
                            dragging_button.reset_position()
                            dragging_button = None
                            return dragging_button, None
                    
                    game_state.console_commands.append(new_btn)
                    
                    # Aktualizuje odsadenie (vrátane nového)
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
