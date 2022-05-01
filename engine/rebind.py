from engine.controller_mappings.gamecube_helper import gamecube_controller_left, gamecube_controller_right
from engine.controller_mappings.generic_helper import generic_left, generic_right
from engine.controller_mappings.xbox_360_helper import xbox_360_left, xbox_360_right
from engine.handle_input import bind_input as bind_input
from engine.handle_input import reset_joystick_map
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

joy_page_0 = [
]

joy_shift_50 = [
]

joy_shift_55 = [
]

for i in range(2): # 2 columns
    for j in range(10): # 10 rows
        rebind_buttons.append(Button(140+60*j, 200 + 60*j, i*450, 450 + i*450))

for i in range(2): # 2 columns
    for j in range(4): # 10 rows
        joy_page_0.append(Button(140+60*j, 200 + 60*j, i*450, 450 + i*450))

for i in range(1): # 2 columns
    for j in range(12): # 10 rows
        joy_shift_50.append(Button(140+50*j, 200 + 50*j, i*900, 900 + i*900))

for i in range(1): # 2 columns
    for j in range(11): # 10 rows
        joy_shift_55.append(Button(140+55*j, 200 + 55*j, i*900, 900 + i*900))

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

def rebind_xbox360(player):
    #print(return_joystick_mapping()[str(player)]["Generic"])
    game_state = "controller_config"
    controller_mapping = "Xbox 360 Controller"
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
        selector_position = 3
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
    'GameCube Controller Adapter': rebind_gcca,
    'Xbox 360 Controller': rebind_xbox360,
    'Generic': rebind_generic,
    3: joystick_misc_func, 
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
                selector_position = 7
            else:
                if(controller_mapping == "GameCube Controller Adapter"):
                    selector_position = 10
                elif(controller_mapping == "Xbox 360 Controller"):
                    selector_position = 11
                elif(controller_mapping == "Generic"):
                    selector_position = 11
                else:
                    selector_position = 10

    elif('down' in pressed):
        selector_position += 1
        selector_max = 0
        if(player_page == 0):
            selector_max = 7
        else:
            if(controller_mapping == "GameCube Controller Adapter"):
                selector_max = 10
            elif(controller_mapping == "Xbox 360 Controller"):
                selector_max = 11
            elif(controller_mapping == "Generic"):
                selector_max = 11
            else:
                selector_max = 10

        if(selector_position > selector_max):
            selector_position = 0
    
    if('left' in pressed):
        if(player_page == 0):
            selector_position -= 4
            if(selector_position <= -1):
                selector_position += 8
        else:
            if(controller_mapping == "GameCube Controller Adapter"):
                current_mapping = return_joystick_mapping()[str(player_page)]["GameCube Controller Adapter"]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                gamecube_controller_left(selector_position, bind_to_joy_arr, current_mapping)
                bind_to_joy(*bind_to_joy_arr)
            elif(controller_mapping == "Xbox 360 Controller"): # TODO: Make this more modular?
                current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                xbox_360_left(selector_position, bind_to_joy_arr, current_mapping)
                bind_to_joy(*bind_to_joy_arr)
            elif(controller_mapping == "Generic"): # TODO: Make this more modular?
                current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                generic_left(selector_position, bind_to_joy_arr, current_mapping)
                bind_to_joy(*bind_to_joy_arr)
    elif('right' in pressed or 'ability' in pressed or 'return' in pressed):
        if(player_page == 0 and 'ability' not in pressed and 'return' not in pressed):
            selector_position += 4
            if(selector_position >= 8):
                selector_position -= 8
        else:
            if(controller_mapping == "GameCube Controller Adapter"):
                current_mapping = return_joystick_mapping()[str(player_page)]["GameCube Controller Adapter"]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                gamecube_controller_right(selector_position, bind_to_joy_arr, current_mapping)
                bind_to_joy(*bind_to_joy_arr)
            elif(controller_mapping == "Xbox 360 Controller"): # TODO: Make this more modular?
                current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                xbox_360_right(selector_position, bind_to_joy_arr, current_mapping)
                bind_to_joy(*bind_to_joy_arr)
            elif(controller_mapping == "Generic"): # TODO: Make this more modular?
                current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                generic_right(selector_position, bind_to_joy_arr, current_mapping)
                bind_to_joy(*bind_to_joy_arr)

    if('ability' in pressed or 'return' in pressed):
        if(player_page == 0):
            input_keys = return_joystick_mapping()

            player_page = (selector_position//4) + 1
            # TODO: Make this work dynamically with shifting lists

            if(selector_position != 3 and selector_position != 7):
                i_ct = 0
                if(selector_position < 3):
                    for i in input_keys['1']:
                        if(selector_position % 4 == i_ct):
                            game_state, controller_mapping = config_menu_func_dict[i](player_page)
                            break
                        i_ct += 1
                else:
                    for i in input_keys['2']:
                        if(selector_position % 4 == i_ct):
                            game_state, controller_mapping = config_menu_func_dict[i](player_page)
                            break
                        i_ct += 1
            else:
                game_state, controller_mapping = config_menu_func_dict[selector_position % 4](player_page)
            if(selector_position != 3):
                selector_position = 0
            else:
                player_page = 0
        else:
            if(controller_mapping == "GameCube Controller Adapter" and selector_position == 10):
                selector_position = 0
                player_page = 0
                controller_mapping = ""
            if(controller_mapping == "Generic" and selector_position == 11):
                selector_position = 0
                player_page = 0
                controller_mapping = ""
            if(controller_mapping == "Xbox 360 Controller" and selector_position == 11):
                selector_position = 0
                player_page = 0
                controller_mapping = ""

    mouse = handle_mouse()
    if(player_page == 0):
        for i in range(len(joy_page_0)):
            if(joy_page_0[i].check_hover(mouse)):
                if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                    selector_position = i # Change the selector position

                if(mouse[1][0] or mouse[1][2]):
                    input_keys = return_joystick_mapping()
                    player_page = (selector_position//4) + 1
                    # TODO: Make this work dynamically with shifting lists

                    if(selector_position != 3 and selector_position != 7):
                        i_ct = 0
                        if(selector_position < 3):
                            for i in input_keys['1']:
                                if(selector_position % 4 == i_ct):
                                    game_state, controller_mapping = config_menu_func_dict[i](player_page)
                                    break
                                i_ct += 1
                        else:
                            for i in input_keys['2']:
                                if(selector_position % 4 == i_ct):
                                    game_state, controller_mapping = config_menu_func_dict[i](player_page)
                                    break
                                i_ct += 1
                    else:
                        game_state, controller_mapping = config_menu_func_dict[selector_position % 4](player_page)
                    if(selector_position != 3):
                        selector_position = 0
                    else:
                        player_page = 0

    elif(controller_mapping == "Xbox 360 Controller"):
        for i in range(len(joy_shift_50)):
            if(joy_shift_50[i].check_hover(mouse)):
                if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                    selector_position = i # Change the selector position

                if(mouse[1][0]):
                    if(selector_position < 11):
                        current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                        bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                        xbox_360_right(selector_position, bind_to_joy_arr, current_mapping)
                        bind_to_joy(*bind_to_joy_arr)
                    else:
                        player_page = 0
                        selector_position = 0
                        controller_mapping = ""
                elif(mouse[1][2]):
                    if(selector_position < 11):
                        current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                        bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                        xbox_360_left(selector_position, bind_to_joy_arr, current_mapping)
                        bind_to_joy(*bind_to_joy_arr)
                    else:
                        player_page = 0
                        selector_position = 0
                        controller_mapping = ""
                    # TODO: Make this work dynamically with shifting lists

    else:
        if(controller_mapping == "GameCube Controller Adapter"):
            l_func = gamecube_controller_left
            r_func = gamecube_controller_right
        else:
            l_func = generic_left
            r_func = generic_right
        for i in range(len(joy_shift_55)):
            if(joy_shift_55[i].check_hover(mouse)):
                if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                    selector_position = i # Change the selector position

                if(mouse[1][0]):
                    if(selector_position < 10):
                        current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                        bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                        r_func(selector_position, bind_to_joy_arr, current_mapping)
                        bind_to_joy(*bind_to_joy_arr)
                    else:
                        player_page = 0
                        selector_position = 0
                        controller_mapping = ""
                elif(mouse[1][2]):
                    if(selector_position < 10):
                        current_mapping = return_joystick_mapping()[str(player_page)][controller_mapping]
                        bind_to_joy_arr = [str(player_page), controller_mapping, None, None] # Player, Mapping, Key, Value
                        l_func(selector_position, bind_to_joy_arr, current_mapping)
                        bind_to_joy(*bind_to_joy_arr)
                    else:
                        player_page = 0
                        selector_position = 0
                        controller_mapping = ""
                    # TODO: Make this work dynamically with shifting lists


    return game_state, [player_page, selector_position, controller_mapping]