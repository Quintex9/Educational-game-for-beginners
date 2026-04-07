# Eventy pre menu a výber levelov

import pygame
from UI.panel import panel_buttons

def handle_menu_events(event, game_state, buttons):
    # Spracuje eventy v menu a levels stave
    if event.type != pygame.MOUSEBUTTONDOWN:
        return False
    
    mx, my = event.pos
    for text, rect in buttons:
        if rect.collidepoint(mx, my):
            if game_state.state == "menu":
                if text == "Štart":
                    game_state.state = "level_groups"
                elif text == "Koniec":
                    return True

            elif game_state.state == "level_groups":
                if text == "Začiatočník":
                    game_state.state = "levels_1_4"
                elif text == "Pokročilý":
                    game_state.state = "levels_5_8"
                elif text == "Späť":
                    game_state.state = "menu"

            elif game_state.state in ("levels_1_4", "levels_5_8"):
                if text.startswith("Level"):
                    game_state.state = text
                    panel_buttons.clear()
                    level_num = int(text.split()[1])
                    game_state.initialize_level(level_num)
                elif text == "Späť":
                    game_state.state = "level_groups"
    
    return False
