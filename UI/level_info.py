# Info o leveloch

from game_logic.level_data import LEVEL_DATA
from rendering.popups import draw_popup

def get_level_info(level_num):
    #Vráti informácie o leveli pre popup
    if level_num not in LEVEL_DATA:
        return f"Level {level_num}", ["Informácie nie sú dostupné"]
    
    level_data = LEVEL_DATA[level_num]
    obstacles_count = len(level_data.get("obstacles", []))
    goal = level_data.get("goal", (0, 0))
    
    info_texts = {
        1: ["Vitaj v prvom leveli!", f"Tvoj cieľ je dostať sa do cieľa.", 
            f"Na ceste sú {obstacles_count} prekážky.", "Použij príkazy UP, DOWN, LEFT, RIGHT."],
        2: ["Level 2 - FOR cykly!", "For cyklus sa používa na opakovanie príkazov.",
            "Slúži na skrátenie zápisu príkazov.", "Pretiahni FOR do konzoly a vyber počet opakovaní."],
        3: ["Level 3 - IF podmienka", "IF sa používa na podmienkové vykonávanie príkazov.",
            "Pomocou IF môžeš skontrolovať, či je na danom mieste prekážka.", "Použij príkazy UP, DOWN, LEFT, RIGHT, IF."],
        4: ["Level 4 - Zložitejšia cesta!",
            f"Na ceste je {obstacles_count} prekážok.", "Využij FOR cykly a IF/ELSE na efektívnejšie riešenie."],
        5: ["Level 5 - Finálny level!",
            f"Pozor na {obstacles_count} prekážok!", "Dokážeš to?"]
    }
    
    return f"Level {level_num}", info_texts.get(level_num, [f"Cieľ: pozícia {goal}", f"Prekážky: {obstacles_count}"])

def draw_level_info_popup(screen, level_num):
    """Vykreslí popup s informáciami o leveli"""
    title, lines = get_level_info(level_num)
    return draw_popup(screen, title, lines, "Začať")
