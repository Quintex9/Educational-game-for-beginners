
# Obsluha eventov - kliknutia, pretiahnutia, atď.

import pygame
from UI.panel import panel_buttons
from UI.draggable_button import draggableButton
from console_logic import (
    expand_for_loops, 
    update_console_indentation, 
    create_console_command,
    setup_console_command_position,
    would_exceed_console_limit
)

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

def handle_for_selection_click(game_state, mx, my, console_rect):
    # Spracuje kliknutie na FOR výber popup
    if game_state.level_num < 2:
        return False
    
    if game_state.for_selection_active is not None:
        # Kontrola kliknutia na možnosti výberu
        for_selection_cmd = game_state.console_commands[game_state.for_selection_active]
        if for_selection_cmd.command == "for_start":
            popup_rect = pygame.Rect(
                for_selection_cmd.rect.x + for_selection_cmd.rect.width + 10,
                for_selection_cmd.rect.y,
                150,
                140
            )
            options = [("FOR 2x", 2), ("FOR 3x", 3), ("FOR 4x", 4)]
            for j, (text, count) in enumerate(options):
                option_rect = pygame.Rect(
                    popup_rect.x + 5,
                    popup_rect.y + 5 + j * 40,
                    popup_rect.width - 10,
                    35
                )
                if option_rect.collidepoint(mx, my):
                    for_selection_cmd.loop_count = count
                    for_selection_cmd.label = f"FOR {count}x"
                    game_state.for_selection_active = None
                    update_console_indentation(game_state.console_commands, console_rect)
                    return True
            else:
                # Klikol mimo popup - zatvorí výber
                if not popup_rect.collidepoint(mx, my):
                    game_state.for_selection_active = None
                    return True
        else:
            game_state.for_selection_active = None
            return True
    
    # Kontrola kliknutia na FOR príkaz v konzole
    if game_state.for_selection_active is None:
        for i, cmd in enumerate(game_state.console_commands):
            if cmd.rect.collidepoint(mx, my) and cmd.command == "for_start":
                game_state.for_selection_active = i
                return True
    
    return False

def handle_level_events(event, game_state, console_rect, button_rect, reset_button_rect, menu_button_rect, dragging_button, popup_rect=None, popup_button_rect=None):
    # Spracuje eventy v level stave
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        
        # Kontrola kliknutia na popup tlačidlo (priorita - popup blokuje ostatné akcie)
        if popup_button_rect and popup_button_rect.collidepoint(mx, my):
            if game_state.show_level_info:
                game_state.show_level_info = False
            elif game_state.show_victory:
                game_state.show_victory = False
            elif game_state.show_limit_warning:
                game_state.show_limit_warning = False
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
            
            # Skúsi pretiahnuť tlačidlo z panelu
            for btn in panel_buttons:
                if btn.start_drag((mx, my)):
                    dragging_button = btn
                    break
            
            # Kontrola FOR výberu (len ak nie je popup)
            if game_state.level_num >= 2 and not popup_rect:
                handle_for_selection_click(game_state, mx, my, console_rect)
            
            # Kontrola START tlačidla (len ak nie je popup)
            if button_rect.collidepoint(mx, my) and not popup_rect:
                if game_state.console_commands and not game_state.executing_commands:
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
                    game_state.console_commands.append(new_btn)
                    
                    # Aktualizuje odsadenie (vrátane nového) - len pre level 2 a vyššie
                    if game_state.level_num >= 2:
                        update_console_indentation(game_state.console_commands, console_rect)
                        # Ak je to FOR tlačidlo, automaticky otvorí výber možností
                        if new_btn.command == "for_start":
                            game_state.for_selection_active = len(game_state.console_commands) - 1
                    else:
                        # Pre level 1 bez odsadenia
                        index = len(game_state.console_commands) - 1
                        setup_console_command_position(new_btn, console_rect, index)
            
            dragging_button.reset_position()
            dragging_button = None
        
        return dragging_button, None
    
    return dragging_button, None
