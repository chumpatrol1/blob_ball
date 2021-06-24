import pygame as pg
import resources.display_graphics as dg
import sys
done = False
pg.init()

def display_graphics():
    dg.handle_graphics()

def run():
    global done
    display_graphics()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pressed = pg.key.get_pressed()
    if(pressed[pg.K_ESCAPE]):
        pg.quit()
        sys.exit()
        done = True #Ends the game
    '''Runs the program'''

while not done:
    run()
else:
    print("All done!")