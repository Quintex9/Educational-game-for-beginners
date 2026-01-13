import pygame

class draggableButton:
    def __init__(self, x, y, w, h, label, command):
        self.rect = pygame.Rect(x,y,w,h)
        self.start_x = x
        self.start_y = y
        self.label = label
        self.command = command
        
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        self.in_console = False
        
    def draw(self, screen, font, color, border_color):
        from settings import DRAG_BUTTON_BG, DRAG_BUTTON_HOVER, DRAG_BUTTON_BORDER, DRAG_BUTTON_SHADOW
        
        # Moderné farby
        base = DRAG_BUTTON_BG
        border = DRAG_BUTTON_BORDER
        shadow = DRAG_BUTTON_SHADOW
        hover = DRAG_BUTTON_HOVER

        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)

        # TIEŇ (len ak nie je v konzole – aby nekazil layout)
        if not self.in_console:
            shadow_rect = self.rect.move(1, 1)
            pygame.draw.rect(screen, shadow, shadow_rect, border_radius=10)

        # TELO - jednoduché bez gradientu
        if hovered:
            pygame.draw.rect(screen, hover, self.rect, border_radius=10)
        else:
            pygame.draw.rect(screen, base, self.rect, border_radius=10)

        # OKRAJ - jemnejší
        border_color_actual = (110, 140, 170) if hovered else border
        pygame.draw.rect(screen, border_color_actual, self.rect, width=1, border_radius=10)

        # TEXT bez tieňa
        text = font.render(self.label, True, (240, 245, 250))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


        
    def start_drag(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.dragging = True
            mx, my = mouse_pos
            self.offset_x = self.rect.x - mx
            self.offset_y = self.rect.y - my
            return True
        return False
    
    def drag(self, mouse_pos):
        if self.dragging:
            mx, my = mouse_pos
            self.rect.x = mx + self.offset_x
            self.rect.y = my + self.offset_y
            
    def stop_drag(self):
        self.dragging = False
        
    def reset_position(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
