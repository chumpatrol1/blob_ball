from engine.environmental_modifiers import return_environmental_modifiers
from resources.graphics_engine.display_particles import return_particle_cache
import pygame as pg

modifier_images = {
    'glue_shot': 'glue_shot',
    'glue_puddle': 'glue_puddle_1',
    'glue_puddle_1': 'glue_puddle_1',
    'glue_puddle_2': 'glue_puddle_2',
    'spire_glyph': 'rock_glyph',
    'spire_spike': 'rock_spire',
    'thunder_glyph': 'thunder_glyph',
    'thunder_bolt': 'thunder_bolt_1',
    'thunder_bolt_1': 'thunder_bolt_1',
    'thunder_bolt_2': 'thunder_bolt_2', 
    'starpunch_wait': 'star_glove',
    'starpunch': 'star_glove',
    'starpunch_spring': 'spring_particle',
    'console': 'console',
    'cartridge': 'cartridge_1',
    'cartridge_1': 'cartridge_1',
    'cartridge_2': 'cartridge_2',
    'cartridge_3': 'cartridge_3',
}

#alpha = 255 * ((p1_blob.special_ability_cooldown_max - p1_blob.special_ability_timer)/(p1_blob.special_ability_delay))

def draw_environmental_modifiers(game_display, ):
    modifiers = return_environmental_modifiers()
    particle_cache = return_particle_cache()
    mod_key = ''
    for modifier in modifiers:
        mod_key = modifier_images[modifier]
        if(modifier == 'spire_glyph'):
            for individual in modifiers[modifier]:
                image = particle_cache[mod_key]
                image.set_alpha(255 * ((individual.max_lifetime - individual.lifetime)/(individual.max_lifetime)))
                game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366), individual.y_pos))
        elif(modifier == 'spire_spike'):
            for individual in modifiers[modifier]:
                image = particle_cache[mod_key]
                image.set_alpha(255 * ((individual.lifetime)/(individual.max_lifetime)))
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos))
        elif(modifier == 'thunder_glyph'):
            for individual in modifiers[modifier]:
                image = particle_cache[mod_key]
                image.set_alpha(255 * ((individual.max_lifetime - individual.lifetime)/(individual.max_lifetime)))
                game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366), individual.y_pos))
        elif(modifier == 'thunder_bolt'):
            for individual in modifiers[modifier]:
                image = particle_cache['thunder_bolt_' + str(individual.random_image)]
                image.set_alpha(255 * ((individual.lifetime)/(individual.max_lifetime)))
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos))
        elif(modifier == 'starpunch_spring'):
             for individual in modifiers[modifier]:
                image = particle_cache[mod_key]
                image.set_alpha(255 * ((individual.lifetime)/(individual.max_lifetime)))
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
        elif(modifier == 'starpunch'):
             for individual in modifiers[modifier]:
                image = particle_cache[mod_key].convert_alpha()
                image.set_alpha(255 * ((individual.lifetime)/(individual.max_lifetime)))
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
        elif(modifier == 'glue_puddle'):
            for individual in modifiers[modifier]:
                image = particle_cache['glue_puddle_' + str(individual.random_image)]
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
        elif(modifier == 'cartridge'):
            for individual in modifiers[modifier]:
                tint = {
                    1: (255, 0, 0, 255),
                    2: (0, 0, 255, 255),
                    3: (0, 0, 0, 255), # IDK if green or yellow?
                    4: (255, 255, 255, 255)
                }
                tc = tint[individual.player] if individual.player in tint else (0, 0, 0, 0)
                image = particle_cache['cartridge_' + str(individual.random_image)].copy()
                image.fill(tc, special_flags=pg.BLEND_RGBA_MULT)
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
        elif(modifier == 'console'):
            for individual in modifiers[modifier]:
                tint = {
                    1: (255, 0, 0, 255),
                    2: (0, 0, 255, 255),
                    3: (0, 0, 0, 255), # IDK if green or yellow?
                    4: (255, 255, 255, 255)
                }
                tc = tint[individual.player] if individual.player in tint else (0, 0, 0, 0)
                image = particle_cache['console'].copy()
                image.fill(tc, special_flags=pg.BLEND_RGBA_MULT)
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
        else:
            for individual in modifiers[modifier]:
                game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))