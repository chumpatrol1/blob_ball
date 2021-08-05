#python -m cProfile -o out.prof main.py
#snakeviz out.prof

import os
from sys import argv
os.chdir(os.path.dirname(argv[0]))
cwd = os.getcwd()
print("MAIN",cwd)

import pygame as pg
import resources.display_graphics as dg
import sys
import engine.handle_input

game_state = "main_menu"

done = False

def handle_input():
    engine.handle_input.get_keypress()

def display_graphics(game_state, cwd):
    game_state = dg.handle_graphics(game_state, cwd)
    return game_state

clock = pg.time.Clock()
def run():
    global done
    global clock
    global game_state
    global cwd
    clock.tick_busy_loop(60)
    handle_input()
    game_state = display_graphics(game_state, cwd)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pressed =  pg.key.get_pressed()
    if(pressed[pg.K_ESCAPE]):
        pg.quit()
        sys.exit()
        done = True #Ends the game
    '''Runs the program'''
    return game_state

while not done:
    game_state = run()
else:
    print("All done!")