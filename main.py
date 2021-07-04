import os

print(os.chdir(os.path.dirname(os.path.abspath(__file__))))
cwd = os.getcwd()
print("MAIN",cwd)

import pygame as pg
import resources.display_graphics as dg
import sys
import engine.handle_input

game_state = "main_menu"

done = False
pg.init()
clock = pg.time.Clock()
clock.tick(60)

def handle_input():
    controls = open(cwd+"\\engine\\controls.txt", "r+")
    engine.handle_input.get_keypress()

def display_graphics(game_state, cwd):
    game_state = dg.handle_graphics(game_state, cwd)
    return game_state

def run():
    global done
    global game_state
    global cwd
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