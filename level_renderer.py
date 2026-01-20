
import pygame
from UI.grid import draw_grid
from UI.console import draw_console
from UI.panel import draw_panel, panel_buttons, buttons_for_level
from UI.buttons import draw_start_button, draw_menu_button, draw_reset_button
from console_logic import update_console_indentation, setup_console_command_position
from notifications import draw_level_info_popup, draw_victory_popup, draw_limit_warning_popup, draw_error_popup

def draw_player(screen, player, level_config):
    #Vykreslí hráča na obrazovku
    if not player:
        return
    
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
        screen.blit(scaled_sprite, (px * cell + offset, py * cell + offset))
    else:
        # Rezerva: vykresľuje červený obdĺžnik, ak sprite nie je dostupný
        player_rect = pygame.Rect(px * cell, py * cell, cell, cell)
        pygame.draw.rect(screen, (255, 0, 0), player_rect)

def draw_selection_popup(screen, cmd, mouse_pos, options, popup_width=150):
    #Generická funkcia pre vykreslenie popup výberu
    popup_height = len(options) * 40 + 10
    popup_rect = pygame.Rect(
        cmd.rect.x + cmd.rect.width + 10,
        cmd.rect.y,
        popup_width,
        popup_height
    )
    pygame.draw.rect(screen, (140, 180, 120), popup_rect, border_radius=8)
    pygame.draw.rect(screen, (80, 140, 60), popup_rect, width=2, border_radius=8)
    
    option_font = pygame.font.SysFont("Consolas", 18, bold=True)
    
    for j, (text, _) in enumerate(options):
        option_rect = pygame.Rect(
            popup_rect.x + 5,
            popup_rect.y + 5 + j * 40,
            popup_rect.width - 10,
            35
        )
        hovered = option_rect.collidepoint(mouse_pos)
        color = (120, 200, 100) if hovered else (100, 160, 80)
        pygame.draw.rect(screen, color, option_rect, border_radius=5)
        
        option_text = option_font.render(text, True, (40, 80, 40))
        text_rect = option_text.get_rect(center=option_rect.center)
        screen.blit(option_text, text_rect)
    
    return popup_rect

def draw_move_selection_popup(screen, cmd, mouse_pos):
    #Vykreslí popup pre výber pohybového príkazu
    from settings import MOVE_COMMANDS
    current_command = cmd.command
    options = [(MOVE_COMMANDS[move_cmd], move_cmd) 
               for move_cmd in MOVE_COMMANDS if move_cmd != current_command]
    return draw_selection_popup(screen, cmd, mouse_pos, options, popup_width=120)

def draw_for_selection_popup(screen, cmd, mouse_pos):
    #Vykreslí popup pre výber počtu opakovaní FOR cyklu
    options = [("FOR 2x", 2), ("FOR 3x", 3), ("FOR 4x", 4), ("FOR 5x", 5)]
    return draw_selection_popup(screen, cmd, mouse_pos, options)

def render_level(screen, game_state, level_config, mouse_pos):

    #Vykreslí celý level - grid, konzolu, panel, tlačidlá, hráča

    level_num = game_state.level_num
    
    # Vykreslí základné UI elementy
    draw_grid(screen, level_config, level_num)
    console_rect = draw_console(screen, level_config)
    panel_rect = draw_panel(screen, level_config)
    button_rect = draw_start_button(screen, level_config, mouse_pos)
    reset_button_rect = draw_reset_button(screen, level_config, mouse_pos)
    menu_button_rect = draw_menu_button(screen, level_config, mouse_pos)
    
    # Inicializuje panel tlačidlá
    if not panel_buttons:
        buttons_for_level(level_num, panel_rect)
    
    # Vykreslí panel tlačidlá
    font = pygame.font.SysFont("Consolas", 20, bold=True)
    for b in panel_buttons:
        b.draw(screen, font, (210, 210, 210), (50, 50, 50))
    
    # Aktualizuje odsadenie príkazov v konzole
    if game_state.console_commands:
        if level_num >= 2:
            update_console_indentation(game_state.console_commands, console_rect)
        else:
            for i, cmd in enumerate(game_state.console_commands):
                cmd.indent_level = 0
                setup_console_command_position(cmd, console_rect, i)
    
    # Vykreslí príkazy v konzole
    for cmd in game_state.console_commands:
        cmd.in_console = True
        cmd.draw(screen, font, (190, 190, 190), (40, 40, 40))
    
    # Zobrazí popup pre výber FOR počtu alebo pohybového príkazu
    if level_num >= 2 and game_state.for_selection_active is not None and game_state.for_selection_active < len(game_state.console_commands):
        cmd = game_state.console_commands[game_state.for_selection_active]
        if cmd.command == "for_start":
            draw_for_selection_popup(screen, cmd, mouse_pos)
    elif game_state.move_selection_active is not None and game_state.move_selection_active < len(game_state.console_commands):
        cmd = game_state.console_commands[game_state.move_selection_active]
        if cmd.command in ["move_up", "move_down", "move_left", "move_right"]:
            draw_move_selection_popup(screen, cmd, mouse_pos)
    
    # Vykreslí hráča
    draw_player(screen, game_state.player, level_config)
    
    # Zobrazí popup okná (priorita: výhra > error > limit > info)
    popup_funcs = [
        (game_state.show_victory, lambda: draw_victory_popup(screen, level_num)),
        (game_state.show_error, lambda: draw_error_popup(screen, game_state.error_message)),
        (game_state.show_limit_warning, lambda: draw_limit_warning_popup(screen)),
        (game_state.show_level_info, lambda: draw_level_info_popup(screen, level_num))
    ]
    popup_rect, popup_button_rect = next((f() for condition, f in popup_funcs if condition), (None, None))
    
    return console_rect, button_rect, reset_button_rect, menu_button_rect, popup_rect, popup_button_rect
