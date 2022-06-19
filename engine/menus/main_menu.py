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
    
    game_state = {
        0: "css",
        1: "main_menu",
        2: "almanac",
        3: "rules",
        4: "settings",
        5: "medals",
        #5: "main_menu",
        6: "main_menu",
        #6: "tutorial",
        7: "quit",
    }
    

    return game_state[selector_position]

def menu_navigation(timer):
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