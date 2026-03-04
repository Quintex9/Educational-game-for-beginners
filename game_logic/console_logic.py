
#Logika pre konzolu - odsadenie, for cykly, popup

from UI.draggable_button import draggableButton
from utils.settings import (CONSOLE_SLOT_HEIGHT, CONSOLE_BUTTON_WIDTH, CONSOLE_BUTTON_HEIGHT,
                     CONSOLE_COLUMN_SPACING, CONSOLE_INDENT_WIDTH, CONSOLE_PADDING)

def _calculate_positions(commands, console_rect, indent_levels):
    #Pomocná funkcia pre výpočet pozícií príkazov
    start_x = console_rect.x + CONSOLE_PADDING
    start_y = console_rect.y + CONSOLE_PADDING
    
    max_indent = max(indent_levels, default=0) if indent_levels else 0
    # Nájde maximálnu šírku tlačidla v príkazoch (break_obstacle má 150, ostatné 100)
    max_button_width = max((cmd.rect.width for cmd in commands), default=CONSOLE_BUTTON_WIDTH)
    column_width = max_button_width + max_indent * CONSOLE_INDENT_WIDTH + CONSOLE_COLUMN_SPACING
    
    current_column = 0
    row_in_column = 0
    
    for i, cmd in enumerate(commands):
        y_pos = start_y + row_in_column * CONSOLE_SLOT_HEIGHT
        if y_pos + CONSOLE_BUTTON_HEIGHT > console_rect.bottom:
            current_column += 1
            row_in_column = 0
            y_pos = start_y
        
        x_pos = start_x + indent_levels[i] * CONSOLE_INDENT_WIDTH + current_column * column_width
        cmd.rect.x = x_pos
        cmd.rect.y = y_pos
        row_in_column += 1

def update_console_indentation(commands, console_rect):
    #Aktualizuje odsadenie všetkých príkazov v konzole na základe for cyklov a IF príkazov
    indent_level = 0
    indent_levels = []
    i = 0
    
    # Vypočíta indent_level pre všetky príkazy
    while i < len(commands):
        cmd = commands[i]
        if cmd.command == "for_start":
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)
            indent_level += 1
        elif cmd.command == "for_end":
            indent_level = max(0, indent_level - 1)
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)
        elif cmd.command == "if":
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)
            indent_level += 1
            # Nasledujúci príkaz (break_obstacle) bude odsadený
            if i + 1 < len(commands) and commands[i + 1].command == "break_obstacle":
                i += 1
                break_cmd = commands[i]
                break_cmd.indent_level = indent_level
                indent_levels.append(indent_level)
                indent_level = max(0, indent_level - 1)  # Po break_obstacle sa vráti späť
        else:
            cmd.indent_level = indent_level
            indent_levels.append(indent_level)
        i += 1
    
    _calculate_positions(commands, console_rect, indent_levels)

def expand_for_loops(commands):
    #Rozbalí for cykly v zozname príkazov
    result, i = [], 0
    while i < len(commands):
        if commands[i].command == "for_start":
            loop_count, loop_commands, i = commands[i].loop_count, [], i + 1
            while i < len(commands) and commands[i].command != "for_end":
                loop_commands.append(commands[i])
                i += 1
            if i < len(commands):
                i += 1
            result.extend(loop_commands * loop_count)
        else:
            if commands[i].command != "for_end":
                result.append(commands[i])
            i += 1
    return result

def setup_console_command_position(cmd, console_rect, index):
    #Nastaví pozíciu príkazu v konzole (pre level 1 bez odsadenia)
    start_x, start_y = console_rect.x + CONSOLE_PADDING, console_rect.y + CONSOLE_PADDING
    max_per_col = max(1, (console_rect.height - CONSOLE_PADDING * 2) // CONSOLE_SLOT_HEIGHT)
    col_width = CONSOLE_BUTTON_WIDTH + CONSOLE_COLUMN_SPACING
    cmd.rect.x = start_x + (index // max_per_col) * col_width
    cmd.rect.y = start_y + (index % max_per_col) * CONSOLE_SLOT_HEIGHT

def create_console_command(dragging_button):
    #Vytvorí nový príkaz v konzole z pretiahnutého tlačidla
    new_btn = draggableButton(
        dragging_button.rect.x,
        dragging_button.rect.y,
        100,
        50,
        dragging_button.label,
        dragging_button.command
    )
    # Kopíruje loop_count a condition z pôvodného tlačidla
    new_btn.loop_count = dragging_button.loop_count
    new_btn.condition = getattr(dragging_button, 'condition', None)
    # Ak je to FOR tlačidlo, nastaví defaultný label a počet
    if new_btn.command == "for_start":
        new_btn.loop_count = 2
        new_btn.label = "FOR"
    # Ak je to IF tlačidlo, nastaví defaultný label
    elif new_btn.command == "if":
        new_btn.label = "IF"
        new_btn.condition = None
    return new_btn

def validate_for_loops(commands):
    if not commands:
        return True, ""
    
    # Kontrola vnorených cyklov a prázdnych cyklov
    i = 0
    while i < len(commands):
        cmd = commands[i]
        
        if cmd.command == "for_start":
            # Kontrola, či už nie sme v cykle (vnorené cykly nie sú povolené)
            # Skontrolujeme, či predchádzajúci FOR už má END
            for_start_index = i
            i += 1
            
            # Zbiera príkazy až do END
            loop_commands = []
            found_end = False
            
            while i < len(commands):
                if commands[i].command == "for_end":
                    found_end = True
                    i += 1
                    break
                elif commands[i].command == "for_start":
                    # Našli sme vnorený FOR - to nie je povolené
                    return False, "Vnorené cykly nie sú povolené!\n\nNemôžeš použiť FOR\nv rámci iného FOR cyklu."
                
                loop_commands.append(commands[i])
                i += 1
            
            # Kontrola, či bol nájdený END
            if not found_end:
                return False, "FOR cyklus nie je uzavretý!\n\nKaždý FOR cyklus musí\nbyť uzavretý pomocou END."
            
            # Kontrola, či cyklus nie je prázdny (FOR hneď za tým END)
            if len(loop_commands) == 0:
                return False, "FOR cyklus je prázdny!\n\nMedzi FOR a END musí\nbyť aspoň jeden príkaz."
        else:
            i += 1
    
    # Kontrola, či všetky END majú svoj FOR
    for_count = 0
    end_count = 0
    for cmd in commands:
        if cmd.command == "for_start":
            for_count += 1
        elif cmd.command == "for_end":
            end_count += 1
            if end_count > for_count:
                return False, "Príliš veľa END príkazov!\n\nKaždý END musí mať\nsvoj zodpovedajúci FOR."
    
    if for_count != end_count:
        return False, "Nesprávny počet FOR a END!\n\nPočet FOR a END príkazov\nmusí byť rovnaký."
    
    return True, ""

def would_exceed_console_limit(commands, console_rect, level_num):
    """
    Skontroluje, či by pridaním nového príkazu presiahla konzola svoju pravú hranicu
    
    Returns:
        bool: True ak by presiahla limit, False inak
    """
    start_x = console_rect.x + CONSOLE_PADDING
    available_height = console_rect.height - CONSOLE_PADDING * 2
    max_commands_per_column = max(1, available_height // CONSOLE_SLOT_HEIGHT)
    new_index = len(commands)
    
    if level_num >= 2:
        # Vypočíta indent_level nového príkazu
        indent_level = sum(1 for cmd in commands if cmd.command == "for_start") - \
                      sum(1 for cmd in commands if cmd.command == "for_end")
        indent_level = max(0, indent_level)
        
        max_indent = max([c.indent_level for c in commands], default=0) if commands else 0
        # Zohľadní maximálnu šírku tlačidla (break_obstacle má 150)
        max_button_width = max((cmd.rect.width for cmd in commands), default=CONSOLE_BUTTON_WIDTH) if commands else CONSOLE_BUTTON_WIDTH
        column_width = max_button_width + max_indent * CONSOLE_INDENT_WIDTH + CONSOLE_COLUMN_SPACING
        current_column = new_index // max_commands_per_column
        x_pos = start_x + indent_level * CONSOLE_INDENT_WIDTH + current_column * column_width
    else:
        max_button_width = max((cmd.rect.width for cmd in commands), default=CONSOLE_BUTTON_WIDTH) if commands else CONSOLE_BUTTON_WIDTH
        column_width = max_button_width + CONSOLE_COLUMN_SPACING
        column = new_index // max_commands_per_column
        x_pos = start_x + column * column_width
    
    # Použije maximálnu šírku tlačidla pre kontrolu limitu
    max_button_width = max((cmd.rect.width for cmd in commands), default=CONSOLE_BUTTON_WIDTH) if commands else CONSOLE_BUTTON_WIDTH
    return x_pos + max_button_width > console_rect.right
