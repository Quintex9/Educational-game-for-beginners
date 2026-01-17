import pygame
import math
from settings import BOARD_OUT, CELL_EDGE, GRID_SHADOW
from level_data import LEVEL_DATA

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
def draw_grid(screen: pygame.Surface, level_conf: dict,level_num):
    grid_size   = level_conf["GRID_SIZE"]
    cell_size   = level_conf["CELL_SIZE"]
    grid_width  = level_conf["GRID_WIDTH"]
    grid_height = level_conf["GRID_HEIGHT"]

    #  Načítanie tiles z floor.png 
    tiles = load_tileset("Images/floor.png", 32, 32)

    layout1 = [
        [0, 1, 1, 1, 9],
        [38, 10, 10, 10, 47],
        [38, 10, 10, 10, 47],
        [38, 10, 10, 10, 47],
        [160, 161, 161, 161, 171]
    ]
    
    layout2 = [
        [0, 1, 1, 1, 1, 9],
        [38, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 47],
        [160, 161, 161, 161, 161, 171]
    ]
    
    layout3 = [
        [0, 1, 1, 1, 1, 1, 9],
        [38, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 47],
        [160, 161, 161, 161, 161, 161, 171]
    ]
    
    layout4 = [
        [0, 1, 1, 1, 1, 1, 1, 9],
        [38, 10, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 10, 47],
        [38, 10, 10, 10, 10, 10, 10, 47],
        [160, 161, 161, 161, 161, 161, 161, 171]
    ]
    
    
    if level_num == 1:
        layout = layout1
    elif level_num == 2:
        layout = layout2
    elif level_num == 3:
        layout = layout3
    elif level_num == 4:
        layout = layout4

    # Rám mriežky s jemnejším tieňom
    grid_rect = pygame.Rect(0, 0, grid_width, grid_height)
    
    # Jemnejší tieň gridu - prírodnejšia farba
    shadow_rect = grid_rect.move(5, 5)
    pygame.draw.rect(screen, GRID_SHADOW, shadow_rect, border_radius=10)
    
    # Hlavný okraj gridu - prírodnejšia farba
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

            # Jemnejšia hranica bunky - jemnejšia farba
            pygame.draw.rect(screen, CELL_EDGE, (x, y, cell_size, cell_size), width=1)

    # Vykreslenie prekážok a cieľa
    if level_num in LEVEL_DATA:
        level_info = LEVEL_DATA[level_num]
        cell_size = level_conf["CELL_SIZE"]
        
        # Načítanie obrázka prekážky
        try:
            obstacle_img = pygame.image.load("Images/obstacle.png").convert_alpha()
        except:
            obstacle_img = None
        
        # Vykreslenie prekážok
        for obs_x, obs_y in level_info.get("obstacles", []):
            if 0 <= obs_x < grid_size and 0 <= obs_y < grid_size:
                obs_rect = pygame.Rect(
                    obs_x * cell_size,
                    obs_y * cell_size,
                    cell_size,
                    cell_size
                )
                # Použije obrázok prekážky, ak je dostupný
                if obstacle_img:
                    scaled_obstacle = pygame.transform.scale(obstacle_img, (cell_size, cell_size))
                    screen.blit(scaled_obstacle, obs_rect)
                else:
                    # Rezerva: tmavá prekážka, ak obrázok nie je dostupný
                    pygame.draw.rect(screen, (60, 40, 30), obs_rect)
                    pygame.draw.rect(screen, (40, 25, 15), obs_rect, width=2)
                    # Kresba X na prekážke
                    pygame.draw.line(screen, (100, 50, 30), 
                                   (obs_rect.left + 5, obs_rect.top + 5),
                                   (obs_rect.right - 5, obs_rect.bottom - 5), width=3)
                    pygame.draw.line(screen, (100, 50, 30),
                                   (obs_rect.right - 5, obs_rect.top + 5),
                                   (obs_rect.left + 5, obs_rect.bottom - 5), width=3)
        
        # Načítanie obrázka dverí a vystrihnutie posledných otvorených dverí
        door_img = None
        try:
            doors_sheet = pygame.image.load("Images/portal/Doors.png").convert_alpha()
            doors_width, doors_height = doors_sheet.get_size()
            # Predpokladáme, že dvere sú usporiadané horizontálne (6 dverí v rade)
            door_width = doors_width // 6
            door_height = doors_height
            # Vystrihneme posledné dvere (6. dvere, index 5)
            door_rect = pygame.Rect(5 * door_width, 0, door_width, door_height)
            door_img = doors_sheet.subsurface(door_rect).copy()
        except Exception as e:
            print(f"Chyba pri načítaní dverí: {e}")
            door_img = None
        
        # Vykreslenie cieľa
        goal = level_info.get("goal")
        if goal:
            goal_x, goal_y = goal
            if 0 <= goal_x < grid_size and 0 <= goal_y < grid_size:
                goal_rect = pygame.Rect(
                    goal_x * cell_size,
                    goal_y * cell_size,
                    cell_size,
                    cell_size
                )
                # Použije obrázok otvorených dverí, ak je dostupný
                if door_img:
                    scaled_door = pygame.transform.scale(door_img, (cell_size, cell_size))
                    screen.blit(scaled_door, goal_rect)
                else:
                    # Rezerva: zelený cieľ, ak obrázok nie je dostupný
                    pygame.draw.rect(screen, (50, 200, 50), goal_rect)
                    pygame.draw.rect(screen, (30, 150, 30), goal_rect, width=3)
                    # Hviezda na cieli
                    center_x = goal_rect.centerx
                    center_y = goal_rect.centery
                    star_size = cell_size // 3
                    points = []
                    for i in range(10):
                        angle = (i * math.pi) / 5
                        if i % 2 == 0:
                            r = star_size
                        else:
                            r = star_size // 2
                        x = center_x + r * math.cos(angle)
                        y = center_y + r * math.sin(angle)
                        points.append((int(x), int(y)))
                    if len(points) > 2:
                        pygame.draw.polygon(screen, (255, 255, 100), points)

    return grid_rect
