
#Logika vykonávania príkazov
import pygame
from level_data import LEVEL_DATA

def execute_single_command(game_state, cmd, level_config):
    #Vykoná jeden príkaz a vráti True, ak sa má pokračovať, False ak sa má zastaviť

    action = cmd.command
    grid_size = level_config["GRID_SIZE"]
    level_num = game_state.level_num
    
    # Získa aktuálnu pozíciu pred pohybom
    old_x, old_y = game_state.player.get_position()
    
    # Vykoná pohyb
    if action == "move_up":
        game_state.player.move_up()
    elif action == "move_down":
        game_state.player.move_down()
    elif action == "move_right":
        game_state.player.move_right()
    elif action == "move_left":
        game_state.player.move_left()
    
    # Kontroluje hranice
    new_x, new_y = game_state.player.get_position()
    if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
        game_state.player.set_position(old_x, old_y)
        return True
    
    # Kontroluje prekážky a cieľ
    if level_num in LEVEL_DATA:
        obstacles = LEVEL_DATA[level_num].get("obstacles", [])
        if (new_x, new_y) in obstacles:
            game_state.player.set_position(old_x, old_y)
            return True
        
        # Kontroluje, či hráč dosiahol cieľ
        goal = LEVEL_DATA[level_num].get("goal")
        if goal and (new_x, new_y) == goal:
            game_state.executing_commands = False
            game_state.command_queue.clear()
            game_state.level_completed = True
            game_state.show_victory = True  # Zobrazí popup pri výhre
            return False
    
    return True

def process_command_execution(game_state, level_config):
    # Spracuje vykonávanie príkazov s oneskorením
    # Nevykonáva príkazy, ak je zobrazený popup
    if game_state.show_level_info or game_state.show_victory or game_state.show_limit_warning:
        return
    
    if not (game_state.executing_commands and game_state.command_queue):
        return
    
    current_time = pygame.time.get_ticks()
    if current_time - game_state.last_command_time >= game_state.command_delay:
        cmd = game_state.command_queue.pop(0)
        
        if execute_single_command(game_state, cmd, level_config):
            game_state.last_command_time = current_time
        
        # Ak nie sú žiadne ďalšie príkazy, zastaví vykonávanie
        if not game_state.command_queue:
            game_state.executing_commands = False
