from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from math import ceil
import pygame as pg
import random
from random import randint
import resources.graphics_engine.dynamic_particle_handler as dpc
from resources.sound_engine.sfx_event import createSFXEvent
cwd = getcwd()

def blit_and_update_particles(memory, game_display):
    temparray = []
    for particle in memory:
        particle.image.set_alpha(particle.alpha)
        # TODO: Fix the mirror ko particle crash
        game_display.blit(particle.image, (particle.x_pos, particle.y_pos), area = particle.crop)
        particle.update()
        if not (particle.alpha <= 0) and not particle.lifetime <= 0:
           temparray.append(particle)

    memory = temparray
    return memory

def blitRotateCenter(game_display, image, topleft, angle):

    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    game_display.blit(rotated_image, new_rect)

particle_cache = {"initialized": False}
overlay_cache = {'initialized': False}
particle_memory = []
ui_memory = []

def return_particle_cache():
    global particle_cache
    return particle_cache

def draw_top_speed_particles(generator_x, particle_memory):
    '''
    HOW TO ADD A NEW PARTICLE TO THE MIX:
    CHANGE random_image = randint(0, #) to whatever # you want (it will generate a number between 0 and #, inclusive)
    ADD AN ELIF STATEMENT BY COPYING + PASTING A PREVIOUS ONE
    ENSURE THAT THE elif(random_image == #): IS SET TO AN APPROPRIATE # (OTHERWISE IT WON'T APPEAR)
    IN particle_memory.append... ENSURE THAT particle_cache['particle_name'] HAS THE CORRECT PARTICLE NAME
    '''
    global particle_cache
    if(randint(0, 1) == 1):
        random_image = randint(0, 1)
        if(random_image == 0):
            particle_memory.append(dpc.Particle(image = particle_cache['earth_particle'], x_pos = (generator_x) * (1000/1366), y_pos = 685, alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 2), y_speed = randint(-3, -1), gravity = 0.1))
        elif(random_image == 1):
            particle_memory.append(dpc.Particle(image = particle_cache['earth_particle_2'], x_pos = (generator_x) * (1000/1366), y_pos = 685, alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 2), y_speed = randint(-3, -1), gravity = 0.1))
        elif(random_image == 2):
            particle_memory.append(dpc.Particle(image = particle_cache['earth_particle_3'], x_pos = (generator_x) * (1000/1366), y_pos = 685, alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 2), y_speed = randint(-3, -1), gravity = 0.1))
    return particle_memory

def draw_landing_particles(blob):
    particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center + 50) * (1000/1366), y_pos = (blob.y_center - 25), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(1, 3), y_speed = randint(-4, -2), gravity = 0.1))
    particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center + 25) * (1000/1366), y_pos = (blob.y_center - 25), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(0, 2), y_speed = randint(-4, -2), gravity = 0.1))
    particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center) * (1000/1366), y_pos = (blob.y_center - 25), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-1, 1), y_speed = randint(-4, -2), gravity = 0.1))
    particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center - 25) * (1000/1366), y_pos = (blob.y_center - 25), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 0), y_speed = randint(-4, -2), gravity = 0.1))
    particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center - 50) * (1000/1366), y_pos = (blob.y_center - 25), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-3, -1), y_speed = randint(-4, -2), gravity = 0.1))

def create_blob_particles(blob):
    global particle_memory
    def draw_gale(blob):
        random_number = randint(0,2)
        if(random_number):
            if(blob.player == 1):
                particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = randint(-100, 1466), y_pos = randint(150, 600), alpha = 15 * randint(10, 17), fade = 1, x_speed = 3))
            elif(blob.player == 2):
                particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = randint(-100, 1466), y_pos = randint(150, 600), alpha = 15 * randint(10, 17), fade = 1, x_speed = -3))      
    used_ability_dict = {
        'gale': draw_gale,
    }

    for ability in blob.used_ability:
        if ability in used_ability_dict:
            used_ability_dict[ability](blob)

from engine.blob_stats import species_to_stars, ability_image_dict

def draw_blob_particles(game_display, blobs):
    '''HOW TO ADD TO THE PARTICLE CACHE
    COPY AND PASTE A PREVIOUS PARTICLE TO A NEW LINE
    ENSURE THAT IT HAS A UNIQUE NAME (OTHERWISE IT WILL OVERWRITE A PREVIOUS PARTICLE)
    particle_cache['fire_particle'] #GETS OVERWRITTEN
    particle_cache['ice_particle']
    particle_cache['water_particle]
    particle_cache['fire_particle'] #OVERWRITES THE ORIGINAL
    ENSURE THAT IT HAS THE CORRECT IMAGE ADDRESS
    ENSURE THAT IT HAS THE CORRECT SCALING (FOR PARTICLES THAT HAVE A SCALING FUNCTION ATTACHED)
    '''
    # TODO: Handle the particle memory a bit differently.
    global particle_memory
    if not particle_cache['initialized']:
        particle_cache['initialized'] = True
        particle_cache['fire_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/fire_particle.png").convert_alpha(), (40, 40))
        particle_cache['ice_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/ice_particle.png").convert_alpha(), (40, 40))
        particle_cache['water_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/water_particle.png").convert_alpha(), (40, 40))
        particle_cache['rock_glyph'] = pg.image.load(cwd + "/resources/images/particles/rock_glyph.png").convert_alpha()
        particle_cache['rock_spire'] = pg.image.load(cwd + "/resources/images/particles/rock_spire.png").convert_alpha()
        particle_cache['thunder_glyph'] = pg.image.load(cwd + "/resources/images/particles/thunder_glyph.png").convert_alpha()
        particle_cache['thunder_bolt_1'] = pg.image.load(cwd + "/resources/images/particles/thunder_bolt.png").convert_alpha()
        particle_cache['thunder_bolt_2'] = pg.image.load(cwd + "/resources/images/particles/thunder_bolt_2.png").convert_alpha()
        particle_cache['earth_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle.png").convert_alpha(), (20, 20))
        particle_cache['earth_particle_2'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle_2.png").convert_alpha(), (20, 20))
        particle_cache['earth_particle_3'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle_3.png").convert_alpha(), (20, 20))
        particle_cache['earth_particle_4'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle_4.png").convert_alpha(), (40, 40))
        particle_cache['landing_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/landing_particle.png").convert_alpha(), (30, 30))
        particle_cache['landing_particle_2'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/landing_particle_2.png").convert_alpha(), (30, 30))
        particle_cache['landing_particle_3'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/landing_particle_3.png").convert_alpha(), (30, 30))
        particle_cache['stoplight'] = pg.image.load(cwd + "/resources/images/ability_icons/block_icon.png").convert_alpha()
        particle_cache['star_glove'] = pg.image.load(cwd + "/resources/images/particles/star_glove.png").convert_alpha()
        particle_cache['spring_particle'] = pg.image.load(cwd + "/resources/images/particles/spring_particle.png").convert_alpha()
        particle_cache['recharge_flash'] = pg.image.load(cwd + "/resources/images/particles/recharge_flash.png").convert_alpha()
        particle_cache['energy_flash'] = pg.image.load(cwd + "/resources/images/particles/energy_flash.png").convert_alpha()
        particle_cache['damage_flash'] = pg.image.load(cwd + "/resources/images/particles/damage_flash.png").convert_alpha()
        particle_cache['heal_flash'] = pg.image.load(cwd + "/resources/images/particles/heal_flash.png").convert_alpha()
        particle_cache['block_flash'] = pg.image.load(cwd + "/resources/images/particles/block_flash.png").convert_alpha()
        particle_cache['boost_flash'] = pg.image.load(cwd + "/resources/images/particles/boost_flash.png").convert_alpha()
        particle_cache['stun_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/stun_particle.png").convert_alpha(), (30, 30))
        particle_cache['reflection_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ability_icons/mirror.png").convert_alpha(), (30, 30))
        particle_cache['shield_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/shield_particle.png").convert_alpha(), (70, 70))
        particle_cache['shatter_spritesheet'] = pg.image.load(cwd + "/resources/images/particles/shatter_spritesheet.png").convert_alpha()
        particle_cache['judgement'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/rules_icon.png").convert_alpha(), (30, 30))
        particle_cache['pill_boost'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ability_icons/pill_boost.png").convert_alpha(), (30, 30))
        particle_cache['taxation'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ability_icons/tax.png").convert_alpha(), (30, 30))
        particle_cache['glue_shot'] = pg.image.load(cwd + "/resources/images/particles/glue_shot.png").convert_alpha()
        particle_cache['glue_puddle_1'] = pg.image.load(cwd + "/resources/images/particles/glue_puddle_1.png").convert_alpha()
        particle_cache['glue_puddle_2'] = pg.image.load(cwd + "/resources/images/particles/glue_puddle_2.png").convert_alpha()
        particle_cache['smoke_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/smoke_particle.png").convert_alpha(), (40, 40))
        particle_cache['console'] = pg.image.load(cwd + "/resources/images/particles/nec.png").convert_alpha()
        particle_cache['cartridge_1'] = pg.image.load(cwd + "/resources/images/particles/cartridge_quirkio.png").convert_alpha()
        particle_cache['cartridge_2'] = pg.image.load(cwd + "/resources/images/particles/cartridge_blobbykong.png").convert_alpha()
        particle_cache['cartridge_3'] = pg.image.load(cwd + "/resources/images/particles/cartridge_legendofbloba.png").convert_alpha()
        particle_cache['glitch_particle_1'] = pg.image.load(cwd + "/resources/images/particles/glitch_1.png").convert_alpha()
        particle_cache['joker_card'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/visible_card.png"), (80, 80))
        particle_cache['hot_sauce'] = pg.image.load(cwd+"/resources/images/ui_icons/hot_sauce.png")
        particle_cache['meat'] = pg.image.load(cwd+"/resources/images/ui_icons/meat.png")
        particle_cache['vegan_crunch'] = pg.image.load(cwd+"/resources/images/ui_icons/vegan_crunch.png")
        particle_cache['cheese'] = pg.image.load(cwd+"/resources/images/ui_icons/cheese.png")
        particle_cache['spike_ball'] = pg.image.load(cwd + "/resources/images/particles/spike_ball.png").convert_alpha()
        particle_cache['sharp_shadow'] = pg.transform.scale(pg.image.load(cwd + "/blobs/random/special_blob.png"), (180, 99)).convert_alpha()
        particle_cache['sharp_shadow'].fill((0, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        particle_cache['icons'] = {}
        particle_cache['merchant_shop'] = pg.image.load(cwd+"/resources/images/ui_icons/merchant_icons.png")
        particle_cache['bubble'] = pg.image.load(cwd + "/resources/images/particles/bubble.png").convert_alpha()
        particle_cache['bubble_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/bubble_particle.png").convert_alpha(), (40, 40))
        particle_cache['f_rank'] = pg.image.load(cwd + "/resources/images/particles/f_rank.png")
        particle_cache['d_rank'] = pg.image.load(cwd + "/resources/images/particles/d_rank.png")
        particle_cache['c_rank'] = pg.image.load(cwd + "/resources/images/particles/c_rank.png")
        particle_cache['b_rank'] = pg.image.load(cwd + "/resources/images/particles/b_rank.png")
        particle_cache['a_rank'] = pg.image.load(cwd + "/resources/images/particles/a_rank.png")
        particle_cache['s_rank'] = pg.image.load(cwd + "/resources/images/particles/s_rank.png")
        particle_cache['x_rank'] = pg.image.load(cwd + "/resources/images/particles/x_rank.png")
        particle_cache['shuriken'] = pg.image.load(cwd + "/resources/images/particles/shuriken.png").convert_alpha()
        particle_cache['shuriken_dmg'] = pg.image.load(cwd + "/resources/images/particles/shuriken_dmg.png").convert_alpha()
        for icon in ability_image_dict:
            try:
                ability_key = species_to_stars(icon, {})['special_ability']
                particle_cache['icons'][ability_key] = pg.transform.scale(pg.image.load(ability_image_dict[icon]), (70, 70))
            except:
                particle_cache['icons'][icon] = pg.transform.scale(pg.image.load(cwd+"/resources/images/ability_icons/404.png"), (70, 70))
    for blob in blobs:
        blob_speed = blob.top_speed
        if(blob.status_effects['glued']):
            blob_speed = 5 + (3 * bool(blob.boost_timer))
        if(blob.status_effects['buttered']):
            blob_speed += 2
        if(blob.status_effects['hypothermia']):
            blob_speed -= 3
        if(blob.status_effects['monado_effect']):
            if(blob.status_effects['monado_effect'] == "JUMP"):
                blob_speed -= 3
            if(blob.status_effects['monado_effect'] == "SPEED"):
                blob_speed += 5
            if(blob.status_effects['monado_effect'] == "SHIELD"):
                blob_speed -= 4
        
        if(abs(blob.x_speed) >= blob_speed and blob.y_pos == blob.ground): #Handles Top Speed Particles while grounded
            particle_memory = draw_top_speed_particles(blob.x_center + 50, particle_memory)
            particle_memory = draw_top_speed_particles(blob.x_center, particle_memory)
            particle_memory = draw_top_speed_particles(blob.x_center - 50, particle_memory)

        #TODO: Add all of these into an array
        if(blob.impact_land_frames == 9): #Landing Particles
            draw_landing_particles(blob)
            draw_landing_particles(blob)
            draw_landing_particles(blob)
            
        
        if(blob.parried):
            particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = (blob.x_center - 65) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, gravity = 0.1, y_speed = -3))
            particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = (blob.x_center - 20) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, gravity = 0.1, y_speed = -3))
            particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = (blob.x_center + 25) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, gravity = 0.1, y_speed = -3))
        
        # TODO: Fix Perfect Parrying so it blocks based on the damage source's speed
        if(blob.perfect_parried):
            # other_blob.x_speed * (500/1366) is added to x speed
            particle_memory.append(dpc.Particle(image = particle_cache['shield_particle'], x_pos = (blob.x_center - 100) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, x_speed =  -1, y_speed = -3, gravity = 0.1))
            particle_memory.append(dpc.Particle(image = particle_cache['shield_particle'], x_pos = (blob.x_center - 40) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, x_speed = 0, y_speed = -3, gravity = 0.1))
            particle_memory.append(dpc.Particle(image = particle_cache['shield_particle'], x_pos = (blob.x_center + 20) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, x_speed = 1, y_speed = -3, gravity = 0.1))

        if(blob.clanked):
            particle_memory.append(dpc.Particle(image = particle_cache['fire_particle'], x_pos = (blob.x_center - 65) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, x_speed = blob.x_speed * (500/1366), y_speed = blob.y_speed * (400/768), gravity = 0.3))
            particle_memory.append(dpc.Particle(image = particle_cache['fire_particle'], x_pos = (blob.x_center - 20) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, x_speed = blob.x_speed * (500/1366), y_speed = blob.y_speed * (400/768), gravity = 0.3))
            particle_memory.append(dpc.Particle(image = particle_cache['fire_particle'], x_pos = (blob.x_center + 25) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, x_speed = blob.x_speed * (500/1366), y_speed = blob.y_speed * (400/768), gravity = 0.3))
        
        if(blob.status_effects['judged'] % 5 == 0 and blob.status_effects['judged'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['judgement'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-10, 10)/10 + blob.x_speed * (500/1366), y_speed = -3, gravity = 0.1, lifetime = 130))
        
        if(blob.status_effects['stunned'] % 5 == 0 and blob.status_effects['stunned'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['stun_particle'], x_pos = (blob.x_center + randint(-45, 5)) * (1000/1366), y_pos = blob.y_center *(382/768) - 30, alpha = 255, fade = 2, x_speed = randint(-5, 5)/10 + blob.x_speed * (500/1366), y_speed = -0.3, lifetime = 130))
        
        if(blob.status_effects['reflecting'] % 5 == 0 and blob.status_effects['reflecting'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['reflection_particle'], x_pos = (blob.x_center + randint(-45, 5)) * (1000/1366), y_pos = blob.y_center *(382/768) - 30, alpha = 255, fade = 2, x_speed = randint(-5, 5)/10 + blob.x_speed * (500/1366), y_speed = -0.3, lifetime = 130))

        if(blob.status_effects['steroided'] % 5 == 0 and blob.status_effects['steroided'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['pill_boost'], x_pos = (blob.x_center + randint(-45, 5)) * (1000/1366), y_pos = blob.y_center *(382/768) - 30, alpha = 255, fade = 2, x_speed = randint(-5, 5)/10 + blob.x_speed * (500/1366), y_speed = -0.3, lifetime = 130))

        if("pill" in blob.used_ability):
            ability_icon = blob.ability_icons['default']
            particle_memory.append(dpc.Particle(image = ability_icon, x_pos = (blob.x_center) * (1000/1366) - 35, y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, gravity = 0.2, y_speed = blob.y_speed * (191/768) - 5))
        
        if(blob.status_effects['taxed'] % 5 == 0 and blob.status_effects['taxed'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['taxation'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-10, 10)/10 + blob.x_speed * (500/1366), y_speed = -3, gravity = 0.1, lifetime = 130))

        if(blob.status_effects['hypothermia'] % 5 == 0 and blob.status_effects['hypothermia'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-5, 5)/5 + blob.x_speed * (100/1366), y_speed = 1, gravity = 0, lifetime = 130))

        if(blob.status_effects['overheat'] % 10 == 0 and blob.status_effects['overheat'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['smoke_particle'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-5, 5)/5 + blob.x_speed * (100/1366), y_speed = -0.1, gravity = -0.03125, lifetime = 130))

        if(blob.status_effects['hyped'] % 10 == 0 and blob.status_effects['hyped'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['thunder_particle'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-5, 5)/5 + blob.x_speed * (100/1366), y_speed = -0.1, gravity = -0.03125, lifetime = 130))

        if(blob.status_effects['nrg_fatigue'] % 10 == 0 and blob.status_effects['nrg_fatigue'] > 0):
            particle_memory.append(dpc.Particle(image = particle_cache['spring_particle'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-5, 5)/5 + blob.x_speed * (100/1366), y_speed = -0.1, gravity = -0.03125, lifetime = 130))

        if(blob.status_effects['cards']['joker_particle']):
            draw_card_selection(*blob.status_effects['cards']['joker_particle'])
            blob.status_effects['cards']['joker_particle'] = None

        if(blob.status_effects['monado_timer'] % 15 == 0 and blob.status_effects['monado_timer'] > 0):
            if(blob.status_effects['monado_effect'] == "SPEED"):
                monado_image = particle_cache['hot_sauce']
            elif(blob.status_effects['monado_effect'] == "SMASH"):
                monado_image = particle_cache['meat']
            elif(blob.status_effects['monado_effect'] == "SHIELD"):
                monado_image = particle_cache['vegan_crunch']
            elif(blob.status_effects['monado_effect'] == "JUMP"):
                monado_image = particle_cache['cheese']

            particle_divider = 100 #if blob.status_effects['monado_effect'] == "JUMP" else 50
            if(blob.status_effects['monado_timer'] >= 100):
                for i in range(blob.status_effects['monado_timer'] // particle_divider):
                    particle_memory.append(dpc.Particle(image = monado_image, x_pos = (blob.x_center + randint(-75, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 60, fade = 1, x_speed = randint(-5, 5)/5 + blob.x_speed * (100/1366), y_speed = -0.1, gravity = -0.03125, lifetime = 130))
            elif(blob.status_effects['monado_timer'] >= 1):
                particle_memory.append(dpc.Particle(image = monado_image, x_pos = (blob.x_center + randint(-75, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 60, fade = 1, x_speed = randint(-5, 5)/5 + blob.x_speed * (100/1366), y_speed = -0.1, gravity = -0.03125, lifetime = 130))
                
        if(blob.status_effects['shop']['purchase_particle']):
            draw_shop_selection((blob.x_pos + 25, blob.y_pos - 180), blob.status_effects['shop']['purchase_particle'])
            blob.status_effects['shop']['purchase_particle'] = None
        
        #if(blob.status_effects['shop']['discard_particle']):
        #    draw_shop_discard((blob.x_pos + 25, blob.y_pos - 180), blob.status_effects['shop']['discard_particle'])
        #    blob.status_effects['shop']['discard_particle'] = None
        create_blob_particles(blob)
        #Manages and updates particles
    particle_memory = blit_and_update_particles(particle_memory, game_display)

def draw_damage_flash(align):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['damage_flash'], alpha = 255, x_pos = align[0], y_pos = align[1], fade = 15, ground_clip = True))

def draw_heal_flash(align):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['heal_flash'], alpha = 255, x_pos = align[0], y_pos = align[1], fade = 15, ground_clip = True))

def draw_recharge_flash(align):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['recharge_flash'], alpha = 255, x_pos = align[0], y_pos = align[1], fade = 15, ground_clip = True))

def draw_block_flash(align):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['block_flash'], alpha = 255, x_pos = align[0], y_pos = align[1], fade = 15, ground_clip = True))

def draw_boost_flash(align):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['boost_flash'], alpha = 255, x_pos = align[0], y_pos = align[1], fade = 15, ground_clip = True))

def draw_energy_flash(align):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['energy_flash'], alpha = 255, x_pos = align[0], y_pos = align[1] + 75, fade = 15, ground_clip = True))

def draw_shatter(align, shatter_timer):
    global particle_memory
    shatter_timer = (68 - shatter_timer)//4
    original = particle_cache['shatter_spritesheet'].get_rect()
    cropx, cropy = ((shatter_timer-1)%5)*70, ((shatter_timer-1)//5) * 70
    cropRect = (cropx, cropy, 70, 70)

    ui_memory.append(dpc.Particle(image = particle_cache['shatter_spritesheet'], alpha = 255, x_pos = align[0], y_pos = align[1], lifetime=1, ground_clip = True, crop=cropRect))

def draw_card_selection(position, icon):
    particle_memory.append(dpc.Particle(image = particle_cache['joker_card'], x_pos = position[0]*(1000/1366), y_pos = position[1]*(382/768), alpha = 255, fade = 1, y_speed = -0.25, lifetime = 300))
    particle_memory.append(dpc.Particle(image = particle_cache['icons'][icon], x_pos = (position[0]+5)*(1000/1366), y_pos = (position[1]+5)*(382/768), alpha = 255, fade = 1, y_speed = -0.25, lifetime = 300))

shop_crop_info = {
        "spring_kick_0": (0,0,60,60),
        "spring_kick_1": (60,0,60,60),
        "spring_kick_2": (120,0,60,60),
        "sprint_master_0": (180,0,60,60),
        "sprint_master_1": (240,0,60,60),
        "sprint_master_2": (300,0,60,60),
        "rainbow_heart_0": (0,60,60,60),
        "rainbow_heart_1": (60,60,60,60),
        "rainbow_heart_2": (120,60,60,60),
        "sharp_shadow_0": (180,60,60,60),
        "sharp_shadow_1": (240,60,60,60),
        "sharp_shadow_2": (300,60,60,60),
    }

def draw_shop_selection(position, icon):
    crop_rect = shop_crop_info[icon]
    particle_memory.append(dpc.Particle(image = particle_cache['merchant_shop'], x_pos = (position[0])*(1000/1366), y_pos = (position[1])*(382/768), alpha = 255, fade = 1, y_speed = -0.25, lifetime = 300, crop = crop_rect))
    createSFXEvent("chime_progress")

def draw_shop_discard(position, icon):
    crop_rect = shop_crop_info[icon]
    left_half = (crop_rect[0], crop_rect[1], 30, 60)
    right_half = (crop_rect[0] + 30, crop_rect[1], 30, 60)
    particle_memory.append(dpc.Particle(image = particle_cache['merchant_shop'], x_pos = (position[0])*(1000/1366), y_pos = (position[1])*(382/768), alpha = 255, fade = 2, x_speed = -1, y_speed = -3, gravity = 0.1, lifetime = 300, crop = left_half))
    particle_memory.append(dpc.Particle(image = particle_cache['merchant_shop'], x_pos = (position[0])*(1000/1366), y_pos = (position[1])*(382/768), alpha = 255, fade = 2, x_speed = 1, y_speed = -3, gravity = 0.1, lifetime = 300, crop = right_half))
    createSFXEvent("crunch")

def clear_particle_memory():
    global particle_memory
    global ball_particle_memory
    global ui_memory
    ball_particle_memory = []
    particle_memory = []
    ui_memory = []



ball_particle_memory = []

def draw_ball_particles(game_display, ball, blobs):
    '''
    Draws appropriate particles on the ball based on abilities used by the blobs.
    '''
    global ball_particle_memory
    for blob in blobs:
        if("fireball" in blob.used_ability):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['fire_particle'], x_pos = ball.x_pos * (1000/1366), y_pos = ball.y_pos * (400/786), alpha = 150, x_speed = 0, y_speed = -1, gravity = 0))
        
        if("snowball" in blob.used_ability):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = ball.x_pos * (1000/1366), y_pos = ball.y_pos * (400/786) + 20, alpha = 150, x_speed = 0, y_speed = 1, gravity = 0))
        
        if("geyser" in blob.used_ability):
            for y in range((1240 - round(ball.y_pos))//40):
                if(y > 7):
                    particle_cache['water_particle'].set_alpha(100)
                else:
                    particle_cache['water_particle'].set_alpha(255)
                game_display.blit(particle_cache['water_particle'], (ball.x_pos * (1000/1366), ((1240 - y*40) + randint(-10, 10)) * (400/768)))
        
    if(ball.status_effects['bubbled'] > 1):
        ball_particle_memory.append(dpc.Particle(image = particle_cache['bubble_particle'], x_pos = ball.x_pos * (1000/1366), y_pos = ball.y_pos * (400/786) + 20, alpha = 150, x_speed = -1 * ball.x_speed + (randint(-9, 9)/3), y_speed = -1 * ball.y_speed, gravity = -0.2))

    ball_particle_memory = blit_and_update_particles(ball_particle_memory, game_display)

def draw_spire_dirt(spire_x):
    for x in range(0, 10):
        earth_particles = [particle_cache['landing_particle'], particle_cache['landing_particle_2'], particle_cache['landing_particle_3']]
        ball_particle_memory.append(dpc.Particle(image = random.choice(earth_particles), x_pos = (spire_x * 1000/1366) + random.randint(0, 100), x_speed = random.randint(-2, 2), y_pos = 675, y_speed = random.randint(-20, -15), gravity = 0.5, alpha = 255, fade = 3, ground_clip=False, lifetime = 255))

def draw_console_sparks(console_pos):
    for x in range(0, 10):
        spark_particles = [particle_cache['thunder_particle'], particle_cache['fire_particle'], particle_cache['spring_particle']]
        ball_particle_memory.append(dpc.Particle(image = random.choice(spark_particles), x_pos = (console_pos[0] * 1000/1366) + random.randint(0, 50), x_speed = random.randint(-2, 2), y_pos = console_pos[1] * (400/768), y_speed = random.randint(-10, -5), gravity = 0.5, alpha = 255, fade = 3, ground_clip=False, lifetime = 255))

def draw_cartridge_sparks(cart_pos, cart_speed):
    for x in range(0, 7):
        spark_particles = [particle_cache['thunder_particle'], particle_cache['fire_particle'], particle_cache['spring_particle']]
        ball_particle_memory.append(dpc.Particle(image = random.choice(spark_particles), x_pos = (cart_pos[0] * 1000/1366) + random.randint(0, 50), x_speed = cart_speed[0] + random.randint(-2, 2), y_pos = cart_pos[1] * (400/768), y_speed = cart_speed[1] + random.randint(-5, 0), gravity = 1, alpha = 255, fade = 3, ground_clip=False, lifetime = 255))

def draw_teleportation_pfx(tele_pos):
    for x in range(0, 7):
        spark_particles = [particle_cache['glitch_particle_1']]
        ball_particle_memory.append(dpc.Particle(image = random.choice(spark_particles), x_pos = (tele_pos[0] * 1000/1366) + random.randint(0, 50), x_speed = random.randint(-2, 2), y_pos = tele_pos[1] * (400/768), y_speed = random.randint(-2, 2), gravity = 0, alpha = 255, fade = 17, ground_clip=True, lifetime = 255))

def draw_monk_upgrade_pfx(monk_pos, level):
    match level:
        case 1:
            pfx_sprite = particle_cache['f_rank']
        case 2:
            pfx_sprite = particle_cache['d_rank']
        case 3:
            pfx_sprite = particle_cache['c_rank']
        case 4:
            pfx_sprite = particle_cache['b_rank']
        case 5:
            pfx_sprite = particle_cache['a_rank']
        case 6:
            pfx_sprite = particle_cache['s_rank']
        case 7:
            pfx_sprite = particle_cache['x_rank']
    particle_memory.append(dpc.Particle(image = pfx_sprite, x_pos = (monk_pos[0] + 20)*(1000/1366), y_pos = (monk_pos[1] - 20)*(382/768), alpha = 255, fade = 1, y_speed = -0.25, lifetime = 300))

ball_overlay_memory = []
def draw_ball_overlay(game_display, ball, blobs):
    global ball_overlay_memory
    if not overlay_cache['initialized']:
        particle_cache['thunder_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/thunder_particle.png").convert_alpha(), (40, 40))
        overlay_cache['initialized'] = True
    

    if 'zapped' in ball.status_effects:
        loop = ball.status_effects['zapped']
        if ball.status_effects['zapped'] > 10:
            loop = 10
        alpha = 100
        for x in range(loop):
            particle_cache['thunder_particle'].set_alpha(alpha)
            blitRotateCenter(game_display, particle_cache['thunder_particle'], (ball.previous_locations[-1][0] * (1000/1366) + randint(-10, 10), ball.previous_locations[-1][1] * (400/768) + randint(-10, 10)), (60 * randint(0, 5)))
            alpha += 10
    
    for blob in blobs:
        if("stoplight" in blob.used_ability):
            ball_overlay_memory.append(dpc.Particle(image = particle_cache['stoplight'], x_pos = (ball.x_center * 1000/1366) - 35, y_pos = ball.y_pos * (400/786), alpha = 255, fade = 8.5))

        if("hook" in blob.used_ability):
            #print("hooka")
            blob_x = (blob.x_center) * (1000/1366)
            blob_y = (blob.y_center - 200) * (382/768)
            ball_x = ball.x_center * (1000/1366)
            ball_y = ball.y_center * (400/768)
            if(blob.ability_holding_timer < blob.special_ability_delay):
                ball_x = (ball_x - blob_x) * (blob.ability_holding_timer/blob.special_ability_delay) + blob_x
                ball_y = (ball_y - blob_y) * (blob.ability_holding_timer/blob.special_ability_delay) + blob_y
            pg.draw.line(game_display, (0, 0, 0), (blob_x, blob_y), (ball_x, ball_y), width = 2)
            pg.draw.rect(game_display, (150, 75, 0), (blob_x - 5, blob_y, 10, 90))

    ball_overlay_memory = blit_and_update_particles(ball_overlay_memory, game_display)

def draw_ui_particles(game_display):
    global ui_memory
    ui_memory = blit_and_update_particles(ui_memory, game_display)