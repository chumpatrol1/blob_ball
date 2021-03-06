from engine.environmental_modifiers import return_environmental_modifiers
from resources.graphics_engine.display_particles import return_particle_cache

modifier_images = {
    'glue_shot': 'glue_shot',
    'glue_puddle_1': 'glue_puddle_1',
    'glue_puddle_2': 'glue_puddle_2',
    'spire_glyph': 'rock_glyph',
    'spire_spike': 'rock_spire',
    'thunder_glyph': 'thunder_glyph',
    'thunder_bolt': 'thunder_bolt_1',
    'thunder_bolt_1': 'thunder_bolt_1',
    'thunder_bolt_2': 'thunder_bolt_2', 
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
        else:
            for individual in modifiers[modifier]:
                game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))