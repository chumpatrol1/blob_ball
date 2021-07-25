from os import getcwd
from resources.background_handler import draw_background as draw_background
from math import ceil
import pygame as pg
from random import randint
cwd = getcwd()

particle_cache = {"initialized": False}
def draw_ball_particles(screen_size, game_display, ball, p1_blob, p2_blob):
    if not particle_cache['initialized']:
        particle_cache['initialized'] = True
        particle_cache['fire_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\fire_particle.png").convert_alpha(), (round(screen_size[0]*(40/1366)), round(screen_size[0]*(40/1366))))
        particle_cache['ice_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\ice_particle.png").convert_alpha(), (round(screen_size[0]*(40/1366)), round(screen_size[0]*(40/1366))))
        particle_cache['water_particle'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\water_particle.png").convert_alpha(), (round(screen_size[0]*(40/1366)), round(screen_size[0]*(40/1366))))
        particle_cache['rock_glyph'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\rock_glyph.png").convert_alpha(), (round(screen_size[0]*(200/1366)), round(screen_size[1]*(100/768))))
        particle_cache['rock_spire'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\particles\\rock_spire.png").convert_alpha(), (round(screen_size[0]*(200/1366)), round(screen_size[1]*(100/768))))
        

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
    
    if(p1_blob.used_ability == "spire" or p2_blob.used_ability == "spire"):
        if(p1_blob.special_ability_timer > p1_blob.special_ability_cooldown - 60):
            game_display.blit(particle_cache['rock_glyph'], ((screen_size[0]/1366)* ball.x_pos * (900/1366), (700* screen_size[1]/768)))
        if(p2_blob.special_ability_timer > p2_blob.special_ability_cooldown - 60):
            game_display.blit(particle_cache['rock_glyph'], ((screen_size[0]/1366)* ball.x_pos * (900/1366), (700* screen_size[1]/768)))
        if(p1_blob.special_ability_timer > p1_blob.special_ability_cooldown - 60):
            game_display.blit(particle_cache['rock_spire'], ((screen_size[0]/1366)* ball.x_pos * (900/1366), (500* screen_size[1]/768)))
    