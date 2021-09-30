'''
INSTRUCTIONS FOR EVERY RELEASE
Update Game Stats Version
Update Setup.py Game Version
python setup.py bdist_msi
Install the Game
Add Missing Resources/Files
Update the Changelog
ZIP the files together for release!
'''

'''OPTIMIZING'''
#python -m cProfile -o out.prof main.py
#snakeviz out.prof
'''CREATING AN INSTALLER'''
#python setup.py bdist_msi

from engine.gameplay import handle_gameplay
import os
from sys import argv
#COMMENT THIS OUT WHEN MAKING THE EXE
#os.chdir(os.path.dirname(argv[0]))

cwd = os.getcwd()
print("MAIN",cwd)

import pygame as pg
from engine.game_handler import update_game_state as ugs
import resources.graphics_engine.display_graphics as dg
import resources.sound_engine.handle_sound as hs
import sys
import engine.handle_input
from json import loads, dumps
import time
game_state = "main_menu"
new_game_state = "main_menu"

done = False

game_stats = {
    #Stats about the state of the game
    'original_version': 'v0.7.2b', #Version this file was created on
    'times_bb_started': 0, #Number of times Blob Ball was started up
    'time_open': 0, #Time in seconds.mm that the game has been open
    'time_in_game': 0, #Time in seconds.mm that was spent in an actual match
    'blobs_unlocked': 1, #Number of blobs unlocked
    'costumes_unlocked': 0, #Number of costumes unlocked
    'backgrounds_unlocked': 0, #Number of backgrounds unlocked
    'most_played_character': 'quirkless', #Most played character

    #Stats about game/match info
    'matches_played': 0, #Number of matches completed
    'points_scored': 0, #Total points scored (should be sum of bottom 2)
    'points_from_goals': 0, #Total points scored from kicking the ball into the goal
    'points_from_kos': 0, #Total points scored from kills

    #Stats relating directly to blobs
    'damage_dealt': 0, #Total damage accumulated
    'kick_count': 0, #Total amount of times the kick button was pressed
    'block_count': 0, #Total amount of times the block button was pressed
    'boost_count': 0, #Total amount of times the boost button was pressed
    'parries': 0, #Total number of kicks or attacks deflected by blocks
    'clanks': 0, #Total numbers of kicks deflected by other kicks
    'blob_x_distance_moved': 0, #Total distance moved by blobs
    'wavebounces': 0, #Total wavebounces performed
    'jumps': 0, #Total jumps
    'jump_cancelled_focuses': 0, #Total focuses cancelled by jumps
    'time_focused_seconds': 0, #Total time spent focusing
    'time_airborne_seconds': 0, #Total time spent in the air
    'time_grounded_seconds': 0, #Total time spent on the ground

    'blob_standard_collisions': 0, #Normal ball collisions (hitting the top)
    'blob_reflect_collisions': 0, #Reflecting ball collisions (hitting the bottom)
    'blob_warp_collisions': 0, #Warp ball collisions (ball warps above the blob)
    'ball_kicked': 0, #Times hit with a kick
    'ball_blocked': 0, #Times hit with a block
    'ball_x_distance_moved': 0, #Distance moved horizontally
    'ball_y_distance_moved': 0, #Distance moved vertically
    'ball_wall_collisions': 0, #Hitting a wall
    'ball_ceiling_collisions': 0, #Hitting the ceiling
    'ball_floor_collisions': 0, #Bouncing off of the floor specifically
    'ball_goal_collisions': 0, #Goalpost collisions
        }

try:
    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
        game_stats = loads(statsdoc.readline())
except:
    try:
        with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
            statsdoc.write(dumps(game_stats))
            print("Not OK!")
    except:
        os.mkdir(cwd+"/saves")
        print("Made new directory!")
        with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
            statsdoc.write(dumps(game_stats))
            print("Not OK!")

try:
    with open(cwd+'/saves/matchup_chart.txt', 'r') as statsdoc:
        print("Sucessfully Opened MU Chart")
except:
     with open(cwd+'/saves/matchup_chart.txt', 'w') as statsdoc:
            statsdoc.write(dumps({}))
            print("Created MU Chart")
with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
    game_stats['times_bb_started'] += 1
    start_time = time.time()
    statsdoc.write(dumps(game_stats))


def handle_input():
    engine.handle_input.get_keypress()

def get_game_state(game_state, cwd):
    return ugs(game_state, cwd)

def display_graphics(game_state, cwd, info_getter):
    dg.handle_graphics(game_state, cwd, info_getter)

def handle_sound(game_state):
    hs.handle_sound(game_state)

clock = pg.time.Clock()
def run():
    global done
    global clock
    global game_state
    global cwd
    clock.tick_busy_loop(60)
    handle_input()
    new_game_state, info_getter, bgm_song = get_game_state(game_state, cwd)
    display_graphics(game_state, cwd, info_getter)
    handle_sound(bgm_song)
    game_state = new_game_state
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pressed =  pg.key.get_pressed()
    if(pressed[pg.K_ESCAPE]):
        done = True #Ends the game
    if(game_state == "quit"):
        done = True
        
    '''Runs the program'''
    return game_state

while not done:
    game_state = run()
else:
    print("All done!")
    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())
    with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
            game_stats['time_open'] = game_stats['time_open'] + round(time.time() - start_time)
            statsdoc.write(dumps(game_stats))
    pg.quit()
    sys.exit()
        