from os import getcwd
from resources.background_handler import draw_background as draw_background
from math import ceil
import pygame as pg
from random import randint
import resources.dynamic_particle_handler as dpc
cwd = getcwd()

def blitRotateCenter(game_display, image, topleft, angle):

    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    game_display.blit(rotated_image, new_rect)

particle_cache = {"initialized": False}
overlay_cache = {'initialized': False}
particle_memory = [] 

def draw_blob_particles(game_display, ball, blob):
    global particle_memory
    if not particle_cache['initialized']:
        particle_cache['initialized'] = True
        particle_cache['fire_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\fire_particle.png").convert_alpha(), (40, 40))
        particle_cache['ice_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\ice_particle.png").convert_alpha(), (40, 40))
        particle_cache['water_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\water_particle.png").convert_alpha(), (40, 40))
        particle_cache['rock_glyph'] = pg.image.load(cwd + "\\resources\\images\\particles\\rock_glyph.png").convert_alpha()
        particle_cache['rock_spire'] = pg.image.load(cwd + "\\resources\\images\\particles\\rock_spire.png").convert_alpha()
        particle_cache['thunder_glyph'] = pg.image.load(cwd + "\\resources\\images\\particles\\thunder_glyph.png").convert_alpha()
        particle_cache['thunder_bolt'] = pg.image.load(cwd + "\\resources\\images\\particles\\thunder_bolt.png").convert_alpha()
        particle_cache['earth_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\earth_particle.png").convert_alpha(), (20, 20))
        particle_cache['landing_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\ice_particle.png").convert_alpha(), (30, 30))
    
    if(abs(blob.x_speed) >= blob.top_speed and blob.y_pos == blob.ground): #Handles Top Speed Particles while grounded
        if(randint(0, 2) == 2):
            particle_memory.append(dpc.Particle(image = particle_cache['earth_particle'], x_pos = (blob.x_center + 50) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 2), y_speed = randint(-3, -1), gravity = 0.1))
        if(randint(0, 2) == 2):
            particle_memory.append(dpc.Particle(image = particle_cache['earth_particle'], x_pos = blob.x_center * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 2), y_speed = randint(-3, -1), gravity = 0.1))
        if(randint(0, 2) == 2):
            particle_memory.append(dpc.Particle(image = particle_cache['earth_particle'], x_pos = (blob.x_center - 50) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 2), y_speed = randint(-3, -1), gravity = 0.1))

    if(blob.impact_land_frames == 9):
        particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center + 50) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(1, 3), y_speed = randint(-4, -2), gravity = 0.1))
        particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center + 25) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(0, 2), y_speed = randint(-4, -2), gravity = 0.1))
        particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-1, 1), y_speed = randint(-4, -2), gravity = 0.1))
        particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center - 25) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-2, 0), y_speed = randint(-4, -2), gravity = 0.1))
        particle_memory.append(dpc.Particle(image = particle_cache['landing_particle'], x_pos = (blob.x_center - 50) * (1000/1366), y_pos = blob.y_center * (400/768), alpha = 15 * randint(10, 17), x_speed = 0.5 * randint(-3, -1), y_speed = randint(-4, -2), gravity = 0.1))

    #Manages and updates particles
    temparray = []
    for particle in particle_memory:
        particle.image.set_alpha(particle.alpha)
        game_display.blit(particle.image, (particle.x_pos, particle.y_pos))
        particle.update()
        if not (particle.alpha <= 0):
           temparray.append(particle)

    particle_memory = temparray 

def draw_ball_particles(screen_size, game_display, ball, p1_blob, p2_blob):

    for previous_location in ball.previous_locations:
        alpha = 150
        if(previous_location[4] == "fireball" or previous_location[5] == "fireball"):
            particle_cache['fire_particle'].set_alpha(alpha)
            game_display.blit(particle_cache['fire_particle'], ((screen_size[0]/1366)*previous_location[0] * (1000/1366), (screen_size[1]/768) * previous_location[1] * (400/768)))
            alpha += 10
        alpha = 150
        if(previous_location[4] == "snowball" or previous_location[5] == "snowball"):
            particle_cache['ice_particle'].set_alpha(alpha)
            game_display.blit(particle_cache['ice_particle'], ((screen_size[0]/1366)*previous_location[0] * (1000/1366), (screen_size[1]/768) * previous_location[1] * (400/768)))
            alpha += 10
    
    if(p1_blob.used_ability == "geyser" or p2_blob.used_ability == "geyser"):
        for y in range((1240 - round(ball.y_pos))//40):
            if(y > 7):
                particle_cache['water_particle'].set_alpha(100)
            else:
                particle_cache['water_particle'].set_alpha(255)
            game_display.blit(particle_cache['water_particle'], ((screen_size[0]/1366)* ball.x_pos * (1000/1366), (screen_size[1]/768) * ((1240 - y*40) + randint(-10, 10)) * (400/768)))
    
    if(p1_blob.used_ability == "spire"):
        if(p1_blob.special_ability_timer > p1_blob.special_ability_cooldown - 60):
            game_display.blit(particle_cache['rock_glyph'], (ball.x_center * (1000/1366) - 50, 700))
        elif(p1_blob.special_ability_cooldown - 95 <= p1_blob.special_ability_timer <= p1_blob.special_ability_cooldown - 60):
            if(p1_blob.special_ability_timer == p1_blob.special_ability_cooldown - 60):
                particle_cache['p1_spire_x'] = (ball.x_center * 1000/1366) - 50
            alpha = 255 - 7 * ((p1_blob.special_ability_cooldown - 60) - p1_blob.special_ability_timer)
            particle_cache['rock_spire'].set_alpha(alpha)
            game_display.blit(particle_cache['rock_spire'], (particle_cache['p1_spire_x'], 500))

    if(p2_blob.used_ability == "spire"):
        if(p2_blob.special_ability_timer > p2_blob.special_ability_cooldown - 60):
            game_display.blit(particle_cache['rock_glyph'], (ball.x_center * (1000/1366) - 50, 700))
        elif(p2_blob.special_ability_cooldown - 95 <= p2_blob.special_ability_timer <= p2_blob.special_ability_cooldown - 60):
            if(p2_blob.special_ability_timer == p2_blob.special_ability_cooldown - 60):
                particle_cache['p2_spire_x'] = (ball.x_center * 1000/1366) - 50
            alpha = 255 - 7 * ((p2_blob.special_ability_cooldown - 60) - p2_blob.special_ability_timer)
            particle_cache['rock_spire'].set_alpha(alpha)
            game_display.blit(particle_cache['rock_spire'], (particle_cache['p2_spire_x'], 500))
        
    if(p1_blob.species == "lightning"):
        if(p1_blob.special_ability_timer > p1_blob.special_ability_cooldown - 30):
            game_display.blit(particle_cache['thunder_glyph'], (ball.x_center * (1000/1366) - 50, 700))
        elif(p1_blob.special_ability_cooldown - 95 <= p1_blob.special_ability_timer <= p1_blob.special_ability_cooldown - 30):
            if(p1_blob.special_ability_timer == p1_blob.special_ability_cooldown - 30):
                particle_cache['p1_spire_x'] = (ball.x_center * 1000/1366) - 50
            alpha = 255 - 7 * ((p1_blob.special_ability_cooldown - 30) - p1_blob.special_ability_timer)
            particle_cache['thunder_bolt'].set_alpha(alpha)
            game_display.blit(particle_cache['thunder_bolt'], (particle_cache['p1_spire_x'], 125))

    if(p2_blob.species == "lightning"):
        if(p2_blob.special_ability_timer > p2_blob.special_ability_cooldown - 30):
            game_display.blit(particle_cache['thunder_glyph'], (ball.x_center * (1000/1366) - 50, 700))
        elif(p2_blob.special_ability_cooldown - 95 <= p2_blob.special_ability_timer <= p2_blob.special_ability_cooldown - 30):
            if(p2_blob.special_ability_timer == p2_blob.special_ability_cooldown - 30):
                particle_cache['p2_spire_x'] = (ball.x_center * 1000/1366) - 50
            alpha = 255 - 7 * ((p2_blob.special_ability_cooldown - 30) - p2_blob.special_ability_timer)
            particle_cache['thunder_bolt'].set_alpha(alpha)
            game_display.blit(particle_cache['thunder_bolt'], (particle_cache['p2_spire_x'], 125))

def draw_ball_overlay(screen_size, game_display, ball, p1_blob, p2_blob):
    if not overlay_cache['initialized']:
        particle_cache['thunder_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\thunder_particle.png").convert_alpha(), (40, 40))
        overlay_cache['initialized'] = True
    
    for previous_location in ball.previous_locations:
        alpha = 100
        if(previous_location[4] == "thunderbolt" or previous_location[5] == "thunderbolt"):
            particle_cache['thunder_particle'].set_alpha(alpha)
            blitRotateCenter(game_display, particle_cache['thunder_particle'], (ball.previous_locations[-1][0] * (1000/1366) + randint(-10, 10), ball.previous_locations[-1][1] * (400/768) + randint(-10, 10)), (60 * randint(0, 5)))
            alpha += 10