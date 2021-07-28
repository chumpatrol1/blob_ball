from os import getcwd
from resources.background_handler import draw_background as draw_background
from resources.display_particles import draw_ball_particles as draw_ball_particles
from math import ceil
import pygame as pg
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

