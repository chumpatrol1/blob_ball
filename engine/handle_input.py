import pygame as pg
import sys
from os import getcwd
from json import loads, dumps

from pygame.constants import K_KP_ENTER
from resources.graphics_engine.handle_screen_size import return_mouse_wh
from resources.sound_engine.sfx_event import createSFXEvent

#print(tuple(filter(lambda x: x.startswith("K_"), pg.constants.__dict__.keys())))

pg.init()
#clock = pg.time.Clock()
#clock.tick(120)

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


forbidden_keys = [pg.K_ESCAPE, pg.K_LCTRL, pg.K_RCTRL, pg.K_RETURN]

input_map = loads(controls.readlines()[0])

update_mapkey_names(input_map)

def unbind_inputs():
    global input_map
    for button in input_map:
        input_map[button] = 0

temp_binding = []

def bind_input(key_to_rebind):
    global input_map
    global temp_binding
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if(not event.key in temp_binding and not event.key in forbidden_keys):
                input_map[key_to_rebind] = event.key
                temp_binding.append(event.key)
                update_mapkey_names(temp_binding, key=key_to_rebind)
                if(key_to_rebind == "p2_boost"):
                    temp_binding = []
                    with open(getcwd()+"/config/controls.txt", "w") as control_list:
                        
                        control_list.write(dumps(input_map))
                    createSFXEvent('chime_completion')
                else:
                    createSFXEvent('chime_progress')
                return True
            else:
                createSFXEvent('chime_error')
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

def get_keypress():
    global input_map
    pressed = pg.key.get_pressed()
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
    return pressed_array

def merge_inputs(pressed):
    global button_timer
    merged_press = []
    if not button_timer:
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
    if(len(merged_press)):
        button_timer = 10
    return merged_press
button_timer = 0

def menu_input():
    global button_timer
    pressed = get_keypress()
    selected = False
    if("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed):
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
def css_input():
    global button_timer
    if(button_timer == 0):
        return get_keypress()
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

def toggle_fullscreen():

    pressed = pg.key.get_pressed()
    if(pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]):
        return True
    else:
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