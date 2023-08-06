from resources.graphics_engine.display_particles import draw_console_sparks
from .base_class import em_base_class # Main Class

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_console(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity
        self.lifetime -= 1
    
        if(self.y_pos > 1270):
            self.y_pos = 1270
            self.y_speed = 0
            self.gravity = 0
        if(self.lifetime == self.max_lifetime - 300 or self.lifetime == 180 or self.lifetime == 60):
            draw_console_sparks([self.x_pos, self.y_pos])
        if(self.lifetime == 1 or self.hp <= 0):
            draw_console_sparks([self.x_pos, self.y_pos])
            draw_console_sparks([self.x_pos, self.y_pos])
            draw_console_sparks([self.x_pos, self.y_pos])