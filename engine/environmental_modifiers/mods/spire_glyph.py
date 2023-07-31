from resources.graphics_engine.display_particles import draw_spire_dirt
from .base_class import em_base_class # Main Class

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_spire_glyph(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        self.create_environmental_modifier = args[len(args)-1][0] # Should be the cem function.
        
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        self.y_speed += self.gravity
        self.lifetime -= 1
        
        if(self.lifetime == 0):
            self.create_environmental_modifier(player = self.player, affects = self.affects, species = 'spire_spike', x_pos = self.x_pos, y_pos = 500, lifetime = 85)
            draw_spire_dirt(self.x_pos)