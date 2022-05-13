from os import environ


class EnvironmentalModifiers:
    def __init__(self, player = 0, affects = set(), species = "", x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60):
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

    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        #if(self.y_pos > 685 - self.image.get_height()/2 and not self.ground_clip):
        #    self.y_pos = 685 - self.image.get_height()/2
        self.y_speed += self.gravity
        self.lifetime -= 1
        if(self.species == 'glue_shot' and self.y_pos > 1350):
            create_environmental_modifier(self.player, affects = {'enemy'}, species = 'glue_puddle', x_pos = self.x_pos - 27.5, y_pos = 1380, lifetime = 180)
            self.lifetime = 0

# FOR EACH MODIFIER, ADD A NEW ENTRY!
environmental_modifiers = {
    'glue_shot': [],
    'glue_puddle': [],
}

def create_environmental_modifier(player = 0, affects = set(), species = "", x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60):
    global environmental_modifiers
    if(species in environmental_modifiers):
        environmental_modifiers[species].append(EnvironmentalModifiers(player, affects, species, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime))
    else:
        environmental_modifiers[species] = [EnvironmentalModifiers(player, affects, species, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime)]

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
    environmental_modifiers = environmental_modifiers = {
    'glue_shot': [],
    'glue_puddle': [],
}