import pygame as pg
import sys
import os

pg.init()
#clock = pg.time.Clock()
#clock.tick(120)

input_map = {
    'p1_up': pg.K_UP,
    'p1_down': pg.K_DOWN,
    'p1_left': pg.K_LEFT,
    'p1_right': pg.K_RIGHT,
    'p1_ability': pg.K_n,
    'p1_kick': pg.K_m,
    'p1_block': pg.K_COMMA,
    'p1_boost': pg.K_PERIOD,
    'p2_up': pg.K_w,
    'p2_down': pg.K_s,
    'p2_left': pg.K_a,
    'p2_right': pg.K_d,
    'p2_ability': pg.K_1,
    'p2_kick': pg.K_2,
    'p2_block': pg.K_3,
    'p2_boost': pg.K_4
}

def bind_inputs(controls, input_map):
    pass

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
    if(button_timer == 0 and selected):
        print("PRESSED!")
        button_timer = 30
        return pressed
    elif(button_timer == 0 and not pressed == []):
        button_timer = 5
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

if(button_timer > 0):
    button_timer -= 1

def player_to_controls(player):
    if(player == 1):
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
    else:
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
    return button_list


def gameplay_input():
    pressed = get_keypress()
    return pressed

if "__name__" == "__main__":
    while True:
        get_keypress