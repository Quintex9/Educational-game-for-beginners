
import pygame
from UI.grid import draw_grid
from UI.console import draw_console
from UI.panel import draw_panel, panel_buttons, buttons_for_level
from UI.start_button import draw_start_button
from UI.menu_button import draw_menu_button
from UI.reset_button import draw_reset_button
from UI.draggable_button import draggableButton
from level_data import LEVEL_DATA
from console_logic import update_console_indentation, setup_console_command_position
from notifications import draw_level_info_popup, draw_victory_popup, draw_limit_warning_popup

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

def draw_for_selection_popup(screen, cmd, mouse_pos):
    #Vykreslí popup pre výber počtu opakovaní FOR cyklu
    popup_rect = pygame.Rect(
        cmd.rect.x + cmd.rect.width + 10,
        cmd.rect.y,
        150,
        140
    )
    pygame.draw.rect(screen, (50, 60, 75), popup_rect, border_radius=8)
    pygame.draw.rect(screen, (80, 100, 120), popup_rect, width=2, border_radius=8)
    
    options = [("FOR 2x", 2), ("FOR 3x", 3), ("FOR 4x", 4)]
    option_font = pygame.font.SysFont("Consolas", 18, bold=True)
    
    for j, (text, count) in enumerate(options):
        option_rect = pygame.Rect(
            popup_rect.x + 5,
            popup_rect.y + 5 + j * 40,
            popup_rect.width - 10,
            35
        )
        hovered = option_rect.collidepoint(mouse_pos)
        color = (70, 90, 110) if hovered else (60, 75, 90)
        pygame.draw.rect(screen, color, option_rect, border_radius=5)
        
        option_text = option_font.render(text, True, (240, 245, 250))
        text_rect = option_text.get_rect(center=option_rect.center)
        screen.blit(option_text, text_rect)

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
    if game_state.console_commands and level_num >= 2:
        update_console_indentation(game_state.console_commands, console_rect)
    elif game_state.console_commands:
        # Pre level 1 bez odsadenia
        for i, cmd in enumerate(game_state.console_commands):
            cmd.indent_level = 0
            setup_console_command_position(cmd, console_rect, i)
    
    # Vykreslí príkazy v konzole
    for cmd in game_state.console_commands:
        cmd.in_console = True
        cmd.draw(screen, font, (190, 190, 190), (40, 40, 40))
    
    # Zobrazí popup pre výber FOR počtu (len pre level 2 a vyššie)
    if (level_num >= 2 and game_state.for_selection_active is not None and 
        game_state.for_selection_active < len(game_state.console_commands)):
        cmd = game_state.console_commands[game_state.for_selection_active]
        if cmd.command == "for_start":
            draw_for_selection_popup(screen, cmd, mouse_pos)
    
    # Vykreslí hráča
    draw_player(screen, game_state.player, level_config)
    
    # Zobrazí popup okná (priorita: výhra > limit > info)
    popup_rect = None
    popup_button_rect = None
    
    # Popup pri výhre (má prioritu)
    if game_state.show_victory:
        popup_rect, popup_button_rect = draw_victory_popup(screen, level_num)
    # Popup s upozornením o limite
    elif game_state.show_limit_warning:
        popup_rect, popup_button_rect = draw_limit_warning_popup(screen)
    # Popup s informáciami o leveli pri spustení
    elif game_state.show_level_info:
        popup_rect, popup_button_rect = draw_level_info_popup(screen, level_num)
    
    return console_rect, button_rect, reset_button_rect, menu_button_rect, popup_rect, popup_button_rect
