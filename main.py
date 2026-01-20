import pygame
import sys
from window import Window
from settings import MENU_IMG, set_level_size
from menu import draw_menu
from showlevels import draw_showlevels
from game_state import GameState
from command_executor import process_command_execution
from level_renderer import render_level
from event_handlers import handle_menu_events, handle_level_events

pygame.init()
window = Window(background_path=MENU_IMG)
clock = pygame.time.Clock()
running = True

# Inicializácia stavu hry
game_state = GameState()
dragging_button = None

# Inicializácia premenných pre level
console_rect = None
button_rect = None
reset_button_rect = None
menu_button_rect = None
popup_rect = None
popup_button_rect = None
buttons = []

# Hlavná herná slučka
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Vykreslenie podľa aktuálneho stavu
    if game_state.state == "menu":
        window.draw_background()
        buttons = draw_menu(window.screen, mouse_pos)
        
    elif game_state.state == "levels":
        buttons = draw_showlevels(window.screen, mouse_pos)
        
    elif game_state.state.startswith("Level"):
        # Moderné tmavé pozadie
        window.draw_background((30, 35, 45))
        level_config = set_level_size(game_state.level_num - 1)
        
        # Spracovanie vykonávania príkazov
        process_command_execution(game_state, level_config)
        
        # Vykreslenie levelu
        console_rect, button_rect, reset_button_rect, menu_button_rect, popup_rect, popup_button_rect = render_level(
            window.screen, game_state, level_config, mouse_pos
        )
    
    # Spracovanie eventov
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.VIDEORESIZE:
            window.resize(event.w, event.h)
            
        elif game_state.state in ("menu", "levels"):
            should_quit = handle_menu_events(event, game_state, buttons)
            if should_quit:
                running = False
                
        elif game_state.state.startswith("Level"):
            if console_rect is not None:
                dragging_button, _ = handle_level_events(
                    event, game_state, console_rect, button_rect, reset_button_rect, menu_button_rect, 
                    dragging_button, popup_rect, popup_button_rect
                )
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
