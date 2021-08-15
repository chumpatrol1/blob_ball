import pygame as pg
import sys
import engine.handle_input
from engine.handle_input import reset_inputs
from json import dumps
from os import getcwd
cwd = getcwd()

pg.init()
clock = pg.time.Clock()
clock.tick(60)

selector_position = 0
p1_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
p2_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
p1_blob = "quirkless"
p2_blob = "quirkless"

def menu_navigation(timer):
    game_state = "main_menu"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(selector_position == 0): #Casual
            game_state = "css"
        elif(selector_position == 1):
            selector_position = 0
        elif(selector_position == 2):
            selector_position = 0
            game_state = "almanac"
        elif(selector_position == 3):
            selector_position = 0
            game_state = "rules"
        elif(selector_position == 4):
            selector_position = 0
            game_state = "settings"
        elif(selector_position == 5): #Quits the game
            game_state = "quit"
            
    return selector_position, game_state

def almanac_navigation(timer, previous_screen):
    game_state = "almanac"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(selector_position == 0): #Casual
            game_state = "almanac"
        elif(selector_position == 1):
            selector_position = 0
        elif(selector_position == 2):
            game_state = "almanac_stats"
        elif(selector_position == 3):
            selector_position = 0
            game_state = "almanac_art"
        elif(selector_position == 4):
            game_state = "credits"
        elif(selector_position == 5): #Go back
            game_state = previous_screen
            if(previous_screen == "main_menu"):
                selector_position = 2
            else:
                selector_position = 0
            
        print("Selected position {}!".format(selector_position))
    return selector_position, game_state

def almanac_stats_navigation(timer):
    pressed = engine.handle_input.menu_input()
    game_state = "almanac_stats"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state = "almanac_stats_page_2"
    return [game_state]

def almanac_stats_navigation_2(timer):
    pressed = engine.handle_input.menu_input()
    game_state = "almanac_stats_page_2"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state = "almanac"
    return [game_state]

def almanac_art_navigation(timer):
    game_state = "almanac_art"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(selector_position == 5): #Casual
            game_state = "almanac"
            selector_position = 3
        elif(selector_position == 0):
            game_state = "almanac_art_backgrounds"
        elif(selector_position == 1):
            selector_position = 0
            game_state = "almanac_art_blobs"
            
        print("Selected position {}!".format(selector_position))
    return selector_position, game_state

def almanac_art_backgrounds_navigation(timer):
    game_state = "almanac_art_backgrounds"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 6
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed):
        if selector_position == 6:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def almanac_art_blobs_navigation(timer):
    game_state = "almanac_art_blobs"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 39
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed):
        if selector_position == 39:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def credits_navigation(timer):
    pressed = engine.handle_input.menu_input()
    game_state = "credits"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state = "almanac"
    return [game_state]

blob_list = [
    ["back", "quirkless", "fire", "ice", "water", "rock", "lightning", "wind",],
    ["rules", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["settings", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["almanac", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
]

def css_navigation(player, selector, timer, other_selector):
    pressed_conversions = engine.handle_input.player_to_controls(player)
    pressed_buttons = engine.handle_input.css_input()
    pressed = []
    for button in pressed_buttons:
        if(button in pressed_conversions):
            pressed.append(pressed_conversions[button])
        
    if pressed == []:
        timer = 0

    if not timer == 0:
        pressed = []
        
    if not (pressed == []):
        if('ability' in pressed):
            timer = 15
        else:
            timer = 30
    
    
    if(selector[2] == 0):
        if('up' in pressed):
            if selector[1] == 0:
                selector[1] = 4
                
            else:
                selector[1] -= 1
        elif('down' in pressed):
            if selector[1] == 4:
                selector[1] = 0
            else:
                selector[1] += 1
        if('left' in pressed):
            if selector[0] == 0:
                selector[0] = 7
            else:
                selector[0] -= 1
        elif('right' in pressed):
            if selector[0] == 7:
                selector[0] = 0
            else:
                selector[0] += 1
    
    if(selector[2] == 0):
        if('ability' in pressed):
            selector[2] = 1
    elif('kick' in pressed):
        selector[2] = 0
        if(other_selector[2] == 2):
            #Deconfirms the other player's selection if the other player has confirmed
            other_selector[2] = 1
    elif(selector[2] >= 1 and other_selector[2] >= 1):
        if('ability' in pressed):
            selector[2] = 2

    return selector, timer, other_selector
    
p1_timer = 0
p2_timer = 0
def css_handler():
    global p1_selector_position
    global p2_selector_position
    global p1_blob
    global p2_blob
    global p1_timer
    global p2_timer
    game_state = "css"
    p1_selector_position, p1_timer, p2_selector_position = css_navigation(1, p1_selector_position, p1_timer, p2_selector_position)
    p2_selector_position, p2_timer, p1_selector_position = css_navigation(2, p2_selector_position, p2_timer, p1_selector_position)
    
    if(p1_selector_position[2] == 1):
        if(p1_selector_position[0] == 0):
            if(p1_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p1_selector_position[1] == 1):
                game_state = "rules"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 2):
                game_state = "settings"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 3):
                game_state = "almanac"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 4):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
        else:
            #TODO: Fix this spaghetti
            p1_blob = blob_list[p1_selector_position[1]][p1_selector_position[0]]
    
    if(p2_selector_position[2] == 1):
        if(p2_selector_position[0] == 0):
            if(p2_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p2_selector_position[1] == 1):
                game_state = "rules"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 2):
                game_state = "settings"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 3):
                game_state = "almanac"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 4):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
        else:
            #TODO: Fix this spaghetti
            p2_blob = blob_list[p2_selector_position[1]][p2_selector_position[0]]

    if(p1_selector_position[2] == 2 and p2_selector_position[2] == 2):
        print("Casual Match Started!")
        game_state = "casual_match"
    
    if(game_state == "casual_match"):
        p1_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed
        p2_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed

    if(p1_timer > 0):
        p1_timer -= 1
    if(p2_timer > 0):
        p2_timer -= 1
    return p1_selector_position, p2_selector_position, game_state, p1_blob, p2_blob

def rules_navigation(timer, ruleset, previous_screen, cwd):
    game_state = "rules"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = len(ruleset)
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == len(ruleset):
            selector_position = 0
        else:
            selector_position += 1
    if('p1_left' in pressed or 'p2_left' in pressed):
        if(selector_position == 0):
            if(ruleset['goal_limit'] > 1):
                ruleset['goal_limit'] -= 1
            else:
                ruleset['goal_limit'] = 25
        elif(selector_position == 1):
            if(ruleset['time_limit'] > 0):
                ruleset['time_limit'] -= 600
            else:
                ruleset['time_limit'] = 36000
        elif(selector_position == 2):
            if(ruleset['time_bonus'] > 0):
                ruleset['time_bonus'] -= 300
            else:
                ruleset['time_bonus'] = 3600
        elif(selector_position == 3):
            if(ruleset['special_ability_charge_base'] > 0):
                ruleset['special_ability_charge_base'] -= 1
            else:
                ruleset['special_ability_charge_base'] = 20
        with open(cwd+'/engine/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))
    elif('p1_right' in pressed or 'p2_right' in pressed or 'return' in pressed):
        if(selector_position == 0):
            if(ruleset['goal_limit'] < 25):
                ruleset['goal_limit'] += 1
            else:
                ruleset['goal_limit'] = 1
        elif(selector_position == 1):
            if(ruleset['time_limit'] < 36000):
                ruleset['time_limit'] += 600
            else:
                ruleset['time_limit'] = 0
        elif(selector_position == 2):
            if(ruleset['time_bonus'] < 3600):
                ruleset['time_bonus'] += 300
            else:
                ruleset['time_bonus'] = 0
        elif(selector_position == 3):
            if(ruleset['special_ability_charge_base'] < 20):
                ruleset['special_ability_charge_base'] += 1
            else:
                ruleset['special_ability_charge_base'] = 0
        with open(cwd+'/engine/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(selector_position == len(ruleset)):
            if(previous_screen == "main_menu"):
                selector_position = 3
            else:
                selector_position = 0
            print(previous_screen)
            game_state = previous_screen
        elif(selector_position == len(ruleset) - 1):
            ruleset['goal_limit'] = 5
            ruleset['time_limit'] = 3600
            ruleset['time_bonus'] = 600
            ruleset['special_ability_charge_base'] = 1
            ruleset['danger_zone_enabled'] = True
        elif(selector_position == 4):
            ruleset['danger_zone_enabled'] = not(ruleset['danger_zone_enabled'])
        with open(cwd+'/engine/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))
            
    return selector_position, game_state

def settings_navigation(timer, settings, previous_screen, cwd):
    game_state = "settings"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = len(settings) + 3
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == len(settings) + 3:
            selector_position = 0
        else:
            selector_position += 1

    if('p1_left' in pressed or 'p2_left' in pressed):
        pass
    elif('p1_right' in pressed or 'p2_right' in pressed):
        pass

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(selector_position == len(settings) + 3):
            if(previous_screen == "main_menu"):
                selector_position = 4
            else:
                selector_position = 0
            game_state = previous_screen
        elif(selector_position == len(settings) + 2):
            settings['hd_backgrounds'] = True
            settings['hd_blobs'] = True
            settings['smooth_scaling'] = True
        elif(selector_position == len(settings) + 1):
            reset_inputs()
        elif(selector_position == 0):
            game_state = "rebind"
        elif(selector_position == 1):
            settings['hd_backgrounds'] = not(settings['hd_backgrounds'])
        elif(selector_position == 2):
            settings['hd_blobs'] = not(settings['hd_blobs'])
        elif(selector_position == 3):
            settings['smooth_scaling'] = not(settings['smooth_scaling'])

        with open(cwd+'/engine/config/settings.txt', 'w') as settingsdoc:
            settingsdoc.write(dumps(settings))

    return selector_position, game_state
