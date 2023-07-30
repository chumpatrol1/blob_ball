from resources.graphics_engine.display_particles import draw_spire_dirt, draw_console_sparks, draw_cartridge_sparks
from random import randint

from .mods import *

# For each modifier, add a definition. (pls keep alphabetical order, it cool)
em_def = {
    'bubble': em_bubble,
    'cartridge': em_cartridge,
    'console': em_console,
    'glue_puddle': em_glue_puddle,
    'glue_shot': em_glue_shot,
    'royal_loan': em_royal_loan,
    'spire_glyph': em_spire_glyph,
    'spire_spike': em_spire_spike,
    'starpunch': em_starpunch,
    'starpunch_spring': em_starpunch_spring,
    'starpunch_wait': em_starpunch_wait,
    'thunder_bolt': em_thunder_bolt,
    'thunder_glyph': em_thunder_glyph
}

# This needs to kept around so we actually know what classes to terminate after a true_reset.
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
    'bubble': [],
}

def create_environmental_modifier(player = 0, affects = set(), species = "", random_image = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60, hp = 1, special_functions = []):
    global environmental_modifiers, em_def
    if(species in environmental_modifiers):
        if(species == "royal_loan"):
            for loan_item in environmental_modifiers["royal_loan"]:
                if(loan_item.player == player):
                    loan_item.hp += 2
                    return
        environmental_modifiers[species].append(em_def[species](player, affects, species, random_image, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime, hp, special_functions))
    else:
        environmental_modifiers[species] = [em_def[species](player, affects, species, random_image, x_pos, y_pos, x_speed, y_speed, gravity, ground_clip, lifetime, hp, special_functions)]

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

def clear_environmental_modifiers(true_reset = False):
    global environmental_modifiers
    shot_glue = environmental_modifiers['glue_puddle']
    unpaid_loans = environmental_modifiers['royal_loan']
    environmental_modifiers = {
    'glue_shot': [],
    'glue_puddle': shot_glue if not true_reset else [],
    'spire_glyph': [],
    'spire_spike': [],
    'thunder_glyph': [],
    'thunder_bolt': [],
    'starpunch_wait': [],
    'starpunch': [],
    'starpunch_spring': [],
    'console': [],
    'cartridge': [],
    'royal_loan': unpaid_loans if not true_reset else [],
    'cactus_spike': [],
    'sharp_shadow': [],
    'bubble': [],
}