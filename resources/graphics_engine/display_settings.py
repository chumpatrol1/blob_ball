from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import draw_ball_particles as draw_ball_particles
from engine.handle_input import return_mapkey_names
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
    game_display.blit(ball, (10, 76 * (selector_position + 1)))

def draw_rebind_screen(game_display, settings, rebind_key):
    text_color = (0, 0, 255)
    draw_background(game_display, "rebind", settings)
    
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    menu_text = menu_font.render('REBINDING: ' + rebind_key, False, text_color)
    text_rect = menu_text.get_rect()
    text_rect.center = (450, 100)

    game_display.blit(menu_text, text_rect)

    input_keys = return_mapkey_names()
    text_array = []
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
    for key in input_keys:
        text_array.append(menu_font.render(key + ": " + str(input_keys[key]), False, text_color))

    text_y = 152
    for text_box in text_array[:len(text_array)//2]:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76
    text_y = 152
    for text_box in text_array[len(text_array)//2:]:
        text_rect = text_box.get_rect()
        text_rect.topleft = (568, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

    small_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 15)
    text_array = [
        small_font.render("Note: You may need to press", False, text_color),
        small_font.render("press and hold to register the input", False, text_color),
        small_font.render("the input. Forbidden keys include", False, text_color),
        small_font.render("ESCAPE (Closes the game),", False, text_color),
        small_font.render("CONTROL (Toggle Full Screen)", False, text_color),
        small_font.render("ENTER (Navigates Menus)", False, text_color),
    ]

    text_y = 152
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (978, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 36
    
def draw_rules_screen(game_display, ruleset, selector_position, settings):
    draw_background(game_display, "rules", settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_color = (0, 0, 255)

    time_limit_seconds = str((ruleset['time_limit']%3600)//60)
    if(len(time_limit_seconds) == 1):
        time_limit_seconds = "0" + time_limit_seconds

    time_limit_text = f"{ruleset['time_limit']//3600}:{time_limit_seconds}"
    if(ruleset['time_limit'] == 0):
        time_limit_text = "No Limit"

    time_bonus_seconds = str((ruleset['time_bonus']%3600)//60)
    if(len(time_bonus_seconds) == 1):
        time_bonus_seconds = "0" + time_bonus_seconds

    time_bonus_text = f"{ruleset['time_bonus']//3660}:{time_bonus_seconds}"
    if(ruleset['time_bonus'] == 0):
        time_bonus_text = "No Bonus"

    text_array = [
        menu_font.render("Goal Limit: " + str(ruleset['goal_limit']), False, text_color),
        menu_font.render("Time Limit: " + time_limit_text, False, text_color),
        menu_font.render("Time Bonus: " + time_bonus_text, False, text_color),
        menu_font.render("NRG Charge Rate: " + str(ruleset['special_ability_charge_base']), False, text_color),
        menu_font.render("Danger Zone Enabled: " + str(ruleset['danger_zone_enabled']), False, text_color),
        menu_font.render("P1 Stat Modifiers", False, text_color),
        menu_font.render("P2 Stat Modifiers", False, text_color),
        menu_font.render("Reset to Default", False, text_color),
        menu_font.render("<-- Back", False, text_color),
    ]
    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    game_display.blit(ball, (10, (76 * (selector_position + 1))))

def draw_pmods_screen(game_display, info_getter, settings):
    draw_background(game_display, "rules", settings)
    
    selector_position = info_getter[0]
    n_ruleset = info_getter[1]
    player = info_getter[2]
    page = info_getter[3]
    ruleset = {player: {}}
    for key in n_ruleset[player]:
        if(n_ruleset[player][key] is None):
            ruleset[player][key] = "Default"
        else:
            ruleset[player][key] = n_ruleset[player][key]

    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_color = (0, 0, 255)
    if(page == 1):
        text_array = [
            menu_font.render("HP Value: " + str(ruleset[player]['max_hp']), False, text_color),
            menu_font.render("Speed Value: " + str(ruleset[player]['top_speed'])  + " Stars", False, text_color),
            menu_font.render("Traction Value: " + str(ruleset[player]['traction'])  + " Stars", False, text_color),
            menu_font.render("Friction Value: " + str(ruleset[player]['friction'])  + " Stars", False, text_color),
            menu_font.render("Gravity Value: " + str(ruleset[player]['gravity'])  + " Stars", False, text_color),
            menu_font.render("Boost Cost: " + str(ruleset[player]['boost_cost'])  + " Energy", False, text_color),
            menu_font.render("Boost Cooldown: " + str(ruleset[player]['boost_cooldown_max'])  + " Stars", False, text_color),
            menu_font.render("Boost Duration: "  + str(ruleset[player]['boost_duration'])  + " Stars", False, text_color),
            menu_font.render("Next -->", False, text_color),
        ]
    elif(page == 2):
        text_array = [
            menu_font.render("Kick Cooldown: " + str(ruleset[player]['kick_cooldown_rate']) + " Stars", False, text_color),
            menu_font.render("Block Cooldown: " + str(ruleset[player]['block_cooldown_rate'])  + " Stars", False, text_color),
            menu_font.render("Ability Activation Cost: " + str(ruleset[player]['special_ability_cost'])  + " Energy", False, text_color),
            menu_font.render("Ability Maintenance Cost: " + str(ruleset[player]['special_ability_maintenance'])  + " Energy", False, text_color),
            menu_font.render("Maximum Stored Energy: " + str(ruleset[player]['special_ability_max'])  + " Energy", False, text_color),
            menu_font.render("Ability Cooldown: " + str(ruleset[player]['special_ability_cooldown'])  + " Frames", False, text_color),
            menu_font.render("Ability Delay: " + str(ruleset[player]['special_ability_delay'])  + " Frames", False, text_color),
            menu_font.render("Ability Duration: "  + str(ruleset[player]['special_ability_duration'])  + " Frames", False, text_color),
            menu_font.render("Next -->", False, text_color),
        ]

    #TODO: Add a disclaimer! Not all settings will work as expected/intended
    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    game_display.blit(ball, (10, 76 * (selector_position + 1)))
