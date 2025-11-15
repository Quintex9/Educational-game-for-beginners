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
        # Normálne farby
        base = (60, 52, 48)
        border = (25, 22, 20)
        shadow = (20, 18, 17)

        # Hover farba (o 20% svetlejšia)
        hover = (80, 70, 65)

        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)

        # TIEŇ (len ak nie je v konzole – aby nekazil layout)
        if not self.in_console:
            shadow_rect = self.rect.move(3, 3)
            pygame.draw.rect(screen, shadow, shadow_rect, border_radius=8)

        # TELO
        pygame.draw.rect(screen, hover if hovered else base, self.rect, border_radius=8)

        # OKRAJ
        pygame.draw.rect(screen, border, self.rect, width=2, border_radius=8)

        # TEXT
        text = font.render(self.label, True, (230, 230, 230))
        screen.blit(text, text.get_rect(center=self.rect.center))


        
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
