
#Logika vykonávania príkazov
import pygame
from level_data import LEVEL_DATA

def execute_single_command(game_state, cmd, level_config):
    #Vykoná jeden príkaz a vráti True, ak sa má pokračovať, False ak sa má zastaviť

    action = cmd.command
    grid_size = level_config["GRID_SIZE"]
    level_num = game_state.level_num
    
    # Spracovanie IF príkazu
    if action == "if":
        if cmd.condition in ["obstacle_down", "obstacle_right", "obstacle_left", "obstacle_up"]:
            # Získa aktuálnu pozíciu hráča
            px, py = game_state.player.get_position()
            
            # Určí pozíciu pre kontrolu podľa podmienky
            if cmd.condition == "obstacle_down":
                check_pos = (px, py + 1)
            elif cmd.condition == "obstacle_right":
                check_pos = (px + 1, py)
            elif cmd.condition == "obstacle_left":
                check_pos = (px - 1, py)
            elif cmd.condition == "obstacle_up":
                check_pos = (px, py - 1)
            else:
                return True
            
            # Kontroluje, či je na pozícii prekážka
            condition_met = check_pos in game_state.dynamic_obstacles
            
            # Ak podmienka nie je splnená, preskočí break_obstacle príkaz
            if not condition_met:
                # Preskočí break_obstacle príkaz (ak existuje)
                if game_state.command_queue and game_state.command_queue[0].command == "break_obstacle":
                    game_state.command_queue.pop(0)
        return True
    
    # Spracovanie break_obstacle príkazu
    if action == "break_obstacle":
        # Tento príkaz sa vykoná len ak bol IF podmienka splnená
        # (ak podmienka nebola splnená, tento príkaz už bol preskočený v IF)
        # Získa aktuálnu pozíciu hráča
        px, py = game_state.player.get_position()
        
        # Získa smer z break_direction atribútu
        if hasattr(cmd, 'break_direction') and cmd.break_direction:
            if cmd.break_direction == "down":
                check_pos = (px, py + 1)
            elif cmd.break_direction == "right":
                check_pos = (px + 1, py)
            elif cmd.break_direction == "left":
                check_pos = (px - 1, py)
            elif cmd.break_direction == "up":
                check_pos = (px, py - 1)
            else:
                return True
            
            # Odstráni prekážku ak existuje
            if check_pos in game_state.dynamic_obstacles:
                game_state.dynamic_obstacles.remove(check_pos)
        return True
    
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
    else:
        # Ak to nie je pohybový príkaz, ignoruje sa
        return True
    
    # Kontroluje hranice
    new_x, new_y = game_state.player.get_position()
    if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
        game_state.player.set_position(old_x, old_y)
        return True
    
    # Kontroluje prekážky a cieľ (používa dynamický zoznam)
    if level_num in LEVEL_DATA:
        obstacles = game_state.dynamic_obstacles
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
            # Uloží číslo ďalšieho levelu (ak existuje)
            next_level = level_num + 1
            if next_level in LEVEL_DATA:
                game_state.next_level_num = next_level
            else:
                game_state.next_level_num = None
            return False
    
    return True

def process_command_execution(game_state, level_config):
    # Spracuje vykonávanie príkazov s oneskorením
    # Nevykonáva príkazy, ak je zobrazený popup
    if game_state.show_level_info or game_state.show_victory or game_state.show_limit_warning or game_state.show_error:
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
