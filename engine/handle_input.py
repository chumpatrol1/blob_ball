import pygame as pg
import sys
from os import getcwd
from json import loads, dumps

pg.init()
#clock = pg.time.Clock()
#clock.tick(120)
controls = open(getcwd()+"\\engine\\controls.txt", "r+")
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

input_map = loads(controls.readlines()[0])

def unbind_inputs():
    global input_map
    for button in input_map:
        input_map[button] = 0

def bind_input(key_to_rebind):
    global input_map
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and not event.key in input_map.values():
            input_map[key_to_rebind] = event.key
            if(key_to_rebind == "p2_boost"):
                with open(getcwd()+"\\engine\\controls.txt", "w") as control_list:
                    control_list.write(dumps(input_map))
            return True
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
    with open(getcwd()+"\\engine\\controls.txt", "w") as control_list:
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
    return pressed_array

button_timer = 0

def menu_input():
    global button_timer
    pressed = get_keypress()
    selected = False
    if("p1_ability" in pressed or "p2_ability" in pressed):
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


def gameplay_input():
    pressed = get_keypress()
    return pressed

if "__name__" == "__main__":
    while True:
        get_keypress