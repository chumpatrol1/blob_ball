import pygame as pg
import sys
from os import getcwd
from json import loads, dumps

from pygame.constants import K_KP_ENTER
from engine.get_events import get_events
from resources.graphics_engine.handle_screen_size import return_mouse_wh
from resources.sound_engine.sfx_event import createSFXEvent

#print(tuple(filter(lambda x: x.startswith("K_"), pg.constants.__dict__.keys())))

pg.init()

# DEFAULT KEYBOARD CONTROLS

input_map = {
    'p1_up': pg.K_w,
    'p1_down': pg.K_s,
    'p1_left': pg.K_a,
    'p1_right': pg.K_d,
    'p1_ability': pg.K_1,
    'p1_kick': pg.K_2,
    'p1_block': pg.K_3,
    'p1_boost': pg.K_4,
    'p2_up': pg.K_UP,
    'p2_down': pg.K_DOWN,
    'p2_left': pg.K_LEFT,
    'p2_right': pg.K_RIGHT,
    'p2_ability': pg.K_n,
    'p2_kick': pg.K_m,
    'p2_block': pg.K_COMMA,
    'p2_boost': pg.K_PERIOD,
}

# DEFAULT GAMECUBE CONTROLS - converts button press to an action

gamecube_map = {
    'horizontal_deadzone': 0.3,
    'vertical_deadzone': 0.3,
    'bumper_deadzone': 0.3,
    'rumble': True,
    0: 'up', # X
    1: 'ability', # A
    2: 'kick', # B
    3: 'down', # Y
    4: 'block', # L
    5: 'block', # R
    6: '',
    7: 'boost', # Z
    8: '',
    9: 'escape', # HOME
    10: '',
}

xbox360_map = {

}

ps3_map = {

}

ps4_map = {

}

switchpro_map = {

}

player_mapping = {
    'GameCube Controller Adapter': dict(gamecube_map),
    'Generic': dict(gamecube_map),
}

joystick_mapping = {
    1: dict(player_mapping),
    2: dict(player_mapping),
}

mapkey_names = {}
override = {
    '.': 'PERIOD',
    ',': 'COMMA',
    '/': 'FORWARDSLASH',
    ';': 'SEMICOLON',
    '\'': 'SINGLEQUOTE',
    '\\': 'BACKSLASH',
    '[': 'OPENBRACKET',
    ']': 'CLOSEBRACKET',
    '-': 'SUBTRACT',
    '=': 'EQUALS',
}
def update_mapkey_names(input_list, key = None):
    global mapkey_names
    global override
    if(key is None):
        for mapkey in input_list:
            key_name = pg.key.name(input_list[mapkey]).upper()
            if key_name in override:
                mapkey_names[mapkey] = override[key_name]
            else:
                mapkey_names[mapkey] = key_name
            
    else:
        key_name = pg.key.name(input_list[-1]).upper()
        if key_name in override:
            mapkey_names[key] = override[key_name]
        else:
            mapkey_names[key] = key_name

def return_mapkey_names():
    global mapkey_names
    return mapkey_names

try:
    controls = open(getcwd()+"/config/controls.txt", "r+")
except:
    with open(getcwd()+"/config/controls.txt", "w") as controls:
        controls.write(dumps(input_map))
    controls = open(getcwd()+"/config/controls.txt", "r+")

try:
    n_joystick_mapping = open(getcwd()+"/configs/joysticks.txt", "r+")
    for key in joystick_mapping:
            if not key in n_joystick_mapping:
                n_joystick_mapping[key] = joystick_mapping[key]
            else:
                for joy_button in n_joystick_mapping[key]:
                    if not joy_button in n_joystick_mapping[key]:
                        n_joystick_mapping[key][joy_button] = joystick_mapping[key][joy_button]
    joystick_mapping = n_joystick_mapping
except:
    with open(getcwd()+"/config/joysticks.txt", "w") as joystick_file:
        joystick_file.write(dumps(joystick_mapping))
    joystick_mapping = open(getcwd()+"/config/joysticks.txt", "r+")

forbidden_keys = [pg.K_ESCAPE, pg.K_LCTRL, pg.K_RCTRL, pg.K_RETURN]

input_map = loads(controls.readlines()[0])
joystick_map = loads(joystick_mapping.readlines()[0])

def return_joystick_mapping():
    global joystick_map
    return joystick_map

update_mapkey_names(input_map)

temp_binding = []

joysticks = []
joystick_count = 0
joystick_handler = {
    'p1_joystick': None,
    'p2_joystick': None,
}

def detect_joysticks():
    global joysticks
    global joystick_count
    for event in get_events():
        #print(event)
        #print(pg.JOYDEVICEADDED)
        if(event.type == pg.JOYDEVICEADDED):
            print("OK")
            joysticks.append(pg.joystick.Joystick(joystick_count))
            joysticks[joystick_count].init()
            joystick_count += 1
        elif(event.type == pg.JOYDEVICEREMOVED):
            print("SADGE")
            joystick_count -= 1
            joysticks[joystick_count].quit()
            joysticks.pop(joystick_count)
            

def unbind_inputs(mode = 'all'):
    global input_map
    global temp_binding
    print("MODE", mode)
    if(mode == 'p1'):
        for button in input_map:
            if 'p1' in button:
                input_map[button] = 0
        
        for key in input_map:
            if 'p2' in key:
                temp_binding.append(input_map[key])

    elif(mode == 'p2'):
        for button in input_map:
            if 'p2' in button:
                input_map[button] = 0
        
        for key in input_map:
            if 'p1' in key:
                temp_binding.append(input_map[key])
    

    elif(mode == 'all'):
        for button in input_map:
            input_map[button] = 0
    
    else:
        input_map[mode] = 0
        print(input_map)
        for key in input_map:
            print(key)
            if(key != mode):
                temp_binding.append(input_map[key])

def bind_input(key_to_rebind, last_key):
    global input_map
    global temp_binding
    for event in get_events():
        if event.type == pg.KEYDOWN:
            if(not event.key in temp_binding and not event.key in forbidden_keys):
                input_map[key_to_rebind] = event.key
                temp_binding.append(event.key)
                update_mapkey_names(temp_binding, key=key_to_rebind)
                print(temp_binding)
                if(key_to_rebind == last_key):
                    temp_binding = []
                    with open(getcwd()+"/config/controls.txt", "w") as control_list:
                        control_list.write(dumps(input_map))
                else:
                    createSFXEvent('chime_progress')
                return True
            else:
                return False
    else:
        return False

def reset_inputs():
    global input_map
    input_map = {
    'p1_up': pg.K_w,
    'p1_down': pg.K_s,
    'p1_left': pg.K_a,
    'p1_right': pg.K_d,
    'p1_ability': pg.K_1,
    'p1_kick': pg.K_2,
    'p1_block': pg.K_3,
    'p1_boost': pg.K_4,
    'p2_up': pg.K_UP,
    'p2_down': pg.K_DOWN,
    'p2_left': pg.K_LEFT,
    'p2_right': pg.K_RIGHT,
    'p2_ability': pg.K_n,
    'p2_kick': pg.K_m,
    'p2_block': pg.K_COMMA,
    'p2_boost': pg.K_PERIOD,
    }
    update_mapkey_names(input_map)
    with open(getcwd()+"/config/controls.txt", "w") as control_list:
                    control_list.write(dumps(input_map))

def get_keypress(detect_new_controllers = True):
    global input_map
    pressed = pg.key.get_pressed()
    events = get_events()
    pressed_array = []
    if(pressed[input_map['p1_up']]):
        pressed_array.append('p1_up')
    if(pressed[input_map['p1_down']]):
        pressed_array.append('p1_down')
    if(pressed[input_map['p1_left']]):
        pressed_array.append('p1_left')
    if(pressed[input_map['p1_right']]):
        pressed_array.append('p1_right')
    if(pressed[input_map['p1_ability']]):
        pressed_array.append('p1_ability')
    if(pressed[input_map['p1_kick']]):
        pressed_array.append('p1_kick')
    if(pressed[input_map['p1_block']]):
        pressed_array.append('p1_block')
    if(pressed[input_map['p1_boost']]):
        pressed_array.append('p1_boost')
    if(pressed[input_map['p2_up']]):
        pressed_array.append('p2_up')
    if(pressed[input_map['p2_down']]):
        pressed_array.append('p2_down')
    if(pressed[input_map['p2_left']]):
        pressed_array.append('p2_left')
    if(pressed[input_map['p2_right']]):
        pressed_array.append('p2_right')
    if(pressed[input_map['p2_ability']]):
        pressed_array.append('p2_ability')
    if(pressed[input_map['p2_kick']]):
        pressed_array.append('p2_kick')
    if(pressed[input_map['p2_block']]):
        pressed_array.append('p2_block')
    if(pressed[input_map['p2_boost']]):
        pressed_array.append('p2_boost')
    if(pressed[pg.K_RETURN]):
        pressed_array.append('return')
    if(pressed[pg.K_ESCAPE]):
        pressed_array.append('escape')
    
    # Handle Joystick Events
    # TODO: Create popup when connecting a new controller
    for event in events:
        if(event.type in {pg.JOYAXISMOTION, pg.JOYHATMOTION}):

            #print(event)
            #print(joysticks[event.__dict__['joy']].get_button(2))
            pass
        elif(event.type == pg.JOYBUTTONDOWN):
            #print(event)
            # Left on DPAD
            new_controller = joysticks[event.__dict__['joy']].get_instance_id() - 1
            if(joysticks[event.__dict__['joy']].get_button(15) and detect_new_controllers):
                old_joystick = joystick_handler['p1_joystick']
                if(joystick_handler['p1_joystick'] == None):
                    joystick_handler['p1_joystick'] = new_controller
                    if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                        joystick_handler['p2_joystick'] = None
                else:
                    if(new_controller != old_joystick):
                        joystick_handler['p1_joystick'] = new_controller
                        if(new_controller == joystick_handler['p2_joystick'] or joystick_handler['p2_joystick'] == None):
                            joystick_handler['p2_joystick'] = old_joystick
                print(joystick_handler)
                print("Assigned joystick to P1")
                #print(joystick_handler)
            # Right on DPAD
            elif(joysticks[event.__dict__['joy']].get_button(13) and detect_new_controllers):    
                #print("test r passed")
                old_joystick = joystick_handler['p2_joystick']
                if(joystick_handler['p2_joystick'] == None):
                    joystick_handler['p2_joystick'] = new_controller
                    if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                        joystick_handler['p1_joystick'] = None
                else:
                    if(new_controller != old_joystick):
                        joystick_handler['p2_joystick'] = new_controller
                        if(new_controller == joystick_handler['p1_joystick'] or joystick_handler['p1_joystick'] == None):
                            joystick_handler['p1_joystick'] = old_joystick
                print(joystick_handler)
                print("Assigned joystick to P2")
                #print(joystick_handler)
            else:
                pass
                #print(joystick_handler)
                #print(new_controller)

            if(joysticks[event.__dict__['joy']].get_button(14)): # Down on DPAD
                pressed_array.append('return')

        
    for joystick in joysticks:
        header = ""
        if(joystick.get_instance_id() - 1 == joystick_handler['p1_joystick']):
            header = "p1_"
        elif(joystick.get_instance_id() - 1 == joystick_handler['p2_joystick']):
            header = "p2_"
        else:
            continue
        
        # Control Stick
        # TODO: Deadzone updates
        # TODO: C-Stick Attack
        if(joystick.get_axis(0) > 0.3):
            #print("Holding Right")
            pressed_array.append(header + "right")
        elif(joystick.get_axis(0) < -0.3):
            #print("Holding Left")
            pressed_array.append(header + "left")

        if(joystick.get_axis(1) > 0.3):
            #print("Holding Down")
            pressed_array.append(header + "down")
        elif(joystick.get_axis(1) < -0.3):
            #print("Holding Up")
            pressed_array.append(header + "up")

        # TODO: Rebindable buttons
        # Buttons
        if(joystick.get_button(2)): # GC B
            pressed_array.append(header + "kick")
        
        if(joystick.get_button(1)): # GC A 
            pressed_array.append(header + "ability")

        if(joystick.get_button(7)): # GC Z
            pressed_array.append(header + "block")

        if(joystick.get_button(0) or joystick.get_button(3)): # GC X Y
            pressed_array.append(header + "boost")

        if(joystick.get_button(9)): # GC Home Button
            pressed_array.append('escape')
        
        # TODO: Shoulder buttons/triggers
        

        
    
    #print(joysticks)
    #print(joysticks[3].get_button(9))
    return pressed_array
button_timer = 0
def merge_inputs(pressed, override = False):
    global button_timer
    merged_press = []
    if not button_timer or override:
        if('p1_up' in pressed or 'p2_up' in pressed):
            merged_press.append('up')
        if('p1_down' in pressed or 'p2_down' in pressed):
            merged_press.append('down')
        if('p1_left' in pressed or 'p2_left' in pressed):
            merged_press.append('left')
        if('p1_right' in pressed or 'p2_right' in pressed):
            merged_press.append('right')
        if('p1_ability' in pressed or 'p2_ability' in pressed):
            merged_press.append('ability')
        if('p1_kick' in pressed or 'p2_kick' in pressed):
            merged_press.append('kick')
        if('return' in pressed):
            merged_press.append('return')
    if(len(merged_press)):
        button_timer = 10
    return merged_press

def menu_input(pause_screen = False):
    global button_timer
    pressed = get_keypress()
    selected = False
    if(not pause_screen and ("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed)):
        selected = True
    elif(pause_screen and "return" in pressed):
        selected = True
    if(pressed == []):
        button_timer = 0
    if(button_timer == 0 and selected):
        button_timer = 30
        return pressed
    elif(button_timer == 0 and not pressed == []):
        button_timer = 15
        return pressed
    else:
        if(button_timer > 0):
            button_timer -= 1
        return []

p1_timer = 0
p2_timer = 1
def css_input(detect_new_controllers = True):
    global button_timer
    if(button_timer == 0):
        return get_keypress(detect_new_controllers = detect_new_controllers)
    else:
        button_timer -= 1
        return []

def player_to_controls(player):
    if(player == 2):
        button_list = {
            'p2_up': 'up',
            'p2_down': 'down',
            'p2_left': 'left',
            'p2_right': 'right',
            'p2_ability': 'ability',
            'p2_kick': 'kick',
            'p2_block': 'block',
            'p2_boost': 'boost'
        }
    else:
        button_list = {
            'p1_up': 'up',
            'p1_down': 'down',
            'p1_left': 'left',
            'p1_right': 'right',
            'p1_ability': 'ability',
            'p1_kick': 'kick',
            'p1_block': 'block',
            'p1_boost': 'boost'
        }
    return button_list

def toggle_fullscreen(force_override = False): # TODO: Override so it works with the settings menu
    
    pressed = pg.key.get_pressed()
    events = get_events()
    if(pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]):
        return True
    
    for event in events:
        if(event.type == pg.JOYBUTTONDOWN):
            # Up on DPAD
            if(joysticks[event.__dict__['joy']].get_button(12)):
                return True

    if(force_override):
        return True

    return False

def gameplay_input():
    pressed = get_keypress()
    return pressed

was_pressed = [0, 0, 0]
prev_coords = [0, 0]
def handle_mouse(update = True):
    # What the mouse should give us:
    # Get Pos returns 2 value tuple (X, Y)
    # Get Pressed returns 3 value tuple (L, M, R)
    global was_pressed
    global prev_coords
    screen_size = return_mouse_wh()
    mouse_pos = list(pg.mouse.get_pos())
    mouse_pos[0] = mouse_pos[0] * (1366/screen_size[0])
    mouse_pos[1] = mouse_pos[1] * (768/screen_size[1])

    get_pressed = pg.mouse.get_pressed()
    return_pressed = [0, 0, 0]
    for i in range(len(was_pressed)): # This whole thing is a fancy mouse key up function
        if(was_pressed[i] and not get_pressed[i]):
            return_pressed[i] = was_pressed[i]
    
    moved_mouse = True
    if(prev_coords == mouse_pos):
        moved_mouse = False

    if(update):
        was_pressed = get_pressed
        prev_coords = mouse_pos

    return mouse_pos, return_pressed, moved_mouse

if "__name__" == "__main__":
    while True:
        get_keypress