import pygame,sys
from window import Window
from settings import MENU_IMG, set_level_size
from menu import draw_menu
from showlevels import draw_showlevels
from UI.grid import draw_grid
from UI.console import draw_console
from UI.panel import draw_panel
from UI.button import draw_button



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
        level_config = set_level_size(0)
        draw_grid(window.screen, level_config)
        draw_console(window.screen,level_config)
        draw_panel(window.screen,level_config)
        draw_button(window.screen,level_config)

        
        

    
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
