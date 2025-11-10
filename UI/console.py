import pygame

def draw_console(screen: pygame.Surface, level_config: dict):
    
    grid_w = level_config["GRID_WIDTH"]
    grid_h = level_config["GRID_HEIGHT"]
    console_w = level_config["CONSOLE_WIDTH"]
    
    x = grid_w
    y = 0
    
    console_rect = pygame.Rect(x,y,console_w,grid_h)
    
    CONSOLE_BG = (145,120,112) ; CONSOLE_BORDER = (100,80,75)
    
    pygame.draw.rect(screen, CONSOLE_BG, console_rect)
    pygame.draw.rect(screen,CONSOLE_BORDER,console_rect,width=3)
    return console_rect