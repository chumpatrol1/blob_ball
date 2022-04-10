from engine.handle_input import bind_input as bind_input
from engine.handle_input import reset_joystick_map
from engine.handle_input import get_keypress
from engine.handle_input import return_joystick_mapping
from engine.handle_input import bind_to_joy
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

def rebind_gcca(player):
    #print(return_joystick_mapping()[str(player)]["GameCube Controller Adapter"])
    game_state = "controller_config"
    controller_mapping = "GameCube Controller Adapter"
    createSFXEvent("select")
    return game_state, controller_mapping

def rebind_generic(player):
    #print(return_joystick_mapping()[str(player)]["Generic"])
    game_state = "controller_config"
    controller_mapping = "Generic"
    createSFXEvent("select")
    return game_state, controller_mapping

def joystick_misc_func(player):
    global player_page
    global selector_position
    if(player == 1):
        selector_position = 2
        createSFXEvent('chime_completion') # TODO: Actually reset the joysticks
        reset_joystick_map()
        game_state = "controller_config"
        controller_mapping = ""
    else:
        game_state = "settings"
        player_page = 0
        selector_position = 0
        controller_mapping = ""
        createSFXEvent("select")
    return game_state, controller_mapping

config_menu_func_dict = {
    0: rebind_gcca,
    1: rebind_generic,
    2: joystick_misc_func,
}

cycle_left_dict = {
    'ability': 'none',
    'kick': 'ability',
    'block': 'kick',
    'boost': 'block',
    'up': 'boost',
    'down': 'up',
    'none': 'down',
}

cycle_right_dict = {
    'ability': 'kick',
    'kick': 'block',
    'block': 'boost',
    'boost': 'up',
    'up': 'down',
    'down': 'none',
    'none': 'ability',
}


def handle_joystick_config():
    global player_page
    global selector_position
    global controller_mapping
    game_state = "controller_config"

    pressed = merge_inputs(menu_input(), True)
    

    if('up' in pressed):
        selector_position -= 1
        if(selector_position <= -1):
            if(player_page == 0):
                selector_position = 5
            else:
                if(controller_mapping == "GameCube Controller Adapter"):
                    selector_position = 10
                elif(controller_mapping == "Generic"):
                    selector_position = 10
                else:
                    selector_position = 10

    elif('down' in pressed):
        selector_position += 1
        selector_max = 0
        if(player_page == 0):
            selector_max = 5
        else:
            if(controller_mapping == "GameCube Controller Adapter"):
                selector_max = 10
            elif(controller_mapping == "Generic"):
                selector_max = 10
            else:
                selector_max = 10

        if(selector_position > selector_max):
            selector_position = 0
    
    if('left' in pressed):
        if(player_page == 0):
            selector_position -= 3
            if(selector_position <= -1):
                selector_position += 6
        else:
            if(controller_mapping == "GameCube Controller Adapter"):
                current_mapping = return_joystick_mapping()[str(player_page)]["GameCube Controller Adapter"]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                if(selector_position == 0): # H Dead
                    bind_to_joy_arr[2] = 'horizontal_deadzone'
                    value = current_mapping['horizontal_deadzone']
                    value = round(value - 0.1, 1)
                    if(value < 0.1):
                        value = 0.8
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                    
                elif(selector_position == 1): # V Dead
                    bind_to_joy_arr[2] = 'vertical_deadzone'
                    value = current_mapping['vertical_deadzone']
                    value = round(value - 0.1, 1)
                    if(value < 0.1):
                        value = 0.8
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)

                elif(selector_position == 2): # A
                    bind_to_joy_arr[2] = '1'
                    value = current_mapping['1']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 3): # B
                    bind_to_joy_arr[2] = '2'
                    value = current_mapping['2']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 4): # X
                    bind_to_joy_arr[2] = '0'
                    value = current_mapping['0']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 5): # Y
                    bind_to_joy_arr[2] = '3'
                    value = current_mapping['3']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 6): # Z
                    bind_to_joy_arr[2] = '7'
                    value = current_mapping['7']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 7): # L
                    bind_to_joy_arr[2] = '4'
                    value = current_mapping['4']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 8): # R
                    bind_to_joy_arr[2] = '5'
                    value = current_mapping['5']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 9): # Rumble
                    bind_to_joy_arr[2] = 'rumble'
                    value = current_mapping['rumble']
                    value = not value
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)

            elif(controller_mapping == "Generic"): # TODO: Make this more modular?
                current_mapping = return_joystick_mapping()[str(player_page)]["Generic"]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                if(selector_position == 0): # H Dead
                    bind_to_joy_arr[2] = 'horizontal_deadzone'
                    value = current_mapping['horizontal_deadzone']
                    value = round(value - 0.1, 1)
                    if(value < 0.1):
                        value = 0.8
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                    
                elif(selector_position == 1): # V Dead
                    bind_to_joy_arr[2] = 'vertical_deadzone'
                    value = current_mapping['vertical_deadzone']
                    value = round(value - 0.1, 1)
                    if(value < 0.1):
                        value = 0.8
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)

                elif(selector_position == 2): # B0
                    bind_to_joy_arr[2] = '0'
                    value = current_mapping['0']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 3): # B1
                    bind_to_joy_arr[2] = '1'
                    value = current_mapping['1']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 4): # B2
                    bind_to_joy_arr[2] = '2'
                    value = current_mapping['2']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 5): # B3
                    bind_to_joy_arr[2] = '3'
                    value = current_mapping['3']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 6): # B4
                    bind_to_joy_arr[2] = '4'
                    value = current_mapping['4']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 7): # B5
                    bind_to_joy_arr[2] = '5'
                    value = current_mapping['5']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 8): # B6
                    bind_to_joy_arr[2] = '6'
                    value = current_mapping['6']
                    value = cycle_left_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 9): # Rumble
                    bind_to_joy_arr[2] = 'rumble'
                    value = current_mapping['rumble']
                    value = not value
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
    elif('right' in pressed):
        if(player_page == 0):
            selector_position += 3
            if(selector_position >= 6):
                selector_position -= 6
        else:
            if(controller_mapping == "GameCube Controller Adapter"):
                current_mapping = return_joystick_mapping()[str(player_page)]["GameCube Controller Adapter"]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                if(selector_position == 0): # H Dead
                    bind_to_joy_arr[2] = 'horizontal_deadzone'
                    value = current_mapping['horizontal_deadzone']
                    value = round(value + 0.1, 1)
                    if(value > 0.8):
                        value = 0.1
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                    
                elif(selector_position == 1): # V Dead
                    bind_to_joy_arr[2] = 'vertical_deadzone'
                    value = current_mapping['vertical_deadzone']
                    value = round(value + 0.1, 1)
                    if(value > 0.8):
                        value = 0.1
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)

                elif(selector_position == 2): # A
                    bind_to_joy_arr[2] = '1'
                    value = current_mapping['1']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 3): # B
                    bind_to_joy_arr[2] = '2'
                    value = current_mapping['2']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 4): # X
                    bind_to_joy_arr[2] = '0'
                    value = current_mapping['0']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 5): # Y
                    bind_to_joy_arr[2] = '3'
                    value = current_mapping['3']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 6): # Z
                    bind_to_joy_arr[2] = '7'
                    value = current_mapping['7']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 7): # L
                    bind_to_joy_arr[2] = '4'
                    value = current_mapping['4']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 8): # R
                    bind_to_joy_arr[2] = '5'
                    value = current_mapping['5']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 9): # Rumble
                    bind_to_joy_arr[2] = 'rumble'
                    value = current_mapping['rumble']
                    value = not value
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
            elif(controller_mapping == "Generic"): # TODO: Make this more modular?
                current_mapping = return_joystick_mapping()[str(player_page)]["Generic"]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                if(selector_position == 0): # H Dead
                    bind_to_joy_arr[2] = 'horizontal_deadzone'
                    value = current_mapping['horizontal_deadzone']
                    value = round(value + 0.1, 1)
                    if(value > 0.8):
                        value = 0.1
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                    
                elif(selector_position == 1): # V Dead
                    bind_to_joy_arr[2] = 'vertical_deadzone'
                    value = current_mapping['vertical_deadzone']
                    value = round(value + 0.1, 1)
                    if(value > 0.8):
                        value = 0.1
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)

                elif(selector_position == 2): # B0
                    bind_to_joy_arr[2] = '0'
                    value = current_mapping['0']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 3): # B1
                    bind_to_joy_arr[2] = '1'
                    value = current_mapping['1']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 4): # B2
                    bind_to_joy_arr[2] = '2'
                    value = current_mapping['2']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 5): # B3
                    bind_to_joy_arr[2] = '3'
                    value = current_mapping['3']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 6): # B4
                    bind_to_joy_arr[2] = '4'
                    value = current_mapping['4']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 7): # B5
                    bind_to_joy_arr[2] = '5'
                    value = current_mapping['5']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 8): # B6
                    bind_to_joy_arr[2] = '6'
                    value = current_mapping['6']
                    value = cycle_right_dict[value]
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)
                elif(selector_position == 9): # Rumble
                    bind_to_joy_arr[2] = 'rumble'
                    value = current_mapping['rumble']
                    value = not value
                    bind_to_joy_arr[3] = value
                    bind_to_joy(*bind_to_joy_arr)


    if('ability' in pressed):
        if(player_page == 0 and selector_position % 3 in config_menu_func_dict):
            player_page = (selector_position//3) + 1
            game_state, controller_mapping = config_menu_func_dict[selector_position % 3](player_page)
            if(selector_position != 2):
                selector_position = 0
            else:
                player_page = 0
        else:
            if(controller_mapping == "GameCube Controller Adapter" and selector_position == 10):
                selector_position = 0
                player_page = 0
                controller_mapping = ""
            if(controller_mapping == "Generic" and selector_position == 10):
                selector_position = 0
                player_page = 0
                controller_mapping = ""


    return game_state, [player_page, selector_position, controller_mapping]