import engine.handle_input
from json import dumps
from os import getcwd
from engine.unlocks import return_css_selector_medals
from engine.menus.main_menu import game_state_navigation
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button
cwd = getcwd()

medal_selected = str("goal")
xpos = 0
ypos = 0
conf = 0

# X position, Y position
selector_position = (xpos, ypos)
medal_list = return_css_selector_medals

def medal_navigation(timer):
    game_state = "medals"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global ypos
    global xpos
    global selector_position
    global medal_selected
    if('p1_up' in pressed or 'p2_up' in pressed):
        if ypos == 0:
            ypos = 4
        else:
            ypos -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if ypos == 4:
            ypos = 0
        else:
            ypos += 1
    if('p1_right' in pressed or 'p2_right' in pressed):
        if xpos == 7:
            xpos = 0
        else:
            xpos += 1
    elif('p1_left' in pressed or 'p2_left' in pressed):
        if xpos == 0:
            xpos = 7
        else:
            xpos -= 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        medal_selected = game_state_navigation(selector_position)
            
    return game_state, [selector_position]