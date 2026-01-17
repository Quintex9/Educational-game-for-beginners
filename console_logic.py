
#Logika pre konzolu - odsadenie, for cykly, popup

from UI.draggable_button import draggableButton

def update_console_indentation(commands, console_rect):
    #Aktualizuje odsadenie všetkých príkazov v konzole na základe for cyklov
    indent_level = 0
    indent_width = 30
    slot_height = 50
    button_width = 100
    button_height = 50
    column_spacing = 20  # Medzera medzi stĺpcami
    start_x = console_rect.x + 20
    start_y = console_rect.y + 10
    
    # Vypočíta koľko príkazov sa zmestí do jedného stĺpca
    available_height = console_rect.height - 20  # -20 pre padding
    max_commands_per_column = max(1, available_height // slot_height)
    
    # Najprv vypočíta indent_level pre všetky príkazy
    for cmd in commands:
        if cmd.command == "for_start":
            cmd.indent_level = indent_level
            indent_level += 1
        elif cmd.command == "for_end":
            indent_level = max(0, indent_level - 1)
            cmd.indent_level = indent_level
        else:
            cmd.indent_level = indent_level
    
    # Vypočíta maximálne odsadenie pre určenie šírky stĺpca
    max_indent = max([c.indent_level for c in commands], default=0) if commands else 0
    column_width = button_width + max_indent * indent_width + column_spacing
    
    # Teraz vypočíta pozície s podporou viacerých stĺpcov
    current_column = 0
    row_in_column = 0
    
    for cmd in commands:
        # Kontrola, či sa príkaz zmestí do aktuálneho stĺpca
        y_pos = start_y + row_in_column * slot_height
        if y_pos + button_height > console_rect.bottom:
            # Presunie sa do ďalšieho stĺpca
            current_column += 1
            row_in_column = 0
            y_pos = start_y
        
        # Vypočíta x pozíciu (základná pozícia v stĺpci + odsadenie + offset stĺpca)
        x_pos = start_x + cmd.indent_level * indent_width + current_column * column_width
        
        # Nastaví pozíciu
        cmd.rect.x = x_pos
        cmd.rect.y = y_pos
        
        row_in_column += 1

def expand_for_loops(commands):
    """
    Rozbalí for cykly v zozname príkazov.
    Nájde for_start a opakuje príkazy po ňom až do for_end.
    """
    result = []
    i = 0
    
    while i < len(commands):
        cmd = commands[i]
        
        if cmd.command == "for_start":
            # Použije loop_count z tohto príkazu
            loop_count = cmd.loop_count
            # Zbiera všetky príkazy po FOR až do END
            loop_commands = []
            i += 1
            
            # Zbiera príkazy až do END alebo do konca
            while i < len(commands) and commands[i].command != "for_end":
                loop_commands.append(commands[i])
                i += 1
            
            # Preskočí END
            if i < len(commands) and commands[i].command == "for_end":
                i += 1
            
            # Opakuje príkazy v cykle
            for _ in range(loop_count):
                result.extend(loop_commands)
        else:
            # Normálny príkaz alebo END - pridá sa do výsledku (END sa ignoruje)
            if cmd.command != "for_end":
                result.append(cmd)
            i += 1
    
    return result

def setup_onsole_command_position(cmd, console_rect, index):
    #Nastaví pozíciu príkazu v konzole (pre level 1 bez odsadenia)"""
    slot_height = 50
    button_width = 100
    button_height = 50
    column_spacing = 20
    start_x = console_rect.x + 20
    start_y = console_rect.y + 10
    
    # Vypočíta koľko príkazov sa zmestí do jedného stĺpca
    available_height = console_rect.height - 20
    max_commands_per_column = max(1, available_height // slot_height)
    
    # Vypočíta stĺpec a riadok
    column = index // max_commands_per_column
    row_in_column = index % max_commands_per_column
    
    # Vypočíta šírku stĺpca (bez odsadenia pre level 1)
    column_width = button_width + column_spacing
    
    # Nastaví pozíciu
    cmd.rect.x = start_x + column * column_width
    cmd.rect.y = start_y + row_in_column * slot_height

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
    # Kopíruje loop_count z pôvodného tlačidla
    new_btn.loop_count = dragging_button.loop_count
    # Ak je to FOR tlačidlo, nastaví defaultný label a počet
    if new_btn.command == "for_start":
        new_btn.loop_count = 2
        new_btn.label = "FOR"
    return new_btn

def would_exceed_console_limit(commands, console_rect, level_num):
    """
    Skontroluje, či by pridaním nového príkazu presiahla konzola svoju pravú hranicu
    
    Returns:
        bool: True ak by presiahla limit, False inak
    """
    indent_width = 30
    button_width = 100
    column_spacing = 20
    start_x = console_rect.x + 20
    slot_height = 50
    button_height = 50
    
    # Vypočíta koľko príkazov sa zmestí do jedného stĺpca
    available_height = console_rect.height - 20
    max_commands_per_column = max(1, available_height // slot_height)
    
    # Vypočíta pozíciu, kde by sa nový príkaz umiestnil
    new_index = len(commands)
    
    if level_num >= 2:
        # Pre level 2+ s odsadením - vypočíta indent_level nového príkazu
        indent_level = 0
        for cmd in commands:
            if cmd.command == "for_start":
                indent_level += 1
            elif cmd.command == "for_end":
                indent_level = max(0, indent_level - 1)
        
        # Vypočíta maximálne odsadenie v existujúcich príkazoch
        max_indent = max([c.indent_level for c in commands], default=0) if commands else 0
        column_width = button_width + max_indent * indent_width + column_spacing
        
        # Vypočíta stĺpec a riadok pre nový príkaz
        row_in_column = new_index % max_commands_per_column
        current_column = new_index // max_commands_per_column
        
        # Vypočíta x pozíciu (základná pozícia + odsadenie + offset stĺpca)
        x_pos = start_x + indent_level * indent_width + current_column * column_width
    else:
        # Pre level 1 bez odsadenia
        column_width = button_width + column_spacing
        column = new_index // max_commands_per_column
        x_pos = start_x + column * column_width
    
    # Kontrola, či by presiahlo pravú hranicu konzoly
    return x_pos + button_width > console_rect.right
