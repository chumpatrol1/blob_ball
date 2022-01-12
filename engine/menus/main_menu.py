import engine.handle_input
from json import dumps
from os import getcwd
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button
cwd = getcwd()
selector_position = 0

buttons = [
    Button(50, 100, 525, 825),
    Button(125, 175, 525, 825),
    Button(200, 250, 525, 825),
    Button(275, 325, 525, 825),
    Button(350, 400, 525, 825),
    Button(425, 475, 525, 825),
    Button(500, 550, 525, 825),
]

def game_state_navigation(selector_position):
    
    game_state = {
        0: "css",
        1: "main_menu",
        2: "almanac",
        3: "rules",
        4: "settings",
        5: "quit",
        6: "medals",
    }
    

    return game_state[selector_position]

def menu_navigation(timer):
    game_state = "main_menu"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 6
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 6:
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