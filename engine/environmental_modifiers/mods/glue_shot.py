from .base_class import em_base_class # Main Class

# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_glue_shot(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
        self.create_environmental_modifier = args[len(args)-1][0] # Should be the cem function.
        
    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        
        self.y_speed += self.gravity
        self.lifetime -= 1
        
        if(self.y_pos > 1350): # Hit ground?
            self.create_environmental_modifier(player = self.player, affects = self.affects, species = 'glue_puddle', random_image = self.player, x_pos = self.x_pos - 27.5, y_pos = 1378, lifetime = 600)
            self.lifetime = 0
        
        if(self.x_pos < 0 or self.x_pos > 1835): # Hit sides?
            self.x_speed *= -0.625
            self.x_pos += self.x_speed * 2

