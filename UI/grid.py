import pygame
from settings import BOARD_OUT, CELL_EDGE

def draw_grid(screen: pygame.Surface, level_conf: dict):
    grid_size   = level_conf["GRID_SIZE"]
    cell_size   = level_conf["CELL_SIZE"]
    grid_width  = level_conf["GRID_WIDTH"]
    grid_height = level_conf["GRID_HEIGHT"]

    # Mriežka bude umiestnená vľavo hore s malým okrajom
    grid_rect = pygame.Rect(0,0, grid_width, grid_height)

    pygame.draw.rect(screen, BOARD_OUT, grid_rect, width=3, border_radius=10)

    # bunky
    for row in range(grid_size):
        for col in range(grid_size):
            x = grid_rect.x + col * cell_size
            y = grid_rect.y + row * cell_size
            cell_rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, CELL_EDGE, cell_rect, width=2)
    return grid_rect
