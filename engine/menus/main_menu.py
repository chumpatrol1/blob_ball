'''
engine/menus/main_menu.py

Handles the splash screen and main menu navigation functions

> game_state_navigation(): Takes a selector position and tells what game state that translates to
> menu_navigation(): Handles the mouse and keyboard navigation of the main menu
> splash_navigator(): Handles the splash screen menu and its flashing
'''
import engine.handle_input
from json import dumps
from os import getcwd
from resources.graphics_engine.display_almanac import load_almanac_static_text, unload_almanac_static_text
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button
cwd = getcwd()
selector_position = 0

buttons = [
    Button(50, 125, 525, 825),
    Button(125, 200, 525, 825),
    Button(200, 275, 525, 825),
    Button(275, 350, 525, 825),
    Button(350, 425, 525, 825),
    Button(425, 500, 525, 825),
    Button(500, 575, 525, 825),
    Button(575, 650, 525, 825),
]

def game_state_navigation(selector_position):
    '''
    Takes a selector position and tells what game state that translates to

    Inputs
        - selector_position [int]: An integer representing the selector location, ranging from 0-7

    Outputs
        - game_state [string]: String representing the updated game state, which is pulled from the dictionary
    '''
    game_state = {
        0: "css",
        1: "main_menu",
        2: "almanac",
        3: "rules",
        4: "settings",
        #5: "medals",
        5: "main_menu",
        6: "tutorial",
        7: "quit",
    }
    

    return game_state[selector_position]

def menu_navigation(timer):
    '''
    Handles the mouse and keyboard navigation of the main menu

    Inputs:
        - timer [int]: The timer, which prevents the player from navigating too quickly

    Outputs:
        - game_state [string]: String representing the updated game state, which is pulled from the dictionary. Defaults to "main_menu"
    '''
    game_state = "main_menu"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 7
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 7:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        game_state = game_state_navigation(selector_position)
    for i in range(len(buttons)):
        if(buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0] or mouse[1][2]):
                createSFXEvent('select')
                game_state = game_state_navigation(selector_position)


    if(game_state == 'almanac'):
        load_almanac_static_text()
    else:
        unload_almanac_static_text()  
    
    return game_state, [selector_position]


splash_flash_timer = 60
def splash_navigator():
    '''
    # TODO: Standardize return!
    Handles the splash screen menu and its flashing

    Inputs:
        - splash_flash_timer [int]: Number telling the game whether or not to display a certain text splash
    
    Outputs:
        - game_state [string]: String representing the updated game state, which is pulled from the dictionary. Defaults to "control_splash"
        - info_getter [array]
            - splash_flash_timer [int]: Number telling the game whether or not to display a certain text splash
    '''
    global splash_flash_timer
    game_state = "control_splash"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    if('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "main_menu"
    splash_flash_timer -= 1
    if(splash_flash_timer == 0):
        splash_flash_timer = 60
    return [splash_flash_timer], game_state