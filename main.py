import pygame,sys
from window import Window
from settings import MENU_IMG, set_level_size
from menu import draw_menu
from showlevels import draw_showlevels
from UI.grid import draw_grid
from UI.console import draw_console
from UI.panel import draw_panel, panel_buttons, buttons_for_level
from UI.start_button import draw_start_button
from UI.draggable_button import draggableButton

pygame.init()
window = Window(background_path=MENU_IMG)

clock = pygame.time.Clock()
running = True
state = "menu"

dragging_button = None

console_commands = []

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    if state == "menu":
        window.draw_background()
        buttons = draw_menu(window.screen, mouse_pos)
        
    elif state == "levels":
        buttons = draw_showlevels(window.screen, mouse_pos)
        
    elif state.startswith("Level"):
        level_num = int(state.split()[1])
        window.draw_background((131, 106, 98))
        level_config = set_level_size(level_num - 1)
        
        draw_grid(window.screen, level_config)
        console_rect = draw_console(window.screen,level_config)
        
        panel_rect = draw_panel(window.screen,level_config)
        draw_start_button(window.screen,level_config,mouse_pos)
        
        if not panel_buttons:
            buttons_for_level(level_num,panel_rect)
        
        font = pygame.font.SysFont("Consolas", 20, bold=True)
        for b in panel_buttons:
            b.draw(window.screen, font, (210, 210, 210), (50, 50, 50))
            
        for cmd in console_commands:
            cmd.draw(window.screen, font, (190,190,190), (40,40,40))


        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.VIDEORESIZE:
            window.resize(event.w,event.h)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            if state in ("menu","levels"):
                for text, rect in buttons:
                    if rect.collidepoint(mx,my):
                        if state == "menu":
                            if text == "Zoznam levelov":
                                state = "levels"
                            elif text == "Koniec":
                                running = False
                                
                        elif state == "levels":
                            if text.startswith("Level"):
                                state = text
                                panel_buttons.clear()
                            elif text == "Späť":
                                state = "menu"
                              
            elif state.startswith("Level"):
                for btn in panel_buttons:
                    if btn.start_drag((mx,my)):
                        dragging_button = btn
                        break
        
        elif event.type == pygame.MOUSEMOTION:
            if dragging_button:
                dragging_button.drag(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_button:
                dragging_button.stop_drag()
                
                if console_rect.collidepoint(dragging_button.rect.center):
                    #Kópia tlačidla
                    new_btn = draggableButton(
                        dragging_button.rect.x,
                        dragging_button.rect.y,
                        100,
                        50,
                        dragging_button.label,
                        dragging_button.command
                        )
                    console_commands.append(new_btn)
                    
                    slot_height = 50
                    index = len(console_commands) - 1
                    
                    new_btn.rect.x = console_rect.x + 20
                    new_btn.rect.y = console_rect.y + 10 + index * slot_height

                dragging_button.reset_position()
                dragging_button = None
                            
    pygame.display.flip()
    clock.tick(60)
