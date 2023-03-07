from resources.graphics_engine.display_particles import draw_spire_dirt, draw_console_sparks, draw_cartridge_sparks
from random import randint


class EnvironmentalModifiers:
    def __init__(self, player = 0, affects = set(), species = "", random_image = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60, hp = 1):
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
        self.hp = hp

    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        #if(self.y_pos > 685 - self.image.get_height()/2 and not self.ground_clip):
        #    self.y_pos = 685 - self.image.get_height()/2
        self.y_speed += self.gravity
        self.lifetime -= 1 if self.species != "royal_loan" else 0
        if(self.species == "royal_loan" and self.lifetime == 1):
            self.lifetime = 0
        elif(self.species == "royal_loan" and self.hp >= 8):
            self.lifetime = 1
        
        if(self.species == 'glue_shot' and self.y_pos > 1350):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'glue_puddle', random_image = self.player, x_pos = self.x_pos - 27.5, y_pos = 1378, lifetime = 600)
            self.lifetime = 0
        
        if(self.species == 'glue_shot' and (self.x_pos < 0 or self.x_pos > 1835)):
            self.x_speed *= -0.625
            self.x_pos += self.x_speed * 2
        
        if(self.species == 'spire_glyph' and self.lifetime == 0):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'spire_spike', x_pos = self.x_pos, y_pos = 500, lifetime = 85)
            draw_spire_dirt(self.x_pos)

        if(self.species == 'thunder_glyph' and self.lifetime == 0):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'thunder_bolt', random_image = randint(1, 2), x_pos = self.x_pos, y_pos = 112, lifetime = 35)

        if(self.species == 'starpunch_wait' and self.lifetime == 0):
            create_environmental_modifier(player = self.player, affects = self.affects, species = 'starpunch', x_pos = self.x_pos, y_pos = self.y_pos, lifetime = 30)

        if(self.species == 'cartridge'):
            if(self.y_pos > 1270):
                self.y_speed *= -0.9
                self.x_speed *= 0.9
                self.y_pos = 1270
            if(self.x_pos < 0):
                self.x_pos = 0
                self.x_speed *= -0.9
            elif(self.x_pos > 1750):
                self.x_pos = 1750
                self.x_speed *= -0.9
        
            if(self.lifetime == 180):
                draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
            
            if(self.lifetime == 60):
                draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])

            if(self.lifetime == 1):
                draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])
                draw_cartridge_sparks([self.x_pos, self.y_pos], [self.x_speed, self.y_speed])

        if(self.species == 'console' and self.y_pos > 1270):
            self.y_pos = 1270
            self.y_speed = 0
            self.gravity = 0
        if(self.species == 'console' and (self.lifetime == self.max_lifetime - 300 or self.lifetime == 180 or self.lifetime == 60)):
            draw_console_sparks([self.x_pos, self.y_pos])
        if(self.species == 'console' and (self.lifetime == 1 or self.hp <= 0)):
            draw_console_sparks([self.x_pos, self.y_pos])
            draw_console_sparks([self.x_pos, self.y_pos])
            draw_console_sparks([self.x_pos, self.y_pos])
        
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
    'console': [],
    'cartridge': [],
    'royal_loan': [],
    'cactus_spike': [],
    'sharp_shadow': [],
}

def create_environmental_modifier(player = 0, affects = set(), species = "", random_image = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60, hp = 1):
    global environmental_modifiers
    if(species in environmental_modifiers):
        environmental_modifiers[species].append(EnvironmentalModifiers(player, affects, species, random_image, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime, hp))
    else:
        environmental_modifiers[species] = [EnvironmentalModifiers(player, affects, species, random_image, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime, hp)]

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
    shot_glue = environmental_modifiers['glue_puddle']
    unpaid_loans = environmental_modifiers['royal_loan']
    environmental_modifiers = {
    'glue_shot': [],
    'glue_puddle': shot_glue,
    'spire_glyph': [],
    'spire_spike': [],
    'thunder_glyph': [],
    'thunder_bolt': [],
    'starpunch_wait': [],
    'starpunch': [],
    'starpunch_spring': [],
    'console': [],
    'cartridge': [],
    'royal_loan': unpaid_loans,
    'cactus_spike': [],
    'sharp_shadow': [],
}