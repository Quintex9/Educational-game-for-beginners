import pygame
from settings import BOARD_OUT, CELL_EDGE

#Funkcia na rozdelenie obrázka tilesetu
def load_tileset(path, tile_width, tile_height):
    image = pygame.image.load(path).convert_alpha()
    tiles = []
    img_width, img_height = image.get_size()

    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            tile = image.subsurface(rect).copy()
            tiles.append(tile)

    return tiles


# Funkcia na vykreslenie mriežky 
def draw_grid(screen: pygame.Surface, level_conf: dict):
    grid_size   = level_conf["GRID_SIZE"]
    cell_size   = level_conf["CELL_SIZE"]
    grid_width  = level_conf["GRID_WIDTH"]
    grid_height = level_conf["GRID_HEIGHT"]

    #  Načítanie tiles z floor.png 
    tiles = load_tileset("Images/floor.png", 32, 32)

    layout = [
        [0, 1, 1, 1, 9],
        [38, 10, 10, 10, 47],
        [38, 10, 10, 10, 47],
        [38, 10, 10, 10, 47],
        [160, 161, 161, 161, 171]
    ]

    # Rám mriežky 
    grid_rect = pygame.Rect(0, 0, grid_width, grid_height)
    pygame.draw.rect(screen, BOARD_OUT, grid_rect, width=3, border_radius=10)

    #  Vykreslenie mriežky
    for row in range(grid_size):
        for col in range(grid_size):
            x = grid_rect.x + col * cell_size
            y = grid_rect.y + row * cell_size
            idx = layout[row][col] if row < len(layout) and col < len(layout[row]) else 0

            if 0 <= idx < len(tiles):
                tile_img = pygame.transform.scale(tiles[idx], (cell_size, cell_size))
                screen.blit(tile_img, (x, y))
            else:
                pygame.draw.rect(screen, (70, 150, 50), (x, y, cell_size, cell_size))

            pygame.draw.rect(screen, CELL_EDGE, (x, y, cell_size, cell_size), width=1)

    return grid_rect
