from resources.graphics_engine.display_particles import draw_spire_dirt
from random import randint


class EnvironmentalModifiers:
    def __init__(self, player = 0, affects = set(), species = "", random_image = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60):
        self.player = player # 0 is a general hazard spawned by the stage, else player # spawned it
        '''
        'self': affects only the player that spawned it
        'team': affects only teammates
        'enemy': affects only the enemy
        'ball': affects only the ball
        '''
        self.affects = affects # Empty set means it affects no one - adding things to it increases # of targets
        self.species = species # Different species means it has a different effect
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.gravity = gravity
        self.ground_clip = ground_clip
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.random_image = random_image

    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        #if(self.y_pos > 685 - self.image.get_height()/2 and not self.ground_clip):
        #    self.y_pos = 685 - self.image.get_height()/2
        self.y_speed += self.gravity
        self.lifetime -= 1
        if(self.species == 'glue_shot' and self.y_pos > 1350):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'glue_puddle', random_image = self.player, x_pos = self.x_pos - 27.5, y_pos = 1378, lifetime = 180)
            self.lifetime = 0
        
        if(self.species == 'spire_glyph' and self.lifetime == 0):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'spire_spike', x_pos = self.x_pos, y_pos = 500, lifetime = 85)
            draw_spire_dirt(self.x_pos)

        if(self.species == 'thunder_glyph' and self.lifetime == 0):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'thunder_bolt', random_image = randint(1, 2), x_pos = self.x_pos, y_pos = 112, lifetime = 35)

        if(self.species == 'starpunch_wait' and self.lifetime == 0):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'starpunch', x_pos = self.x_pos, y_pos = self.y_pos, lifetime = 30)

# FOR EACH MODIFIER, ADD A NEW ENTRY!
environmental_modifiers = {
    'glue_shot': [],
    'glue_puddle': [],
    'spire_glyph': [],
    'spire_spike': [],
    'thunder_glyph': [],
    'thunder_bolt': [],
    'starpunch_wait': [],
    'starpunch': [],
    'starpunch_spring': [],
}

def create_environmental_modifier(player = 0, affects = set(), species = "", random_image = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60):
    global environmental_modifiers
    if(species in environmental_modifiers):
        environmental_modifiers[species].append(EnvironmentalModifiers(player, affects, species, random_image, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime))
    else:
        environmental_modifiers[species] = [EnvironmentalModifiers(player, affects, species, random_image, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime)]

def update_environmental_modifiers():
    global environmental_modifiers
    for mod_type in environmental_modifiers:
        n_mod = []
        for modifier in environmental_modifiers[mod_type]:
            modifier.update()
            if(modifier.lifetime > 0):
                n_mod.append(modifier)
        environmental_modifiers[mod_type] = n_mod

def return_environmental_modifiers():
    global environmental_modifiers
    return environmental_modifiers

def clear_environmental_modifiers():
    global environmental_modifiers
    environmental_modifiers = {
    'glue_shot': [],
    'glue_puddle': [],
    'glue_puddle': [],
    'spire_glyph': [],
    'spire_spike': [],
    'thunder_glyph': [],
    'thunder_bolt': [],
    'starpunch_wait': [],
    'starpunch': [],
    'starpunch_spring': [],
}