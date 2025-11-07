import pygame
from settings import BUTTON_COLOR, BUTTON_HOVER, BUTTON_SHADOW, TEXT_COLOR

def draw_menu(screen: pygame.Surface,mouse_pos):
    screen_width, screen_height = screen.get_size()
    
    font_button = pygame.font.SysFont("Arial", 30, bold=True)
    
    #tlačidlá
    button_texts = ["Zoznam levelov","Koniec"]
    
    buttons = []
    
    for i, text in enumerate(button_texts):
        #Veľkosť tlačidla
        btn_width, btn_height = 250,100
        
        #Pozícia tlačidla
        btn_x = screen_width // 2 - btn_width // 2
        btn_y = screen_height // 2 - 45  + i * 120
        
        rect = pygame.Rect(btn_x,btn_y,btn_width,btn_height)
        
        #Vyvorenie kópie pôvodného rect, posunie o 6 px na osi x,y
        shadow_rect = rect.move(6,6)
        pygame.draw.rect(screen,BUTTON_SHADOW,shadow_rect,border_radius=10)
        
        
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen,color, rect, border_radius=12)
        
        txt = font_button.render(text, True, TEXT_COLOR)
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)
        
        buttons.append((text,rect))
        
    return buttons
        