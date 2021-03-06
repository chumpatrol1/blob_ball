'''
INSTRUCTIONS FOR EVERY RELEASE
Update Game Stats Version (initializer.py)
Update Setup.py Game Version
python setup.py bdist_msi
Install the Game
Add Missing Resources/Files
Update the Changelog
ZIP the files together for release!
'''

# COMMAND TO RUN THE GAME IN NOTEPAD ++: D:\Python\python.exe -i "$(FULL_CURRENT_PATH)"

'''OPTIMIZING'''
#python -m cProfile -o out.prof main.py
#snakeviz out.prof
'''CREATING AN INSTALLER'''
#python setup.py bdist_msi

import os

from engine.get_events import update_events

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

os.chdir(get_script_path())
cwd = os.getcwd()
print("MAIN",cwd)

import pygame as pg
from engine.initializer import check_folders, initialize_ruleset, initialize_game_stats, load_matchup_chart, check_existing_directory
check_existing_directory(cwd)
from engine.game_handler import update_game_state as ugs
import resources.graphics_engine.display_graphics as dg
import resources.sound_engine.handle_sound as hs
import engine.handle_input
from engine.handle_input import detect_joysticks, get_keypress
from json import loads, dumps
import time
from engine.unlocks import load_blob_unlocks, update_costumes, update_css_blobs, load_medal_unlocks, update_css_medals, load_costume_unlocks
game_state = "control_splash"
new_game_state = "control_splash"

check_folders(cwd)
game_stats = initialize_game_stats(cwd)
initialize_ruleset(cwd)
load_matchup_chart(cwd)

load_blob_unlocks(cwd)
load_medal_unlocks(cwd)
load_costume_unlocks(cwd)
update_css_blobs(cwd)
update_costumes()

done = False

with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
    game_stats['times_bb_started'] += 1
    start_time = time.time()
    statsdoc.write(dumps(game_stats))


def handle_input():
    engine.handle_input.get_keypress()

def get_game_state(game_state, cwd):
    return ugs(game_state, cwd)

def display_graphics(game_state, cwd, info_getter, settings):
    dg.handle_graphics(game_state, cwd, info_getter, settings)

def handle_sound(game_state, settings):
    hs.handle_sound(game_state, settings)

clock = pg.time.Clock()
escape_timer = 0
def run(game_state):
    global done
    global clock
    global cwd
    global escape_timer
    events = update_events()
    clock.tick_busy_loop(60)

    for event in events:
        if event.type == pg.QUIT:
            done = True
    detect_joysticks()
    #handle_input()
    new_game_state, info_getter, bgm_song, settings, ruleset = get_game_state(game_state, cwd)
    display_graphics(game_state, cwd, info_getter, settings) # Graphics always lag behind by a single frame
    # Why did I write it this way?
    handle_sound(bgm_song, settings)
    game_state = new_game_state
    pressed = get_keypress(detect_new_controllers = False)
    if('escape' in pressed and not escape_timer):
        if(game_state in {"casual_match", "pause", "css", "replay_match", "replay_pause"}):
            escape_timer = 30
        elif(game_state == "rebind"):
            #game_state = "settings"
            escape_timer = 30
        else:
            done = True #Ends the game
    if(escape_timer):
        escape_timer -= 1
    if(game_state == "quit"):
        done = True
    '''Runs the program'''
    return game_state
try:
    while not done:
        game_state = run(game_state)
    else:
        print("All done!")
        with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
                game_stats = loads(statsdoc.readline())
        with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
                game_stats['time_open'] = game_stats['time_open'] + round(time.time() - start_time)
                statsdoc.write(dumps(game_stats))
        pg.quit()
        from sys import exit
        exit()


except Exception as ex:
    '''
    Error handling. If the game crashes after loading it will leave a crash log
    '''
    import logging
    logging.basicConfig(filename = cwd + "/crash_logs.log", level = logging.ERROR,\
        format='%(process)d-%(levelname)s-%(message)s')
    #Debug, Info, Warning, Error, Critical
    from engine.initializer import return_game_version
    from engine.game_handler import return_blobs
    logging.error(f"Game Crash at {time.asctime()} (Version {return_game_version()})", exc_info=True)
    with open(cwd + "/crash_logs.log", 'a') as crash_logs:
        crash_logs.write("Game State: " + game_state + "\n")
        blob_info = return_blobs()
        crash_logs.write("P1 Blob: " + str(blob_info[0]) + ", is CPU: " + str(bool(blob_info[2])) + "\n")
        crash_logs.write("P2_Blob: " + str(blob_info[1]) + ", is CPU: " + str(bool(blob_info[3])) + "\n")
        crash_logs.write("\n")
        crash_logs.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        crash_logs.write("\n")
    print("GAME CRASH! Please check crash_logs.log and send them to the Blob Ball Devs")

    pg.quit()
    from sys import exit
    exit()
