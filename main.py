import pygame,sys
from window import Window
from settings import MENU_IMG

pygame.init()
window = Window(background_path=MENU_IMG)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window.resize(event.w,event.h)
    
    window.draw_background()
    pygame.display.flip()
    clock.tick(60)