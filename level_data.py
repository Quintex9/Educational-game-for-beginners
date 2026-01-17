"""
Definície levelov s prekážkami a cieľom
Každý level má:
- obstacles: zoznam (x, y) pozícií prekážok
- goal: (x, y) pozícia cieľa
- start: (x, y) štartovacia pozícia hráča
"""

LEVEL_DATA = {
    1: {
        "start": (0, 0),
        "goal": (3, 3),
        "obstacles": [(2, 1), (2, 2), (2, 3)]
    },
    2: {
        "start": (0, 0),
        "goal": (5, 5),
        "obstacles": [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4)]
    },
    3: {
        "start": (0, 0),
        "goal": (6, 6),
        "obstacles": [(2, 1), (2, 2), (2, 3), (4, 2), (4, 3), (4, 4), (1, 4), (3, 4)]
    },
    4: {
        "start": (0, 0),
        "goal": (7, 7),
        "obstacles": [(1, 1), (2, 2), (3, 3), (4, 4), (5, 3), (3, 5), (2, 5), (5, 5)]
    }
}
