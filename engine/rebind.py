from engine.handle_input import bind_input as bind_input, get_keypress
from engine.handle_input import menu_input
from engine.handle_input import unbind_inputs as unbind_inputs
from engine.handle_input import handle_mouse
from engine.handle_input import merge_inputs

from engine.button import Button
from resources.sound_engine.sfx_event import createSFXEvent
rebind_buttons = [
]

for i in range(2): # 2 columns
    for j in range(10): # 10 rows
        rebind_buttons.append(Button(140+60*j, 200 + 60*j, i*450, 450 + i*450))

# God forbid I made spaghetti

rebind_array = ['p1_up', 'p1_down', 'p1_left', 'p1_right', 'p1_ability', 'p1_kick', 'p1_block', 'p1_boost',
'p2_up', 'p2_down', 'p2_left', 'p2_right', 'p2_ability', 'p2_kick', 'p2_block', 'p2_boost',
    ]
rebind_number = -1
rebind_end = 16
selector_position = 0
rebind_start = 0

def handle_rebinding():
    global rebind_number

    if(bind_input(rebind_array[rebind_number], rebind_array[rebind_end])):
        rebind_number += 1
        if(rebind_number - 1 == rebind_end):
            rebind_number = -1
            createSFXEvent('chime_completion')
        else: createSFXEvent('chime_progress')
    
    rebind_key = rebind_array[rebind_number]

    return rebind_key

def choose_rebinds(selector_position):
    global rebind_number
    global rebind_end
    rebind_start = 0
    game_state = 'rebind'
    if(selector_position == 0):
        unbind_inputs('p1')
        rebind_end = 7
        rebind_number = 0
        createSFXEvent('chime_progress')
    elif(selector_position == 10):
        unbind_inputs('p2')
        rebind_end = 15
        rebind_number = 8
    elif(selector_position == 9):
        unbind_inputs()
        rebind_end = 15
        rebind_number = 0
    elif(selector_position == 19):
        game_state = 'settings'
    else:
        if(selector_position < 9):
            rebind_number = selector_position - 1
            rebind_end = rebind_number
        else:
            rebind_number = selector_position - 3
            rebind_end = rebind_number
        unbind_inputs(rebind_array[rebind_number])

    return game_state, rebind_start

def rebind_menu():
    global rebind_number
    global selector_position
    global rebind_number
    global rebind_start
    mouse = handle_mouse()
    game_state = "rebind"
    rebind_key = "Click to Rebind!"

    if(rebind_number == -1):
        for i in range(len(rebind_buttons)):
            if(rebind_buttons[i].check_hover(mouse)):
                if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                    selector_position = i # Change the selector position

                if(mouse[1][0]):
                    game_state, rebind_start = choose_rebinds(selector_position)

                elif(mouse[1][2]):
                    game_state, rebind_start = choose_rebinds(selector_position)
    else:
       rebind_key = handle_rebinding()


    return game_state, [rebind_key, selector_position]

player_page = 0 # 0 is default page, 1 and 2 
controller_mapping = ""
def handle_joystick_config():
    global player_page
    global selector_position
    global controller_mapping
    game_state = "controller_config"

    pressed = merge_inputs(menu_input(), True)
    

    if('up' in pressed):
        selector_position -= 1
        if(selector_position <= -1):
            selector_position = 5
    elif('down' in pressed):
        selector_position += 1
        if(selector_position >= 6):
            selector_position = 0
    
    if('left' in pressed):
        selector_position -= 3
        if(selector_position <= -1):
            selector_position += 6
    elif('right' in pressed):
        selector_position += 3
        if(selector_position >= 6):
            selector_position -= 6

    if('ability' in pressed):
        if(selector_position == 5):
            game_state = "settings"
            player_page = 0
            selector_position = 0
            controller_mapping = ""
            createSFXEvent("select")

    return game_state, [player_page, selector_position, controller_mapping]