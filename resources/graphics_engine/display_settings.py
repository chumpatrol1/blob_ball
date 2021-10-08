from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import draw_ball_particles as draw_ball_particles
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
    text_color = (0, 0, 255)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_array = [
        menu_font.render("HD Backgrounds: " + str(settings['hd_backgrounds']), False, text_color),
        menu_font.render("HD Blobs: " + str(settings['hd_blobs']), False, text_color),
        menu_font.render("Smooth Scaling: " + str(settings['smooth_scaling']), False, text_color),
        menu_font.render("Music Volume: " + str(settings['music_volume']), False, text_color),
        menu_font.render("Sound Volume: " + str(settings['sound_volume']), False, text_color),
        menu_font.render("Remap Inputs", False, text_color),
        menu_font.render("Default Controls", False, text_color),
        menu_font.render("Reset to Default", False, text_color),
        menu_font.render("<-- Back", False, text_color),
    ]
    text_y = 768//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    game_display.blit(ball, (68, (76 * selector_position) + (0.5 * 76)))

def draw_rebind_screen(game_display, settings, rebind_key):
    text_color = (0, 0, 255)
    draw_background(game_display, "rebind", settings)
    
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    menu_text = menu_font.render('REBIND ' + rebind_key, False, text_color)
    text_rect = menu_text.get_rect()
    text_rect.center = (300, 100)

    game_display.blit(menu_text, text_rect)
    
def draw_rules_screen(screen_size, game_display, ruleset, selector_position, settings):
    draw_background(game_display, "rules", settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", round(30*(screen_size[1]/768)))
    text_color = (0, 0, 255)
    text_array = [
        menu_font.render("Goal Limit: " + str(ruleset['goal_limit']), False, text_color),
        menu_font.render("Time Limit: " + str(ruleset['time_limit']), False, text_color),
        menu_font.render("Time Bonus: " + str(ruleset['time_bonus']), False, text_color),
        menu_font.render("NRG Charge Rate: " + str(ruleset['special_ability_charge_base']), False, text_color),
        menu_font.render("Danger Zone Enabled: " + str(ruleset['danger_zone_enabled']), False, text_color),
        menu_font.render("Reset to Default", False, text_color),
        menu_font.render("<-- Back", False, text_color),
    ]
    text_y = screen_size[1]//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (screen_size[0]//20, text_y)
        game_display.blit(text_box, text_rect)
        text_y += screen_size[1]//10

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (screen_size[1]//20, screen_size[1]//20))
    game_display.blit(ball, (screen_size[0]*(1/20), ((screen_size[1]//10) * selector_position) + (0.5 * screen_size[1]//10)))
