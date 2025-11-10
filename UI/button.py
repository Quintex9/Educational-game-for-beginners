import pygame

def draw_button(screen: pygame.display, level_config: dict):
    
    button_w = level_config["CONSOLE_WIDTH"]
    button_x = level_config["GRID_HEIGHT"]
    button_h = level_config["PANEL_HEIGHT"]
    button_rect = pygame.Rect(button_x,button_w,button_w,button_h)
    
    pygame.draw.rect(screen,(0,0,0),button_rect)
    
    return button_rect