import pygame,sys
from window import Window
from settings import MENU_IMG
from menu import draw_menu
from showlevels import draw_showlevels



pygame.init()
window = Window(background_path=MENU_IMG)


clock = pygame.time.Clock()
running = True
state = "menu"

while running:
    mouse_pos  = pygame.mouse.get_pos()
    
    if state == "menu":
        window.draw_background()
        buttons = draw_menu(window.screen, mouse_pos)
    elif state == "levels":
        buttons = draw_showlevels(window.screen, mouse_pos)
    elif state == "Level 1":
        window.draw_background((131, 106, 98))

        
        

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window.resize(event.w,event.h)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for text, rect in buttons:
                if rect.collidepoint(mx,my):
                    if state == "menu":
                        if text == "Zoznam levelov":
                            state = "levels"
                        elif text == "Koniec":
                            running = False
                    elif state == "levels":
                        if text == "Level 1":
                            state = "Level 1"
                        elif text == "Level 2":
                            state = "Level 2"
                        elif text == "Level 3":
                            state = "Level 3"
                        elif text == "Level 4":
                            state = "Level 4"
                        elif text == "Späť":
                            state = "menu"
                            
    
    
    pygame.display.flip()
    clock.tick(60)
