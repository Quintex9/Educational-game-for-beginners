import pygame,sys
from window import Window
from settings import MENU_IMG, set_level_size
from menu import draw_menu
from showlevels import draw_showlevels
from UI.grid import draw_grid
from UI.console import draw_console
from UI.panel import draw_panel, panel_buttons, buttons_for_level
from UI.start_button import draw_start_button
from UI.draggable_button import draggableButton
from player import Player
from executor import execute_commands

pygame.init()
window = Window(background_path=MENU_IMG)

clock = pygame.time.Clock()
running = True
state = "menu"

dragging_button = None

console_commands = []
command_queue = []  
command_delay = 500  # Delay medzi príkazmi v milisekundách
last_command_time = 0  # Čas, keď bol posledný príkaz vykonaný
executing_commands = False  # Flag, ktorý sleduje, či sa príkazy vykonávajú

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    if state == "menu":
        window.draw_background()
        buttons = draw_menu(window.screen, mouse_pos)
        
    elif state == "levels":
        buttons = draw_showlevels(window.screen, mouse_pos)
        
    elif state.startswith("Level"):
        level_num = int(state.split()[1])
        # Moderné tmavé pozadie
        window.draw_background((30, 35, 45))
        level_config = set_level_size(level_num - 1)
        
        draw_grid(window.screen, level_config,level_num)
        console_rect = draw_console(window.screen,level_config)
        
        panel_rect = draw_panel(window.screen,level_config)
        button_rect = draw_start_button(window.screen,level_config,mouse_pos)
        
        # Vykonáva príkazy postupne s oneskorením
        if executing_commands and command_queue:
            current_time = pygame.time.get_ticks()
            if current_time - last_command_time >= command_delay:
                # Vykonáva ďalší príkaz
                cmd = command_queue.pop(0)
                action = cmd.command
                grid_size = level_config["GRID_SIZE"]
                
                # Získa aktuálnu pozíciu pred pohybom
                old_x, old_y = player.get_position()
                
                # Vykonáva pohyb
                if action == "move_up":
                    player.move_up()
                elif action == "move_down":
                    player.move_down()
                elif action == "move_right":
                    player.move_right()
                elif action == "move_left":
                    player.move_left()
                
                # Kontroluje hranice a vracia, ak je mimo
                new_x, new_y = player.get_position()
                if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
                    player.set_position(old_x, old_y)
                
                last_command_time = current_time
                
                # Ak nie sú žiadne ďalšie príkazy, zastaví vykonávanie
                if not command_queue:
                    executing_commands = False
        
        #PLAYER
        if 'player' in locals():
            cell = level_config["CELL_SIZE"]
            px, py = player.get_position()
            
            # Získa sprite a škáluje ho na menšiu veľkosť (70% z veľkosti bunky)
            sprite = player.get_sprite()
            if sprite:
                sprite_size = int(cell * 0.7)
                scaled_sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
                # Centruje sprite v bunkách
                offset = (cell - sprite_size) // 2
                # Vykresľuje sprite na pozícii hráča (centrovaný v bunkách)
                window.screen.blit(scaled_sprite, (px * cell + offset, py * cell + offset))
            else:
                # Rezerva: vykresľuje červený obdĺžnik, ak sprite nie je dostupný
                player_rect = pygame.Rect(px * cell, py * cell, cell, cell)
                pygame.draw.rect(window.screen, (255, 0, 0), player_rect)
        
        
        if not panel_buttons:
            buttons_for_level(level_num,panel_rect)
        
        font = pygame.font.SysFont("Consolas", 20, bold=True)
        for b in panel_buttons:
            b.draw(window.screen, font, (210, 210, 210), (50, 50, 50))
            
        for cmd in console_commands:
            cmd.draw(window.screen, font, (190,190,190), (40,40,40))


        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.VIDEORESIZE:
            window.resize(event.w,event.h)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            if state in ("menu","levels"):
                for text, rect in buttons:
                    if rect.collidepoint(mx,my):
                        if state == "menu":
                            if text == "Zoznam levelov":
                                state = "levels"
                            elif text == "Koniec":
                                running = False
                                
                        elif state == "levels":
                            if text.startswith("Level"):
                                state = text
                                panel_buttons.clear()
                                player = Player(0,0)
                                # Resetuje frontu príkazov pri začatí nového levelu
                                command_queue.clear()
                                executing_commands = False
                            elif text == "Späť":
                                state = "menu"
                              
            elif state.startswith("Level"):
                for btn in panel_buttons:
                    if btn.start_drag((mx,my)):
                        dragging_button = btn
                        break
                    
                if button_rect.collidepoint(mx,my):
                    # Začne vykonávať príkazy postupne
                    if console_commands and not executing_commands:
                        command_queue = console_commands.copy()  # Kopíruje príkazy do fronty
                        console_commands.clear()
                        executing_commands = True
                        # Nastaví čas na minulý, aby prvý príkaz vykonával okamžite
                        last_command_time = pygame.time.get_ticks() - command_delay
        
        elif event.type == pygame.MOUSEMOTION:
            if dragging_button:
                dragging_button.drag(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_button:
                dragging_button.stop_drag()
                
                if console_rect.collidepoint(dragging_button.rect.center):
                    #Vytvorí kópiu tlačidla
                    new_btn = draggableButton(
                        dragging_button.rect.x,
                        dragging_button.rect.y,
                        100,
                        50,
                        dragging_button.label,
                        dragging_button.command
                        )
                    console_commands.append(new_btn)
                    
                    slot_height = 50
                    index = len(console_commands) - 1
                    
                    new_btn.rect.x = console_rect.x + 20
                    new_btn.rect.y = console_rect.y + 10 + index * slot_height

                dragging_button.reset_position()
                dragging_button = None
                            
    pygame.display.flip()
    clock.tick(60)
