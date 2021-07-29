from os import getcwd
from resources.background_handler import draw_background as draw_background
from resources.display_particles import draw_ball_particles as draw_ball_particles
from math import ceil
import pygame as pg
from engine.handle_input import bind_input as bind_input
from engine.handle_input import unbind_inputs as unbind_inputs
cwd = getcwd()

image_cache = {"initialized": False}


def draw_settings_screen(game_display, settings, selector_position):
    #TODO: Simplify and remove
    draw_background(game_display, "settings", settings)
    global cwd
    global image_cache
    if not image_cache['initialized']: #Load in the images so we don't keep importing them
        image_cache['initialized'] = True
    
    menu_font = pg.font.SysFont('Arial', 30)
    text_array = [
        menu_font.render("Remap Inputs", False, (255, 124, 0)),
        menu_font.render("HD Backgrounds: " + str(settings['hd_backgrounds']), False, (255, 124, 0)),
        menu_font.render("HD Blobs: " + str(settings['hd_blobs']), False, (255, 124, 0)),
        menu_font.render("Default Controls", False, (255, 124, 0)),
        menu_font.render("Reset to Default", False, (255, 124, 0)),
        menu_font.render("<-- Back", False, (255, 124, 0)),
    ]
    text_y = 768//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

    ball = pg.image.load(cwd + "\\resources\\images\\soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    game_display.blit(ball, (68, (76 * selector_position) + (0.5 * 76)))

rebind_array = ['p1_up', 'p1_down', 'p1_left', 'p1_right', 'p1_ability', 'p1_kick', 'p1_block', 'p1_boost',
'p2_up', 'p2_down', 'p2_left', 'p2_right', 'p2_ability', 'p2_kick', 'p2_block', 'p2_boost',
    ]

rebind_number = -1
def draw_rebind_screen(game_display, settings):
    game_state = "rebind"
    draw_background(game_display, "rebind", settings)
    global rebind_number
    if(rebind_number == -1):
        unbind_inputs()
        rebind_number = 0
    menu_font = pg.font.SysFont('Arial', 30)
    menu_text = menu_font.render('REBIND ' + rebind_array[rebind_number], False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (300, 100)
    if(bind_input(rebind_array[rebind_number])):
        rebind_number += 1
        if(rebind_number == 16):
            game_state = "settings"
            rebind_number = -1

    game_display.blit(menu_text, text_rect)
    return [game_state]
    