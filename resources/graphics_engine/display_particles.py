from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from math import ceil
import pygame as pg
import random
from random import randint
import resources.graphics_engine.dynamic_particle_handler as dpc
cwd = getcwd()

def blit_and_update_particles(memory, game_display):
    temparray = []
    for particle in memory:
        particle.image.set_alpha(particle.alpha)
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

def create_blob_particles(blob, other_blob):
    global particle_memory
    def draw_gale(blob, other_blob):
        random_number = randint(0,2)
        if(random_number):
            if(blob.player == 1):
                particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = randint(-100, 1466), y_pos = randint(100, 600), alpha = 15 * randint(10, 17), fade = 1, x_speed = 3))
            elif(blob.player == 2):
                particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = randint(-100, 1466), y_pos = randint(100, 600), alpha = 15 * randint(10, 17), fade = 1, x_speed = -3))
    
    def draw_starpunch_wait(blob, other_blob): #Bad location
        particle_memory.append(dpc.Particle(image = particle_cache['star_glove'], x_pos = blob.x_center * (1000/1366) - 20, y_pos = blob.y_center * (382/768), alpha = 255, lifetime = 1))
    
    def draw_starpunch(blob, other_blob):
        punch_x = other_blob.x_center
        punch_y = other_blob.y_center
        if(other_blob.x_center > blob.x_center + 255):
            punch_x = blob.x_center + 255
        elif(blob.x_center - 315 > other_blob.x_center):
            punch_x = blob.x_center - 315

        if(blob.y_center + 330 < other_blob.y_center):
            punch_y = blob.y_center + 330
        elif(blob.y_center - 300 > other_blob.y_center):
            punch_y = blob.y_center - 300

        x_midpoint = (punch_x + blob.x_center)/2
        y_midpoint = (punch_y + blob.y_center)/2

        particle_memory.append(dpc.Particle(image = particle_cache['spring_particle'], x_pos = blob.x_center * (1000/1366), y_pos = blob.y_center * 382/768, alpha = 255, lifetime = 60, fade = 10))
        particle_memory.append(dpc.Particle(image = particle_cache['spring_particle'], x_pos = ((blob.x_center + x_midpoint)/2) * (1000/1366), y_pos = (blob.y_center + y_midpoint)/2 * 382/768, alpha = 255, lifetime = 60, fade = 10))
        particle_memory.append(dpc.Particle(image = particle_cache['spring_particle'], x_pos = x_midpoint * (1000/1366), y_pos = y_midpoint * 382/768, alpha = 255, lifetime = 60, fade = 10))
        particle_memory.append(dpc.Particle(image = particle_cache['spring_particle'], x_pos = (punch_x + x_midpoint)/2 * (1000/1366), y_pos = (punch_y + y_midpoint)/2 * 382/768, alpha = 255, lifetime = 60, fade = 10))
        particle_memory.append(dpc.Particle(image = particle_cache['star_glove'], x_pos = punch_x * (1000/1366), y_pos = punch_y * 382/768, alpha = 255, lifetime = 60, fade = 10))
        
    used_ability_dict = {
        'gale': draw_gale,
        'starpunch_wait': draw_starpunch_wait,
        'starpunch': draw_starpunch,
    }

    if blob.used_ability in used_ability_dict:
        used_ability_dict[blob.used_ability](blob, other_blob)


def draw_blob_particles(game_display, ball, blob, other_blob):
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
    global particle_memory
    if not particle_cache['initialized']:
        particle_cache['initialized'] = True
        particle_cache['fire_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/fire_particle.png").convert_alpha(), (40, 40))
        particle_cache['ice_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/ice_particle.png").convert_alpha(), (40, 40))
        particle_cache['water_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/water_particle.png").convert_alpha(), (40, 40))
        particle_cache['rock_glyph'] = pg.image.load(cwd + "/resources/images/particles/rock_glyph.png").convert_alpha()
        particle_cache['rock_spire'] = pg.image.load(cwd + "/resources/images/particles/rock_spire.png").convert_alpha()
        particle_cache['thunder_glyph'] = pg.image.load(cwd + "/resources/images/particles/thunder_glyph.png").convert_alpha()
        particle_cache['thunder_bolt'] = pg.image.load(cwd + "/resources/images/particles/thunder_bolt.png").convert_alpha()
        particle_cache['thunder_bolt_2'] = pg.image.load(cwd + "/resources/images/particles/thunder_bolt_2.png").convert_alpha()
        particle_cache['earth_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle.png").convert_alpha(), (20, 20))
        particle_cache['earth_particle_2'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle_2.png").convert_alpha(), (20, 20))
        particle_cache['earth_particle_3'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/earth_particle_3.png").convert_alpha(), (20, 20))
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
        particle_cache['shatter_spritesheet'] = pg.image.load(cwd + "/resources/images/particles/shatter_spritesheet.png").convert_alpha()
        particle_cache['judgement'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/rules_icon.png").convert_alpha(), (30, 30))
        particle_cache['taxation'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ability_icons/tax.png").convert_alpha(), (30, 30))
    if(abs(blob.x_speed) >= blob.top_speed and blob.y_pos == blob.ground): #Handles Top Speed Particles while grounded
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

    if(blob.used_ability == "pill"):
        ability_icon = pg.image.load(blob.ability_icon)
        particle_memory.append(dpc.Particle(image = ability_icon, x_pos = (blob.x_center) * (1000/1366) - 35, y_pos = blob.y_center *(382/768), alpha = 255, fade = 5, gravity = 0.2, y_speed = blob.y_speed * (191/768) - 5))

    if(blob.status_effects['taxed'] % 5 == 0 and blob.status_effects['taxed'] > 0):
        particle_memory.append(dpc.Particle(image = particle_cache['taxation'], x_pos = (blob.x_center + randint(-65, 25)) * (1000/1366), y_pos = blob.y_center *(382/768), alpha = 255, fade = 2, x_speed = randint(-10, 10)/10 + blob.x_speed * (500/1366), y_speed = -3, gravity = 0.1, lifetime = 130))

    create_blob_particles(blob, other_blob)
    #Manages and updates particles
    particle_memory = blit_and_update_particles(particle_memory, game_display)

def draw_damage_flash(flash_x):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['damage_flash'], alpha = 255, x_pos = flash_x, y_pos = 0, fade = 15, ground_clip = True))

def draw_heal_flash(flash_x):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['heal_flash'], alpha = 255, x_pos = flash_x, y_pos = 0, fade = 15, ground_clip = True))

def draw_recharge_flash(flash_x):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['recharge_flash'], alpha = 255, x_pos = flash_x, y_pos = 0, fade = 15, ground_clip = True))

def draw_block_flash(flash_x):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['block_flash'], alpha = 255, x_pos = flash_x, y_pos = 0, fade = 15, ground_clip = True))

def draw_boost_flash(flash_x):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['boost_flash'], alpha = 255, x_pos = flash_x, y_pos = 0, fade = 15, ground_clip = True))


def draw_energy_flash(flash_x):
    global particle_memory
    ui_memory.append(dpc.Particle(image = particle_cache['energy_flash'], alpha = 255, x_pos = flash_x, y_pos = 75, fade = 15, ground_clip = True))

def draw_shatter(flash_x, shatter_timer):
    global particle_memory
    shatter_timer = (68 - shatter_timer)//4
    original = particle_cache['shatter_spritesheet'].get_rect()
    cropx, cropy = ((shatter_timer-1)%5)*70, ((shatter_timer-1)//5) * 70
    cropRect = (cropx, cropy, 70, 70)

    ui_memory.append(dpc.Particle(image = particle_cache['shatter_spritesheet'], alpha = 255, x_pos = flash_x, y_pos = 0, lifetime=1, ground_clip = True, crop=cropRect))

def clear_particle_memory():
    global particle_memory
    global ball_particle_memory
    global ui_memory
    ball_particle_memory = []
    particle_memory = []
    ui_memory = []



ball_particle_memory = []

def draw_ball_particles(game_display, ball, p1_blob, p2_blob):
    global ball_particle_memory
    if(p1_blob.used_ability == "fireball" or p2_blob.used_ability == "fireball"):
        ball_particle_memory.append(dpc.Particle(image = particle_cache['fire_particle'], x_pos = ball.x_pos * (1000/1366), y_pos = ball.y_pos * (400/786), alpha = 150, x_speed = 0, y_speed = -1, gravity = 0))
    
    if(p1_blob.used_ability == "snowball" or p2_blob.used_ability == "snowball"):
        ball_particle_memory.append(dpc.Particle(image = particle_cache['ice_particle'], x_pos = ball.x_pos * (1000/1366), y_pos = ball.y_pos * (400/786) + 20, alpha = 150, x_speed = 0, y_speed = 1, gravity = 0))
    
    if(p1_blob.used_ability == "geyser" or p2_blob.used_ability == "geyser"):
        for y in range((1240 - round(ball.y_pos))//40):
            if(y > 7):
                particle_cache['water_particle'].set_alpha(100)
            else:
                particle_cache['water_particle'].set_alpha(255)
            game_display.blit(particle_cache['water_particle'], (ball.x_pos * (1000/1366), ((1240 - y*40) + randint(-10, 10)) * (400/768)))
    
    if(p1_blob.species == "rock"):
        if(p1_blob.used_ability == "spire_wait"):
            #print(100 * log10(255 * ((p1_blob.special_ability_cooldown_max - p1_blob.special_ability_timer)/(p1_blob.special_ability_delay))))
            ball_particle_memory.append(dpc.Particle(image = particle_cache['rock_glyph'], x_pos = ball.x_center * (1000/1366) - 50, y_pos = 700, alpha = 255 * ((p1_blob.special_ability_cooldown_max - p1_blob.special_ability_timer)/(p1_blob.special_ability_delay)), fade = 0, lifetime = 1))
            #ball_particle_memory.append(dpc.Particle(image = particle_cache['rock_glyph'], x_pos = ball.x_center * (1000/1366) - 50, y_pos = 700, alpha = 100 * log10(255 * ((p1_blob.special_ability_cooldown_max - p1_blob.special_ability_timer)/(p1_blob.special_ability_delay))), fade = 0, lifetime = 1))
        
        elif(p1_blob.special_ability_timer == p1_blob.special_ability_cooldown_max - p1_blob.special_ability_delay):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['rock_spire'], x_pos = (ball.x_center * 1000/1366) - 50, y_pos = 500, alpha = 255, fade = 7.25, ground_clip=True))
            for x in range(0, 10):
                earth_particles = [particle_cache['landing_particle'], particle_cache['landing_particle_2'], particle_cache['landing_particle_3']]
                ball_particle_memory.append(dpc.Particle(image = random.choice(earth_particles), x_pos = (ball.x_center * 1000/1366) + random.randint(-50, 50), x_speed = random.randint(-2, 2), y_pos = 675, y_speed = random.randint(-20, -15), gravity = 0.5, alpha = 255, fade = 3, ground_clip=False, lifetime = 255))
        

    if(p2_blob.species == "rock"):
        if(p2_blob.used_ability == "spire_wait"):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['rock_glyph'], x_pos = ball.x_center * (1000/1366) - 50, y_pos = 700, alpha = 255 * ((p2_blob.special_ability_cooldown_max - p2_blob.special_ability_timer)/(p2_blob.special_ability_delay)), fade = 0, lifetime = 1))
            
        
        elif(p2_blob.special_ability_timer == p2_blob.special_ability_cooldown_max - p2_blob.special_ability_delay):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['rock_spire'], x_pos = (ball.x_center * 1000/1366) - 50, y_pos = 500, alpha = 255, fade = 7.25, ground_clip=True))
            for x in range(0, 10):
                earth_particles = [particle_cache['landing_particle'], particle_cache['landing_particle_2'], particle_cache['landing_particle_3']]
                ball_particle_memory.append(dpc.Particle(image = random.choice(earth_particles), x_pos = (ball.x_center * 1000/1366) + random.randint(-50, 50), x_speed = random.randint(-2, 2), y_pos = 675, y_speed = random.randint(-20, -15), gravity = 0.5, alpha = 255, fade = 3, ground_clip=False, lifetime = 255))
        
    if(p1_blob.species == "lightning"):
        if(p1_blob.used_ability == "thunderbolt_wait"):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['thunder_glyph'], x_pos = ball.x_center * (1000/1366) - 50, y_pos = 700, alpha = 255 * ((p1_blob.special_ability_cooldown_max - p1_blob.special_ability_timer)/(p1_blob.special_ability_delay)), fade = 0, lifetime = 1))
        
        elif(p1_blob.special_ability_timer == p1_blob.special_ability_cooldown_max - p1_blob.special_ability_delay):
            
            bolt = (1, 2)
            boltch = random.choice(bolt)

            if boltch == 1:
                ball_particle_memory.append(dpc.Particle(image = particle_cache['thunder_bolt'], x_pos = (ball.x_center * 1000/1366) - 50, y_pos = 112, alpha = 255, fade = 7.25))
            elif boltch == 2:
                ball_particle_memory.append(dpc.Particle(image = particle_cache['thunder_bolt_2'], x_pos = (ball.x_center * 1000/1366) - 50, y_pos = 112, alpha = 255, fade = 7.25))

    if(p2_blob.species == "lightning"):
        if(p2_blob.used_ability == "thunderbolt_wait"):
            ball_particle_memory.append(dpc.Particle(image = particle_cache['thunder_glyph'], x_pos = ball.x_center * (1000/1366) - 50, y_pos = 700, alpha = 255 * ((p2_blob.special_ability_cooldown_max - p2_blob.special_ability_timer)/(p2_blob.special_ability_delay)), fade = 0, lifetime = 1))
        
        elif(p2_blob.special_ability_timer == p2_blob.special_ability_cooldown_max - p2_blob.special_ability_delay):
            
            bolt = (1, 2)
            boltch = random.choice(bolt)

            if boltch == 1:
                ball_particle_memory.append(dpc.Particle(image = particle_cache['thunder_bolt'], x_pos = (ball.x_center * 1000/1366) - 50, y_pos = 112, alpha = 255, fade = 7.25))
            elif boltch == 2:
                ball_particle_memory.append(dpc.Particle(image = particle_cache['thunder_bolt_2'], x_pos = (ball.x_center * 1000/1366) - 50, y_pos = 112, alpha = 255, fade = 7.25))

    ball_particle_memory = blit_and_update_particles(ball_particle_memory, game_display)

ball_overlay_memory = []
def draw_ball_overlay(game_display, ball, p1_blob, p2_blob):
    global ball_overlay_memory
    if not overlay_cache['initialized']:
        particle_cache['thunder_particle'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/particles/thunder_particle.png").convert_alpha(), (40, 40))
        overlay_cache['initialized'] = True
    
    for previous_location in ball.previous_locations:
        alpha = 100
        if(previous_location[4] == "thunderbolt" or previous_location[5] == "thunderbolt"):
            particle_cache['thunder_particle'].set_alpha(alpha)
            blitRotateCenter(game_display, particle_cache['thunder_particle'], (ball.previous_locations[-1][0] * (1000/1366) + randint(-10, 10), ball.previous_locations[-1][1] * (400/768) + randint(-10, 10)), (60 * randint(0, 5)))
            alpha += 10
    
    if(p1_blob.used_ability == "stoplight_pfx" or p2_blob.used_ability == "stoplight_pfx"):
        ball_overlay_memory.append(dpc.Particle(image = particle_cache['stoplight'], x_pos = (ball.x_center * 1000/1366) - 35, y_pos = ball.y_pos * (400/786), alpha = 255, fade = 8.5))

    if(p1_blob.used_ability == "hook"):
        #print("hooka")
        blob_x = (p1_blob.x_center) * (1000/1366)
        blob_y = (p1_blob.y_center - 200) * (382/768)
        ball_x = ball.x_center * (1000/1366)
        ball_y = ball.y_center * (400/768)
        if(p1_blob.holding_timer < p1_blob.special_ability_delay):
            ball_x = (ball_x - blob_x) * (p1_blob.holding_timer/p1_blob.special_ability_delay) + blob_x
            ball_y = (ball_y - blob_y) * (p1_blob.holding_timer/p1_blob.special_ability_delay) + blob_y
        pg.draw.line(game_display, (0, 0, 0), (blob_x, blob_y), (ball_x, ball_y), width = 2)
        pg.draw.rect(game_display, (150, 75, 0), (blob_x - 5, blob_y, 10, 90))

    if(p2_blob.used_ability == "hook"):
        #print("snooka")
        blob_x = (p2_blob.x_center) * (1000/1366)
        blob_y = (p2_blob.y_center - 200) * (382/768)
        ball_x = ball.x_center * (1000/1366)
        ball_y = ball.y_center * (400/768)
        if(p2_blob.holding_timer < p2_blob.special_ability_delay):
            ball_x = (ball_x - blob_x) * (p2_blob.holding_timer/p2_blob.special_ability_delay) + blob_x
            ball_y = (ball_y - blob_y) * (p2_blob.holding_timer/p2_blob.special_ability_delay) + blob_y
        pg.draw.line(game_display, (0, 0, 0), (blob_x, blob_y), (ball_x, ball_y), width = 2)
        pg.draw.rect(game_display, (150, 75, 0), (blob_x - 5, blob_y, 10, 90))

    ball_overlay_memory = blit_and_update_particles(ball_overlay_memory, game_display)

def draw_ui_particles(game_display):
    global ui_memory
    ui_memory = blit_and_update_particles(ui_memory, game_display)