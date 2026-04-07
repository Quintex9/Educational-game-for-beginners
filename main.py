import pygame
import sys
from utils.window import Window
from utils.settings import MENU_IMG, set_level_size
from rendering.menu_renderer import draw_menu, draw_level_groups, draw_showlevels
from core.game_state import GameState
from game_logic.command_executor import process_command_execution
from rendering.level_renderer import render_level
from events.menu_events import handle_menu_events
from events.level_events import handle_level_events

pygame.init()
window = Window(background_path=MENU_IMG)
clock = pygame.time.Clock()
running = True

# Inicializacia stavu hry
game_state = GameState()
dragging_button = None

# Inicializacia premennych pre level
console_rect = None
button_rect = None
reset_button_rect = None
menu_button_rect = None
mode_toggle_button_rect = None
stars_info_button_rect = None
popup_rect = None
popup_button_rect = None
buttons = []

# Hlavna herna slucka
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Vykreslenie podla aktualneho stavu
    if game_state.state == "menu":
        window.draw_background()
        buttons = draw_menu(window.screen, mouse_pos)

    elif game_state.state == "level_groups":
        window.draw_background()
        buttons = draw_level_groups(window.screen, mouse_pos)

    elif game_state.state in ("levels_1_4", "levels_5_8"):
        buttons = draw_showlevels(window.screen, mouse_pos, game_state.state)

    elif game_state.state.startswith("Level"):
        window.draw_background((30, 35, 45))
        level_config = set_level_size(game_state.level_num - 1)

        # Spracovanie vykonavania prikazov
        process_command_execution(game_state, level_config)

        # Vykreslenie levelu
        (
            console_rect,
            button_rect,
            reset_button_rect,
            menu_button_rect,
            popup_rect,
            popup_button_rect,
            mode_toggle_button_rect,
            stars_info_button_rect,
            popup_extra_buttons,
        ) = render_level(window.screen, game_state, level_config, mouse_pos)

    # Spracovanie eventov
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif game_state.state in ("menu", "level_groups", "levels_1_4", "levels_5_8"):
            should_quit = handle_menu_events(event, game_state, buttons)
            if should_quit:
                running = False

        elif game_state.state.startswith("Level"):
            if console_rect is not None:
                dragging_button, _ = handle_level_events(
                    event,
                    game_state,
                    console_rect,
                    button_rect,
                    reset_button_rect,
                    menu_button_rect,
                    dragging_button,
                    popup_rect,
                    popup_button_rect,
                    mode_toggle_button_rect,
                    stars_info_button_rect,
                    popup_extra_buttons,
                )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
