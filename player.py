
class Player:
    def __init__(self,start_x = 0, start_y = 0):
        self.x = start_x
        self.y = start_y
        
    def set_position(self,x,y):
        self.x = x
        self.y = y
        
    def get_position(self):
        return self.x,self.y
    
    def move_up(self):
        self.y -= 1
        
    def move_down(self):
        self.y += 1
        
    def move_left(self):
        self.x -= 1
        
    def move_right(self):
        self.x += 1