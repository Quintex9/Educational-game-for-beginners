import pygame
import os

class Player:
    def __init__(self, start_x=0, start_y=0):
        self.x = start_x
        self.y = start_y
        self.direction = "down"  # default smer
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # snímky na animáciu
        
        # Načítanie sprite obrázkov
        self.sprites = {}
        base_path = "Images/player"
        directions = ["down", "left", "right", "up"]
        
        for direction in directions:
            self.sprites[direction] = []
            for i in range(4):
                img_path = os.path.join(base_path, direction, f"{i}.png")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    self.sprites[direction].append(img)
                else:
                    # Rezerva: vytvorí červený obdĺžnik, ak obrázok nie je nájdený
                    surf = pygame.Surface((32, 32))
                    surf.fill((255, 0, 0))
                    self.sprites[direction].append(surf)
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        
    def get_position(self):
        return self.x, self.y
    
    def set_direction(self, direction):
        #Nastaví smer: 'up', 'down', 'left', 'right'
        if direction in self.sprites:
            self.direction = direction
    
    def move_up(self):
        self.y -= 1
        self.set_direction("up")
        self.animation_frame = (self.animation_frame + 1) % 4
        
    def move_down(self):
        self.y += 1
        self.set_direction("down")
        self.animation_frame = (self.animation_frame + 1) % 4
        
    def move_left(self):
        self.x -= 1
        self.set_direction("left")
        self.animation_frame = (self.animation_frame + 1) % 4
        
    def move_right(self):
        self.x += 1
        self.set_direction("right")
        self.animation_frame = (self.animation_frame + 1) % 4
    
    def get_sprite(self):
        #Získa aktuálny sprite obrázok na základe smeru a animačného snímku
        if self.direction in self.sprites and len(self.sprites[self.direction]) > 0:
            return self.sprites[self.direction][self.animation_frame]
        return None
    
    def update_animation(self):
        #Aktualizuje animačný snímok
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4