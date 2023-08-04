from .base_class import em_base_class # Main Class
from math import sin, cos, radians, pi
from resources.sound_engine.sfx_event import createSFXEvent

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_bubble(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        self.x_orbit = 0
        self.y_orbit = 0
    def update(self):
        self.x_pos += self.x_speed + self.x_orbit
        self.y_pos += self.y_speed + self.y_orbit
        self.lifetime -= 1

        if(self.x_pos < 0):
            self.x_pos = 0
        elif(self.x_pos > 1700):
            self.x_pos = 1700
        
        if(self.y_pos > 1300): # Common case
            self.y_pos = 1300
        elif(self.y_pos < 0): # Happens more rarely
            self.y_pos = 0

        
        
        if(-1 < self.x_speed < 1):
            self.x_speed = 0

        if(self.x_speed > 1):
            self.x_speed -= 1
        
        if(self.x_speed < -1):
            self.x_speed += 1

        if(-1 < self.y_speed < 1):
            self.y_speed = 0

        if(self.y_speed > 1):
            self.y_speed -= 1
        
        if(self.y_speed < -1):
            self.y_speed += 1


        if(self.species == 'bubble' and self.lifetime < self.max_lifetime):
            if(self.player == 1):
                self.x_orbit = sin(radians((self.max_lifetime - self.lifetime) *  pi)) * 10
                self.y_orbit = cos(radians((self.max_lifetime - self.lifetime)  * pi)) * -10
            else:
                self.x_orbit = sin(radians((self.max_lifetime - self.lifetime) *  pi)) * -10
                self.y_orbit = cos(radians((self.max_lifetime - self.lifetime)  * pi)) * -10
        if(self.lifetime == 5):
            createSFXEvent('pop')

