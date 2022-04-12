from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import draw_ball_particles as draw_ball_particles
from engine.handle_input import return_mapkey_names, return_joystick_mapping
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

    ui_mode_text = "Top" if settings['ui_mode'] else "Bottom"

    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_array = [
        menu_font.render("HD Backgrounds: " + str(settings['hd_backgrounds']), False, text_color),
        menu_font.render("UI Mode: " + ui_mode_text, False, text_color),
        menu_font.render("Smooth Scaling: " + str(settings['smooth_scaling']), False, text_color),
        menu_font.render("Music Volume: " + str(settings['music_volume']), False, text_color),
        menu_font.render("Sound Volume: " + str(settings['sound_volume']), False, text_color),
        menu_font.render("Remap Keyboard", False, text_color),
        menu_font.render("Remap Joystick", False, text_color),
        menu_font.render("Default Controls", False, text_color),
        menu_font.render("Reset to Default", False, text_color),
        menu_font.render("<-- Back", False, text_color),
    ]
    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 60

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    game_display.blit(ball, (10, 76 + 60 * selector_position))

rebind_key_to_position = {
    'p1_up': 1,
    'p1_down': 2,
    'p1_left': 3,
    'p1_right': 4,
    'p1_ability': 5,
    'p1_kick': 6,
    'p1_block': 7,
    'p1_boost': 8, 
    'p2_up': 11,
    'p2_down': 12,
    'p2_left': 13,
    'p2_right': 14,
    'p2_ability': 15,
    'p2_kick': 16,
    'p2_block': 17,
    'p2_boost': 18, 
}

def draw_rebind_screen(game_display, settings, info_getter):
    text_color = (0, 0, 255)
    draw_background(game_display, "rebind", settings)
    rebind_key = info_getter[0]
    selector_position = info_getter[1]
    
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    menu_text = menu_font.render('REBINDING: ' + rebind_key, False, text_color)
    text_rect = menu_text.get_rect()
    text_rect.center = (450, 50)

    game_display.blit(menu_text, text_rect)

    input_keys = return_mapkey_names()
    text_array = []
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
    for key in input_keys:
        text_array.append(menu_font.render(key + ": " + str(input_keys[key]), False, text_color))

    text_array.insert(len(text_array)//2, menu_font.render("Rebind P2", False, text_color))
    text_array.insert(len(text_array)//2, menu_font.render("Rebind All", False, text_color))
    text_array.insert(0, menu_font.render("Rebind P1", False, text_color))
    text_array.append(menu_font.render("Back", False, text_color))

    text_y = 152
    for text_box in text_array[:len(text_array)//2]:
        text_rect = text_box.get_rect()
        text_rect.topleft = (68, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 60
    text_y = 152
    for text_box in text_array[len(text_array)//2:]:
        text_rect = text_box.get_rect()
        text_rect.topleft = (568, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 60
    # TODO: Cache these
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
    if(rebind_key == "Click to Rebind!"): # TODO: Cache these
        ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    else:
        ball = pg.image.load(cwd + "/resources/images/balls/goal_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    if not(rebind_key == "Click to Rebind!"):
        selector_position = rebind_key_to_position[rebind_key]
    
    selector_x = 500 * (selector_position//10)
    selector_y = 150 + 60 * (selector_position%10)

    game_display.blit(ball, (selector_x, selector_y))
    

def draw_controller_bind_screen(game_display, info_getter, settings):
    text_color = (0, 0, 255)
    draw_background(game_display, "rebind", settings)

    player_page = info_getter[0]
    selector_position = info_getter[1]
    controller_mapping = info_getter[2]

    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    menu_text = menu_font.render('PLAYER PAGE' + str(player_page) + controller_mapping, False, text_color)
    text_rect = menu_text.get_rect()
    text_rect.center = (450, 50)
    game_display.blit(menu_text, text_rect)

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png") # TODO: Cache this
    ball = pg.transform.scale(ball, (38, 38))

    input_keys = return_joystick_mapping()
    if(player_page == 0):

        selector_x = 500 * (selector_position//4)
        selector_y = 150 + 60 * (selector_position%4)

        game_display.blit(ball, (selector_x, selector_y))

        text_array = []
        for i in input_keys:
            for j in input_keys[i]:
                config_text = j
                if(config_text == "GameCube Controller Adapter"):
                    config_text = "GCCA"
                text_array.append(menu_font.render(config_text, False, text_color))

        text_array.insert(len(text_array)//2, menu_font.render("Reset All", False, text_color))
        text_array.append(menu_font.render("Back", False, text_color))

        text_y = 152
        for text_box in text_array[:len(text_array)//2]:
            text_rect = text_box.get_rect()
            text_rect.topleft = (68, text_y)
            game_display.blit(text_box, text_rect)
            text_y += 60
        
        text_y = 152
        for text_box in text_array[len(text_array)//2:]:
            text_rect = text_box.get_rect()
            text_rect.topleft = (568, text_y)
            game_display.blit(text_box, text_rect)
            text_y += 60
    elif(player_page == 1 or player_page == 2):
        active_joystick_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]

        if(controller_mapping == "GameCube Controller Adapter"):
            y_shift = 55
            text_array = [
                menu_font.render("H Deadzone: " + str(active_joystick_mapping['horizontal_deadzone']), False, text_color),
                menu_font.render("V Deadzone: " + str(active_joystick_mapping['vertical_deadzone']), False, text_color),
                menu_font.render("A: " + str(active_joystick_mapping['1']), False, text_color),
                menu_font.render("B: " + str(active_joystick_mapping['2']), False, text_color),
                menu_font.render("X: " + str(active_joystick_mapping['0']), False, text_color),
                menu_font.render("Y: " + str(active_joystick_mapping['3']), False, text_color),
                menu_font.render("Z: " + str(active_joystick_mapping['7']), False, text_color),
                menu_font.render("L: " + str(active_joystick_mapping['4']), False, text_color),
                menu_font.render("R: " + str(active_joystick_mapping['5']), False, text_color),
                menu_font.render("Rumble: " + str(active_joystick_mapping['rumble']), False, text_color),
                menu_font.render("Back", False, text_color),
            ]
        elif(controller_mapping == "Generic"):
            y_shift = 55
            text_array = [
                menu_font.render("H Deadzone: " + str(active_joystick_mapping['horizontal_deadzone']), False, text_color),
                menu_font.render("V Deadzone: " + str(active_joystick_mapping['vertical_deadzone']), False, text_color),
                menu_font.render("B0: " + str(active_joystick_mapping['0']), False, text_color),
                menu_font.render("B1: " + str(active_joystick_mapping['1']), False, text_color),
                menu_font.render("B2: " + str(active_joystick_mapping['2']), False, text_color),
                menu_font.render("B3: " + str(active_joystick_mapping['3']), False, text_color),
                menu_font.render("B4: " + str(active_joystick_mapping['4']), False, text_color),
                menu_font.render("B5: " + str(active_joystick_mapping['5']), False, text_color),
                menu_font.render("B6: " + str(active_joystick_mapping['6']), False, text_color),
                menu_font.render("Rumble: " + str(active_joystick_mapping['rumble']), False, text_color),
                menu_font.render("Back", False, text_color),
            ]
        elif(controller_mapping == "Xbox 360 Controller"):
            y_shift = 50
            text_array = [
                menu_font.render("H Deadzone: " + str(active_joystick_mapping['horizontal_deadzone']), False, text_color),
                menu_font.render("V Deadzone: " + str(active_joystick_mapping['vertical_deadzone']), False, text_color),
                menu_font.render("A: " + str(active_joystick_mapping['0']), False, text_color),
                menu_font.render("B: " + str(active_joystick_mapping['1']), False, text_color),
                menu_font.render("X: " + str(active_joystick_mapping['2']), False, text_color),
                menu_font.render("Y: " + str(active_joystick_mapping['3']), False, text_color),
                menu_font.render("LB: " + str(active_joystick_mapping['4']), False, text_color),
                menu_font.render("RB: " + str(active_joystick_mapping['5']), False, text_color),
                menu_font.render("LT: " + str(active_joystick_mapping['lt']), False, text_color),
                menu_font.render("RT: " + str(active_joystick_mapping['rt']), False, text_color),
                menu_font.render("Rumble: " + str(active_joystick_mapping['rumble']), False, text_color),
                menu_font.render("Back", False, text_color),
            ]
        
        selector_x = 0
        selector_y = 150 + y_shift * (selector_position)

        game_display.blit(ball, (selector_x, selector_y))

        text_y = 152
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.topleft = (68, text_y)
            game_display.blit(text_box, text_rect)
            text_y += y_shift

    #print(len(text_array))


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
        menu_font.render("HP Regeneration: " + str(ruleset['hp_regen']), False, text_color),
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
        text_y += 66

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38))
    game_display.blit(ball, (10, 76 + (66 * selector_position)))

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
