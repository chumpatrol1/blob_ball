import engine.handle_input
from json import dumps
from os import getcwd
from resources.sound_engine.sfx_event import createSFXEvent
cwd = getcwd()
selector_position = 0
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
        createSFXEvent('select')
        if(selector_position == 0): #Casual
            game_state = "css"
        elif(selector_position == 1):
            selector_position = 0
        elif(selector_position == 2):
            game_state = "almanac"
        elif(selector_position == 3):
            game_state = "rules"
        elif(selector_position == 4):
            game_state = "settings"
        elif(selector_position == 5): #Quits the game
            game_state = "quit"
            
    return game_state, [selector_position]


splash_flash_timer = 60
def splash_navigator():
    global splash_flash_timer
    game_state = "control_splash"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    if('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed or mouse[1][0]):
        createSFXEvent('select')
        game_state = "main_menu"
    splash_flash_timer -= 1
    if(splash_flash_timer == 0):
        splash_flash_timer = 60
    return [splash_flash_timer], game_state