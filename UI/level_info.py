# Info o leveloch

from game_logic.level_data import LEVEL_DATA
from rendering.popups import draw_popup


def get_level_info(level_num):
    # Vrati informacie o leveli pre popup
    if level_num not in LEVEL_DATA:
        return f"Level {level_num}", ["Informácie nie sú dostupné"]

    level_data = LEVEL_DATA[level_num]
    obstacles_count = len(level_data.get("obstacles", []))
    goal = level_data.get("goal", (0, 0))

    info_texts = {
        1: [
            "Vítaj v prvom leveli!",
            "Tvoj cieľ je prejsť dverami.",
            f"Na ceste sú {obstacles_count} prekazky.",
            "Použi príkazy UP, DOWN, LEFT, RIGHT.",
        ],
        2: [
            "Level 2 - FOR cykly!",
            "FOR cyklus sa používa na opakovanie príkazov.",
            "Slúži na skrátenie zápisu príkazov.",
            "Pretiahni FOR do konzoly a vyber počet opakovaní.",
        ],
        3: [
            "Level 3 - IF podmienka",
            "IF sa používa na podmienkove vykonávanie príkazov.",
            "Pomocou IF môžeš skontrolovať prekážku pred hráčom.",
            "Použi príkazy UP, DOWN, LEFT, RIGHT, IF.",
        ],
        4: [
            "Level 4 - Zložitejšia cesta!",
            f"Na ceste je {obstacles_count} prekážok.",
            "Využi FOR a IF pre najefektívnejšie riesenie.",
        ],
        5: [
            "Level 5 - Prvý pokročilý level!",
            f"Pozor na {obstacles_count} prekážok!",
            "Dokážes to?",
        ],
        6: [
            "Level 6 - Pokročilá logika",
            f"Na mape je {obstacles_count} prekážok.",
            "Kombinuj FOR a IF pre čisté riešenie.",
        ],
        7: [
            "Level 7 - Hustý labyrint",
            f"Čaká ťa {obstacles_count} prekážok.",
            "Planuj dopredu, každý príkaz sa ráta.",
            "Skús minimalizovať počeť resetov.",
        ],
        8: [
            "Level 8 - Finále",
            f"Posledná mapa má {obstacles_count} prekážok.",
            "Použi najlepšiu kombináciu FOR + IF + text mode.",
            "Dokaž, že más GRID RUN pod kontrolou!",
        ],
    }

    return f"Level {level_num}", info_texts.get(level_num, [f"Cieľ: pozícia {goal}", f"Prekážky: {obstacles_count}"])


def draw_level_info_popup(screen, level_num):
    """Vykresli popup s informaciami o leveli."""
    title, lines = get_level_info(level_num)
    return draw_popup(screen, title, lines, "Zacat")
