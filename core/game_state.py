
from core.player import Player
from game_logic.level_data import LEVEL_DATA

class GameState:
    #Trieda pre správu stavu hry
    def __init__(self):
        self.state = "menu"
        self.dragging_button = None
        self.player = None
        self.console_commands = []
        self.command_queue = []
        self.command_delay = 500
        self.last_command_time = 0
        self.executing_commands = False
        self.level_completed = False
        self.for_selection_active = None
        self.if_selection_active = None  # Index príkazu IF v konzole pre výber podmienky
        self.move_selection_active = None  # Index príkazu v konzole, ktorý sa má zmeniť
        self.level_num = None
        self.dynamic_obstacles = []  # Dynamický zoznam prekážok pre aktuálny level (môže sa meniť)
        self.show_level_info = False  # Flag pre zobrazenie info o leveli
        self.show_victory = False  # Flag pre zobrazenie výhry
        self.next_level_num = None  # Číslo ďalšieho levelu (ak existuje)
        self.show_limit_warning = False  # Flag pre zobrazenie upozornenia o limite
        self.show_error = False  # Flag pre zobrazenie error popup
        self.error_message = ""  # Správa error popup
        self.show_stars_info = False  # Flag pre zobrazenie informácií o hviezdičkách
        # Textová konzola pre levely 5-8
        self.text_mode = False  # True = textový režim, False = drag&drop režim (pre levely 5-8)
        self.text_console_input = ""  # Text v textovej konzole
        self.text_console_active = False  # Či je textová konzola aktívna (focused)
        self.text_console_cursor_pos = 0  # Pozícia kurzora v texte (index znaku)
        self.text_console_selection_start = None  # Začiatok výberu textu (pre prepisovanie)
        self.text_console_selection_end = None  # Koniec výberu textu
        # Metriky pre hodnotenie hviezdičkami
        self.stars_earned = 0  # Počet získaných hviezdičiek (0-3)
        self.reset_count = 0  # Počet resetov počas levelu
        self.used_text_mode_only = True  # Pre levely 5-8: či použili len textový režim
        self.total_commands_used = 0  # Celkový počet príkazov použitých počas levelu
        self.total_commands_list = []  # Zoznam všetkých príkazov použitých počas levelu (pre detekciu FOR/IF)
    
    def reset_level_state(self):
        #Resetuje stav pri zmene levelu
        self.console_commands.clear()
        self.command_queue.clear()
        self.executing_commands = False
        self.level_completed = False
        self.for_selection_active = None
        self.if_selection_active = None
        self.move_selection_active = None
        self.dynamic_obstacles = []
        self.show_level_info = False
        self.show_victory = False
        self.next_level_num = None
        self.show_limit_warning = False
        self.show_error = False
        self.error_message = ""
        self.show_stars_info = False
        # Reset textovej konzoly
        self.text_console_input = ""
        self.text_console_active = False
        self.text_console_cursor_pos = 0
        self.text_console_selection_start = None
        self.text_console_selection_end = None
        # Reset metrík pre hodnotenie
        self.stars_earned = 0
        self.reset_count = 0
        self.used_text_mode_only = True
        self.total_commands_used = 0
        self.total_commands_list = []
        # text_mode sa nastavuje v initialize_level() po nastavení level_num
    
    def initialize_level(self, level_num):
        #Inicializuje level s hráčom na správnej pozícii
        self.level_num = level_num
        self.reset_level_state()
        self.show_level_info = True  # Zobrazí info popup pri spustení levelu
        
        # Pre levely 5-8: defaultne drag&drop režim
        if 5 <= level_num <= 8:
            self.text_mode = False
            self.used_text_mode_only = True  # Začína s True, ak prepnú na drag&drop, nastaví sa na False
        
        if level_num in LEVEL_DATA:
            start_pos = LEVEL_DATA[level_num].get("start", (0, 0))
            self.player = Player(start_pos[0], start_pos[1])
            # Inicializuje dynamický zoznam prekážok z LEVEL_DATA
            obstacles = LEVEL_DATA[level_num].get("obstacles", [])
            self.dynamic_obstacles = list(obstacles)  # Kópia zoznamu
        else:
            self.player = Player(0, 0)
            self.dynamic_obstacles = []
    
    def reset_to_menu(self):
        #Resetuje všetko pri návrate do menu
        self.state = "menu"
        self.reset_level_state()
        self.player = None
        self.level_num = None
