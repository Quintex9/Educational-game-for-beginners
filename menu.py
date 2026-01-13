import pygame
from settings import BUTTON_COLOR, BUTTON_HOVER, BUTTON_SHADOW, TEXT_COLOR

def draw_menu(screen: pygame.Surface, mouse_pos):
    screen_width, screen_height = screen.get_size()
    
    font_button = pygame.font.SysFont("Consolas", 32, bold=True)
    
    #tlačidlá
    button_texts = ["Zoznam levelov", "Koniec"]
    
    buttons = []
    
    for i, text in enumerate(button_texts):
        #Veľkosť tlačidla
        btn_width, btn_height = 280, 80
        
        #Pozícia tlačidla
        btn_x = screen_width // 2 - btn_width // 2
        btn_y = screen_height // 2 - 30 + i * 110
        
        rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        hovered = rect.collidepoint(mouse_pos)
        
        # Veľmi jemný tieň
        shadow_rect = rect.move(2, 2)
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=15)
        
        # Jednoduché tlačidlo bez gradientu
        color = BUTTON_HOVER if hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=15)
        
        # Jemnejší okraj
        border_color = (130, 180, 240) if hovered else (90, 140, 210)
        pygame.draw.rect(screen, border_color, rect, width=1, border_radius=15)
        
        # Text bez tieňa - čistejší vzhľad
        txt = font_button.render(text, True, TEXT_COLOR)
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)
        
        buttons.append((text, rect))
        
    return buttons
        