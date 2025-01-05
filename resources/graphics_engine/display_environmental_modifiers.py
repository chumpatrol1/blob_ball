from engine.environmental_modifiers import return_environmental_modifiers
from resources.graphics_engine.display_particles import return_particle_cache
import pygame as pg
import math

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
    'royal_loan': 'taxation',
    'cactus_spike': 'spike_ball',
    'sharp_shadow': 'sharp_shadow',
    'bubble': 'bubble',
    'hadoukatamari': 'spike_ball',
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
        elif(modifier == 'royal_loan'):
            for individual in modifiers[modifier]:
                x_tilt = individual.hp * 10
                for hitpoint in range(individual.hp + 1):
                        game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366) + (20 * hitpoint) - x_tilt, individual.y_pos * (382/768)))
        elif(modifier == 'sharp_shadow'):
            for individual in modifiers[modifier]:
                game_display.blit(particle_cache[mod_key], ((individual.x_pos - 105) * (1000/1366), (individual.y_pos - 90) * (382/768)))
        elif(modifier == 'bubble'):
            for individual in modifiers[modifier]:
                image = particle_cache[mod_key].convert_alpha()
                if(individual.lifetime < 120):
                    bubble_alpha = 255-abs(200*math.cos(math.radians(individual.lifetime*21/4)))
                    # Good values: 27/4, 15/4, 21/4, 9/4, 3/4
                    image.set_alpha(bubble_alpha)
                
                    #print(bubble_alpha)
                game_display.blit(image, (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
                
        else:
            for individual in modifiers[modifier]:
                game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))
                #pg.draw.rect(game_display, (255, 0, 0), pg.Rect(individual.x_pos * (1000/1366) + 55, individual.y_pos * (382/768) + 55, 10, 10))