from resources.graphics_engine.display_particles import draw_cartridge_sparks
from .base_class import em_base_class # Main Class

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_cartridge(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        self.sparkflags = [0, 0, 0]
    
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity
        self.lifetime -= 1
        
        if(self.y_pos > 1270):
            if(abs(self.y_speed > 10)):
                draw_cartridge_sparks(int(abs(self.y_speed)/10), [self.x_pos, self.y_pos], [self.x_speed, self.y_speed], [0, int(-self.y_speed * 2)])
            self.y_speed *= -0.7
            if(abs(self.y_speed) < 2):
                self.y_speed = 0
            self.lifetime -= 10
            self.x_speed *= 0.7
            self.y_pos = 1270
        if(self.x_pos < 0):
            self.x_pos = 0
            self.lifetime -= 10
            if(abs(self.x_speed > 10)):
                draw_cartridge_sparks(int(abs(self.x_speed)/10), [self.x_pos, self.y_pos], [self.x_speed, self.y_speed], [int(self.x_speed * 1.5), 0])
            self.x_speed *= -0.7
        elif(self.x_pos > 1750):
            self.x_pos = 1750
            self.lifetime -= 10
            if(abs(self.x_speed > 10)):
                draw_cartridge_sparks(int(abs(self.x_speed)/10), [self.x_pos, self.y_pos], [self.x_speed, self.y_speed], [int(-self.x_speed * 1.5), 0])
            self.x_speed *= -0.7
        
        if(self.lifetime <= 180 and not self.sparkflags[0]):
            draw_cartridge_sparks(3, [self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
            self.sparkflags[0] = 1
            
        if(self.lifetime <= 60 and not self.sparkflags[1]):
            draw_cartridge_sparks(3, [self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
            self.sparkflags[1] = 1

        if(self.lifetime <= 1 and not self.sparkflags[2]):
            draw_cartridge_sparks(6, [self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
            self.sparkflags[2] = 1