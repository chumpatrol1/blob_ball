from .base_class import em_base_class # Main Class

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_royal_loan(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity
        
        if(self.lifetime == 1):
            self.lifetime = 0
        elif(self.hp >= 8):
            self.lifetime = 1