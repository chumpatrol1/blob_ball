from engine.environmental_modifiers import return_environmental_modifiers
from resources.graphics_engine.display_particles import return_particle_cache

modifier_images = {
    'glue_shot': 'glue_shot',
    'glue_puddle': 'glue_puddle',
}

def draw_environmental_modifiers(game_display, ):
    modifiers = return_environmental_modifiers()
    particle_cache = return_particle_cache()
    mod_key = ''
    for modifier in modifiers:
        mod_key = modifier_images[modifier]
        for individual in modifiers[modifier]:
            game_display.blit(particle_cache[mod_key], (individual.x_pos * (1000/1366), individual.y_pos * (382/768)))