'''
main.py

File used to open the rest of the game. Contains the game loop and handles the crash logs.

> get_script_path(): Changes the current working directory for use in os.getcwd() calls throughout the script
> run(): The game loop that runs every frame
> exception block: Opens crash_logs.log and outputs data based on what caused the crash
'''

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
cwd = os.getcwd()
appcwd = os.getenv('APPDATA')+'/BlobBall'
from engine.initializer import check_folders, initialize_ruleset, initialize_game_stats, load_matchup_chart, check_existing_directory
check_existing_directory(appcwd)

from engine.get_events import update_events
from engine.rebind import reset_rebind
from engine.tutorial import reset_tutorial
from resources.graphics_engine.display_gameplay import unload_image_cache
from resources.graphics_engine.display_particles import clear_particle_memory


def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

os.chdir(get_script_path())

print("MAIN",cwd)

import pygame as pg
from engine.game_handler import update_game_state as ugs
import resources.graphics_engine.display_graphics as dg
import resources.sound_engine.handle_sound as hs
import engine.handle_input
from engine.handle_input import detect_joysticks, get_keypress
from json import loads, dumps
import time
from engine.unlocks import load_blob_unlocks, update_costumes, update_css_blobs, load_medal_unlocks, update_mam_medals, load_costume_unlocks
game_state = "control_splash"
new_game_state = "control_splash"

check_folders(appcwd)
game_stats = initialize_game_stats(appcwd)
initialize_ruleset(appcwd)
load_matchup_chart(appcwd)

load_blob_unlocks(appcwd)
load_medal_unlocks(appcwd)
load_costume_unlocks(appcwd)
update_css_blobs(appcwd)
update_costumes()

done = False

with open(appcwd+'/saves/game_stats.txt', 'w') as statsdoc:
    game_stats['times_bb_started'] += 1
    start_time = time.time()
    statsdoc.write(dumps(game_stats))

clock = pg.time.Clock()
escape_timer = 0
def run(game_state):
    '''
    Runs the game, calling the essential functions to handle gameplay, display and sound.

    Inputs:
        - game_state: The current game state, or screen that we're on (such as the main menu, character select, etc.)
        - done (global): Global variable that determines whether or not the game loop will run.
        - clock (global): Locks the game's frame rate at 60 fps
        - cwd (global): The working directory, allowing the game to open files and resources.
        - escape_timer (global): Timer that prevents escape from being spammed and accidentally closing the game

    Outputs:
        - game_state (global): Updates every frame to use in the next
        - done (global): If this is set to True, the game will quit
        - dg.handle_graphics(): Displays graphics
        - hs.handle_sound(): Handles SFX and BGM
    '''
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
    # Having things lag behind a frame is a weird design decision - why did I write it this way?
    new_game_state, info_getter, bgm_song, settings, ruleset = ugs(game_state, cwd)
    dg.handle_graphics(game_state, cwd, info_getter, settings) # Graphics always lag behind by a single frame
    hs.handle_sound(game_state, settings)
    game_state = new_game_state
    pressed = get_keypress(detect_new_controllers = False)
    if('escape' in pressed and not escape_timer):
        if(game_state in {"casual_match", "pause", "css", "replay_match", "replay_pause"}):
            escape_timer = 30
        elif(game_state == "tutorial"):
            escape_timer = 30
            game_state = "main_menu"
            clear_particle_memory()
            unload_image_cache()

            reset_tutorial()
        elif(game_state == "rebind"):
            reset_rebind()
            game_state = "settings"
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
        with open(appcwd+'/saves/game_stats.txt', 'r') as statsdoc:
                game_stats = loads(statsdoc.readline())
        with open(appcwd+'/saves/game_stats.txt', 'w') as statsdoc:
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
