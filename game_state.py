
from player import Player
from level_data import LEVEL_DATA

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
        self.move_selection_active = None  # Index príkazu v konzole, ktorý sa má zmeniť
        self.level_num = None
        self.show_level_info = False  # Flag pre zobrazenie info o leveli
        self.show_victory = False  # Flag pre zobrazenie výhry
        self.show_limit_warning = False  # Flag pre zobrazenie upozornenia o limite
        self.show_error = False  # Flag pre zobrazenie error popup
        self.error_message = ""  # Správa error popup
    
    def reset_level_state(self):
        #Resetuje stav pri zmene levelu
        self.console_commands.clear()
        self.command_queue.clear()
        self.executing_commands = False
        self.level_completed = False
        self.for_selection_active = None
        self.move_selection_active = None
        self.show_level_info = False
        self.show_victory = False
        self.show_limit_warning = False
        self.show_error = False
        self.error_message = ""
    
    def initialize_level(self, level_num):
        #Inicializuje level s hráčom na správnej pozícii
        self.level_num = level_num
        self.reset_level_state()
        self.show_level_info = True  # Zobrazí info popup pri spustení levelu
        
        if level_num in LEVEL_DATA:
            start_pos = LEVEL_DATA[level_num].get("start", (0, 0))
            self.player = Player(start_pos[0], start_pos[1])
        else:
            self.player = Player(0, 0)
    
    def reset_to_menu(self):
        #Resetuje všetko pri návrate do menu
        self.state = "menu"
        self.reset_level_state()
        self.player = None
        self.level_num = None
