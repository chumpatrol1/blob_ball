def set_timer(frames):
    global timer
    timer = frames

from engine.initializer import initialize_ruleset, initialize_settings
import engine.menus.main_menu
from os import getcwd
cwd = getcwd()

ruleset = initialize_ruleset(cwd)
settings = initialize_settings(cwd)

timer = 0
previous_screen = ""
p1_blob = []
p2_blob = []
p1_is_cpu = False
p2_is_cpu = False
game_stats = []
def update_game_state(game_state, cwd):
    global timer
    global previous_screen
    global p1_blob
    global p2_blob
    global p1_is_cpu
    global p2_is_cpu
    global ruleset
    global settings
    global game_stats
    song_playing = "bb_main_theme"

    if(timer > 0):
            timer -= 1

    if(game_state == "control_splash"):
        info_getter, game_state = engine.menus.main_menu.splash_navigator()
        if(game_state != "control_splash"):
            timer = 10
    elif(game_state == "main_menu"):
        game_state, info_getter = engine.menus.main_menu.menu_navigation(timer)
        info_getter += [ruleset]
        if(game_state == "rules" or game_state == "settings" or game_state == "almanac"):
            previous_screen = "main_menu" 
    return game_state, info_getter, song_playing, settings, ruleset

def return_blobs():
    return p1_blob, p2_blob, p1_is_cpu, p2_is_cpu