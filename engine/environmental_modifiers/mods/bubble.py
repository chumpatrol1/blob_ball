from .base_class import em_base_class # Main Class
from math import sin, cos, radians, pi
from resources.sound_engine.sfx_event import createSFXEvent

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_bubble(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity
        self.lifetime -= 1

        if(self.species == 'bubble' and self.lifetime < self.max_lifetime):
            if(self.player == 1):
                self.x_speed = sin(radians((self.max_lifetime - self.lifetime) *  pi)) * 10
                self.y_speed = cos(radians((self.max_lifetime - self.lifetime)  * pi)) * -10
            else:
                self.x_speed = sin(radians((self.max_lifetime - self.lifetime) *  pi)) * -10
                self.y_speed = cos(radians((self.max_lifetime - self.lifetime)  * pi)) * -10
        if(self.lifetime == 5):
            createSFXEvent('pop')

