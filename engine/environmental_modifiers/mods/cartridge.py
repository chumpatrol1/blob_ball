from resources.graphics_engine.display_particles import draw_cartridge_sparks
from .base_class import em_base_class # Main Class

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_cartridge(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity
        self.lifetime -= 1
        
        if(self.y_pos > 1270):
            self.y_speed *= -0.7
            self.x_speed *= 0.7
            self.y_pos = 1270
        if(self.x_pos < 0):
            self.x_pos = 0
            self.x_speed *= -0.7
        elif(self.x_pos > 1750):
            self.x_pos = 1750
            self.x_speed *= -0.7
        
        if(self.lifetime == 180):
            draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
            
        if(self.lifetime == 60):
            draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])

        if(self.lifetime == 1):
            draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
            draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
