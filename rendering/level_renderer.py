
import pygame
from UI.grid import draw_grid
from UI.console import draw_console
from UI.panel import draw_panel, panel_buttons, buttons_for_level
from UI.buttons import draw_start_button, draw_menu_button, draw_reset_button, draw_console_buttons_area, draw_stars_info_button
from game_logic.console_logic import update_console_indentation, setup_console_command_position
from UI.level_info import draw_level_info_popup
from UI.stars import draw_victory_popup, draw_stars_info_popup
from rendering.popups import draw_limit_warning_popup, draw_error_popup
from utils.popup_position import compute_selection_popup_rect

def draw_player(screen,player, level_config):
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
    popup_rect = compute_selection_popup_rect(
        cmd.rect,
        popup_width,
        popup_height,
        screen.get_rect(),
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
    from utils.settings import MOVE_COMMANDS
    current_command = cmd.command
    options = [(MOVE_COMMANDS[move_cmd], move_cmd) 
               for move_cmd in MOVE_COMMANDS if move_cmd != current_command]
    return draw_selection_popup(screen, cmd, mouse_pos, options, popup_width=120)

def draw_for_selection_popup(screen, cmd, mouse_pos):
    #Vykreslí popup pre výber počtu opakovaní FOR cyklu
    from utils.settings import FOR_OPTIONS, FOR_POPUP_WIDTH
    return draw_selection_popup(screen, cmd, mouse_pos, FOR_OPTIONS, popup_width=FOR_POPUP_WIDTH)

def draw_if_selection_popup(screen, cmd, mouse_pos):
    #Vykreslí popup pre výber podmienky IF
    options = [
        ("obstacle down", "obstacle_down"),
        ("obstacle right", "obstacle_right"),
        ("obstacle left", "obstacle_left"),
        ("obstacle up", "obstacle_up")
    ]
    return draw_selection_popup(screen, cmd, mouse_pos, options, popup_width=180)

def draw_text_console(screen, game_state, console_rect):
    """Vykreslí textovú konzolu pre level 5"""
    # Font pre text
    font = pygame.font.SysFont("Consolas", 18)
    line_height = 25
    padding = 15
    indent_size = 20  # Veľkosť odsadenia
    
    # Vykreslí textové pole
    text_area_rect = pygame.Rect(
        console_rect.x + padding,
        console_rect.y + padding,
        console_rect.width - 2 * padding,
        console_rect.height - 2 * padding
    )
    
    # Pozadie textovej oblasti
    pygame.draw.rect(screen, (40, 45, 50), text_area_rect)
    pygame.draw.rect(screen, (60, 70, 80), text_area_rect, width=2)
    
    # Rozdelí text na riadky
    lines = game_state.text_console_input.split('\n')
    
    # Vykreslí text s odsadením
    y_offset = text_area_rect.y + padding
    for i, line in enumerate(lines):
        if y_offset + line_height > text_area_rect.bottom:
            break
        
        # Vypočíta odsadenie pre tento riadok
        indent_level = 0
        stripped_line = line.lstrip()
        
        # Ak je aktuálny riadok "end", nemá odsadenie
        if stripped_line.lower() == "end":
            indent_level = 0
        else:
            # Počíta počet "for" pred aktuálnym riadkom (vrátane neukončených).
            for j in range(i):
                prev_line = lines[j].strip().lower()
                if prev_line.startswith("for"):
                    indent_level += 1
                elif prev_line == "end":
                    indent_level = max(0, indent_level - 1)

            # IF vetva: "break obstacle" je odsadený o +1 iba ak je priamo pod IF.
            if (
                stripped_line.lower() == "break obstacle"
                and i > 0
                and lines[i - 1].strip().lower().startswith("if obstacle ")
            ):
                indent_level += 1
        
        # Vykreslí odsadenie
        indent_x = text_area_rect.x + padding + indent_level * indent_size
        
        # Vykreslí riadok
        text_surf = font.render(stripped_line, True, (200, 200, 200))
        screen.blit(text_surf, (indent_x, y_offset))
        
        # Vykreslí výber textu (ak existuje) - zjednodušená verzia
        if (game_state.text_console_selection_start is not None and 
            game_state.text_console_selection_end is not None):
            # Vypočíta pozície výberu v celom texte
            sel_start = min(game_state.text_console_selection_start, game_state.text_console_selection_end)
            sel_end = max(game_state.text_console_selection_start, game_state.text_console_selection_end)
            
            # Vypočíta pozíciu začiatku tohto riadku v texte
            line_start_pos = sum(len(lines[j]) + 1 for j in range(i))  # +1 pre \n
            
            # Skontroluje, či výber sa týka tohto riadku
            if sel_start < line_start_pos + len(line) and sel_end > line_start_pos:
                # Vypočíta pozície výberu v rámci tohto riadku
                sel_in_line_start = max(0, sel_start - line_start_pos)
                sel_in_line_end = min(len(line), sel_end - line_start_pos)
                
                if sel_in_line_start < sel_in_line_end:
                    # Vykreslí pozadie výberu
                    sel_text = line[sel_in_line_start:sel_in_line_end]
                    sel_width = font.size(sel_text)[0]
                    sel_x = indent_x + font.size(line[:sel_in_line_start])[0]
                    sel_rect = pygame.Rect(sel_x, y_offset, sel_width, line_height - 5)
                    pygame.draw.rect(screen, (100, 150, 255), sel_rect)
                    # Vykreslí text výberu s inou farbou
                    sel_surf = font.render(sel_text, True, (255, 255, 255))
                    screen.blit(sel_surf, (sel_x, y_offset))
        
        # Vykreslí kurzor na aktuálnom riadku
        if game_state.text_console_active:
            # Vypočíta pozíciu kurzora v aktuálnom riadku
            text_before_cursor = game_state.text_console_input[:game_state.text_console_cursor_pos]
            lines_before = text_before_cursor.split('\n')
            if len(lines_before) > 0 and i == len(lines_before) - 1:
                cursor_in_line = len(lines_before[-1])
                cursor_x = indent_x + font.size(stripped_line[:cursor_in_line])[0]
                cursor_y = y_offset
                pygame.draw.line(screen, (255, 255, 255), 
                               (cursor_x, cursor_y), 
                               (cursor_x, cursor_y + line_height - 5), 
                               width=2)
        
        y_offset += line_height
    
    # Vykreslí prázdny kurzor, ak je text prázdny
    if game_state.text_console_active and not game_state.text_console_input:
        cursor_x = text_area_rect.x + padding
        cursor_y = text_area_rect.y + padding
        pygame.draw.line(screen, (255, 255, 255), 
                       (cursor_x, cursor_y), 
                       (cursor_x, cursor_y + line_height - 5), 
                       width=2)

def render_level(screen, game_state, level_config, mouse_pos):

    #Vykreslí celý level - grid, konzolu, panel, tlačidlá, hráča

    level_num = game_state.level_num
    
    # Vykreslí základné UI elementy
    draw_grid(screen, level_config, level_num, game_state.dynamic_obstacles)
    console_rect = draw_console(screen, level_config)
    panel_rect = draw_panel(screen, level_config)
    has_mode_toggle = 5 <= level_num <= 8
    
    # Vykreslí oblasť tlačidiel v konzole
    draw_console_buttons_area(screen, level_config, has_mode=has_mode_toggle)
    
    # Vykreslí tlačidlá v konzole
    reset_button_rect = draw_reset_button(screen, level_config, mouse_pos, has_mode=has_mode_toggle)
    menu_button_rect = draw_menu_button(screen, level_config, mouse_pos, has_mode=has_mode_toggle)
    stars_info_button_rect = draw_stars_info_button(screen, level_config, mouse_pos, has_mode=has_mode_toggle)
    # Pre levely 5-8: tlačidlo na prepínanie režimov
    mode_toggle_button_rect = None
    if has_mode_toggle:
        from UI.buttons import draw_mode_toggle_button
        mode_toggle_button_rect = draw_mode_toggle_button(screen, level_config, mouse_pos, game_state.text_mode)
    
    # START tlačidlo v paneli
    button_rect = draw_start_button(screen, level_config, mouse_pos)
    
    # Upraví console_rect aby začínal pod tlačidlami
    buttons_area_height = 50
    commands_console_rect = pygame.Rect(
        console_rect.x,
        console_rect.y + buttons_area_height,
        console_rect.width,
        console_rect.height - buttons_area_height
    )
    
    # Inicializuje panel tlačidlá
    if not panel_buttons:
        buttons_for_level(level_num, panel_rect)
    
    # Vykreslí panel tlačidlá
    font = pygame.font.SysFont("Consolas", 20, bold=True)
    for b in panel_buttons:
        # Pre levely 5-8: disabled v textovom režime
        disabled = (5 <= level_num <= 8 and game_state.text_mode)
        b.draw(screen, font, (210, 210, 210), (50, 50, 50), disabled=disabled)
    
    # Pre levely 5-8: textová konzola alebo drag&drop podľa režimu
    if 5 <= level_num <= 8 and game_state.text_mode:
        # Pre textovú konzolu použijeme pôvodný console_rect (celá oblasť)
        draw_text_console(screen, game_state, commands_console_rect)
    else:
        # Aktualizuje odsadenie príkazov v konzole (začína pod tlačidlami)
        if game_state.console_commands:
            if level_num >= 2:
                update_console_indentation(game_state.console_commands, commands_console_rect)
            else:
                for i, cmd in enumerate(game_state.console_commands):
                    cmd.indent_level = 0
                    setup_console_command_position(cmd, commands_console_rect, i)
        
        # Vykreslí príkazy v konzole
        for cmd in game_state.console_commands:
            cmd.in_console = True
            cmd.draw(screen, font, (190, 190, 190), (40, 40, 40))
    
    # Zobrazí popup pre výber FOR počtu, IF podmienky alebo pohybového príkazu
    if level_num >= 2 and game_state.for_selection_active is not None and game_state.for_selection_active < len(game_state.console_commands):
        cmd = game_state.console_commands[game_state.for_selection_active]
        if cmd.command == "for_start":
            draw_for_selection_popup(screen, cmd, mouse_pos)
    elif level_num >= 3 and game_state.if_selection_active is not None and game_state.if_selection_active < len(game_state.console_commands):
        cmd = game_state.console_commands[game_state.if_selection_active]
        if cmd.command == "if":
            draw_if_selection_popup(screen, cmd, mouse_pos)
    elif game_state.move_selection_active is not None and game_state.move_selection_active < len(game_state.console_commands):
        cmd = game_state.console_commands[game_state.move_selection_active]
        if cmd.command in ["move_up", "move_down", "move_left", "move_right"]:
            draw_move_selection_popup(screen, cmd, mouse_pos)
    
    # Vykreslí hráča
    draw_player(screen, game_state.player, level_config)
    
    # Zobrazí popup okná (priorita: výhra > error > limit > stars_info > info)
    popup_funcs = [
        (game_state.show_victory, lambda: draw_victory_popup(screen, level_num, game_state.next_level_num, game_state.stars_earned)),
        (game_state.show_error, lambda: draw_error_popup(screen, game_state.error_message)),
        (game_state.show_limit_warning, lambda: draw_limit_warning_popup(screen)),
        (game_state.show_stars_info, lambda: draw_stars_info_popup(screen, level_num)),
        (game_state.show_level_info, lambda: draw_level_info_popup(screen, level_num))
    ]
    popup_result = next((f() for condition, f in popup_funcs if condition), None)
    if popup_result is None:
        popup_rect, popup_button_rect, extra_popup_buttons = None, None, None
    else:
        # Podpora nového návratu z draw_victory_popup: (popup, btn1, (btn_menu, btn_quit))
        if len(popup_result) == 3:
            popup_rect, popup_button_rect, extra_popup_buttons = popup_result
        else:
            popup_rect, popup_button_rect = popup_result
            extra_popup_buttons = None
    
    # Vracia pôvodný console_rect (celá oblasť) pre event handlery + prípadné extra tlačidlá
    return commands_console_rect, button_rect, reset_button_rect, menu_button_rect, popup_rect, popup_button_rect, mode_toggle_button_rect, stars_info_button_rect, extra_popup_buttons
