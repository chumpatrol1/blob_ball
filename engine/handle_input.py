import pygame as pg
import sys
import os

pg.init()
clock = pg.time.Clock()
clock.tick(120)

input_map = {
    'p1_up': pg.K_UP,
    'p1_down': pg.K_DOWN,
    'p1_left': pg.K_LEFT,
    'p1_right': pg.K_RIGHT,
    'p1_ability': pg.K_m,
    'p1_kick': pg.K_n,
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
    return pressed_array

button_timer = 0
button_timer_2 = 0

def menu_input():
    global button_timer
    pressed = get_keypress()
    if(button_timer == 0):
        button_timer = 1
        return pressed
    elif(button_timer == 1 and pressed == []):
        button_timer = 0
        return pressed
    else:
        button_timer = 1
        return []

def css_input():
    global button_timer
    pressed = get_keypress()
    if(button_timer == 0):
        button_timer = 1
        return pressed
    elif(button_timer == 1 and pressed == []):
        button_timer = 0
        return pressed
    else:
        button_timer = 0
        return []
        


if "__name__" == "__main__":
    while True:
        get_keypress