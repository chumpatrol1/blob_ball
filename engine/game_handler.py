'''
engine/game_handler.py

Updates the game state and some important global variables every frame. Calls basically every other function

> set_timer(): Sets the button lockout timer to a specific amount
> update_game_state(): Takes the game state, and calls the appropriate function to return a new game state, the info getter (used for the display), bgm, settings and ruleset
> update_replay_blobs(): Extracts information from the currently loaded replay file to use in the replay and its display
> return_blobs(): Returns the blobs and their CPU status for use in crash reports
'''

def set_timer(frames):
    '''
    Sets the button lockout timer

    Inputs:
        - frames [int]: The number that the lockout timer should be set to

    Outputs:
        - timer [int] (global): The lockout timer
    '''
    global timer
    timer = frames

from tkinter import N
from engine.gameplay import clear_info_cache
import engine.tutorial
import engine.menus.pause_menu
from engine.initializer import initialize_ruleset, initialize_settings
import engine.menus.main_menu
import engine.menus.css_menu
import engine.menus.rules_menu
import engine.menus.settings_menu
import engine.menus.almanac_menu
import engine.menus.blob_info_menu
import engine.menus.medal_milestone_menu
import engine.rebind
from engine.game_mode_flags import set_game_mode, return_game_mode
from engine.replays import return_replay_info
from engine.unlocks import return_available_costumes, update_css_blobs, update_mam_medals, update_costumes
from engine.get_random_blob import get_random_blob
import engine.win_screen_handler
import resources.graphics_engine.display_gameplay
import resources.graphics_engine.display_win_screen
import resources.graphics_engine.display_css
from os import getcwd, getenv
cwd = getcwd()
appcwd = getenv('APPDATA')+'/BlobBall/'

ruleset = initialize_ruleset(appcwd)
settings = initialize_settings(appcwd)
replay_ruleset = None


timer = 0
previous_screen = ""
player_info = {}
game_stats = []
def update_game_state(game_state, cwd):
    '''
    Takes in the current game state, and then calls the appropriate function that handles the game state.
    Updates the game state, info getter (used for the display), background music, ruleset and settings

    Inputs:
        - game_state [string]: The current game state, which tells which screen we are currently on (String)
        - cwd [string]: The current directory. Use unknown.
        - timer [int] (global): A lockout timer that prevents people from menuing too quickly
        - previous_screen [string] (global): This keeps track of our previous screen in certain circumstances, used mostly for ruleset, settings and almanac (you can navigate to these through the css and the main menu)
        - p1_blob [varies] (global): Keeps track of the current selected blob of P1
        - p2_blob [varies] (global): Keeps track of the current selected blob of P2 
        - p1_is_cpu [bool] (global): Keeps track of P1's status as a CPU or human player
        - p2_is_cpu [bool] (global): Keeps track of P2's status as a CPU or human player
        - p1_costume [int] (global): Keeps track of P1's selected costume
        - p2_costume [int] (global): Keeps track of P2's selected costume
        - ruleset [dict] (global): Keeps track of the current state of the ruleset, a dictionary
        - settings [dict] (global): Keeps track of the game settings, like volume and quality, a dictionary
        - game_stats [dict] (global): Keeps track of the current game stats, which can be viewed in the almanac
    
    Outputs:
        - game_state: The updated game_state, which tells which screen we are now on
        - info_getter: Usually an array filled with various elements. Contain necessary information to draw dynamic elements like characters and selector positions
        - song_playing: A string with the name of the background track to play
        - ruleset: Keeps track of the current state of the ruleset, a dictionary
        - settings: Keeps track of the game settings, like volume and quality, a dictionary
    '''
    global timer
    global previous_screen
    #global p1_blob
    #global p2_blob
    #global p1_is_cpu
    #global p2_is_cpu
    #global p1_costume
    #global p2_costume
    global player_info
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
        elif(game_state == "main_menu"):
            set_game_mode("squadball")

    elif(game_state == "css"):
        game_state, info_getter = engine.menus.css_menu.css_handler()
        if(game_state == "casual_match"):
            resources.graphics_engine.display_css.unload_css()

            # Looks like Miscellaneous CPU, Costume and Random Blob code
            """p1_blob = info_getter[0][1].token.current_blob
            p2_blob = info_getter[0][2].token.current_blob
            p1_costume = info_getter[0][1].token.current_costume
            p2_costume = info_getter[0][2].token.current_costume
            p1_is_cpu = info_getter[0][1].token.player_state == 'cpu'
            p2_is_cpu = info_getter[0][2].token.player_state == 'cpu'"""

            player_info = info_getter[0]
            timer = 60
        elif(game_state == "rules" or game_state == "settings"):
            timer = 3
            previous_screen = "css"
        elif(game_state == "main_menu"):
            timer = 10
        elif(game_state == "almanac"):
            timer = 10
            previous_screen = "css"
    elif(game_state == "casual_match"):
        game_state, info_getter = engine.gameplay.handle_gameplay(player_info, ruleset, settings, timer)
        if(game_state == "casual_win"):
            game_stats = info_getter[5]
            clear_info_cache()
        elif(game_state == "pause"):
            timer = 10
    elif(game_state == "pause"):
        game_state, info_getter = engine.menus.pause_menu.handle_pause_menu(timer, settings)
        if(game_state == 'css'):
            from resources.graphics_engine.display_gameplay import unload_image_cache
            clear_info_cache()
            unload_image_cache()
            timer = 10
        elif(game_state == 'casual_match'):
            timer = 10
    elif(game_state == "casual_win"):
        game_state, info_getter = engine.win_screen_handler.handle_win_screen(game_stats)
        song_playing = "bb_win_theme"
        if(game_state == "css" or game_state == "unlock_splash"):
            engine.win_screen_handler.reset_ready()
            resources.graphics_engine.display_gameplay.unload_image_cache()
            resources.graphics_engine.display_win_screen.unload_win_screen()
            resources.graphics_engine.display_css.update_css_blobs(appcwd)
            update_costumes()
            if(game_state == "unlock_splash"):
                timer = 60
    elif(game_state == "replay_match"):
        try:
            update_replay_blobs()
            game_state, info_getter = engine.gameplay.handle_gameplay(p1_blob, p2_blob, replay_ruleset, settings, False, False, p1_costume, p2_costume, timer, is_replay = True)
            if(game_state == "replay_win"):
                game_stats = info_getter[5]
                clear_info_cache()
            elif(game_state == "replay_pause"):
                timer = 10
        except KeyError:
            print("Short Replay Error")
            clear_info_cache()
            engine.win_screen_handler.reset_ready()
            resources.graphics_engine.display_gameplay.unload_image_cache()
            resources.graphics_engine.display_win_screen.unload_win_screen()
            game_state, info_getter = 1, "almanac"
    elif(game_state == "replay_win"):
        game_state, info_getter = engine.win_screen_handler.handle_win_screen(game_stats, is_replay = True)
        song_playing = "bb_win_theme"
        if(game_state == "almanac"):
            engine.win_screen_handler.reset_ready()
            resources.graphics_engine.display_gameplay.unload_image_cache()
            resources.graphics_engine.display_win_screen.unload_win_screen()
    elif(game_state == "replay_pause"):
        game_state, info_getter = engine.menus.pause_menu.handle_pause_menu(timer, settings)
        if(game_state == 'css'):
            from resources.graphics_engine.display_gameplay import unload_image_cache
            game_state = "almanac"
            clear_info_cache()
            unload_image_cache()
            timer = 10
        elif(game_state == 'casual_match'):
            game_state = 'replay_match'
            timer = 10
        else:
            game_state = "replay_pause"
    elif(game_state == "unlock_splash"):
        game_state, info_getter = engine.menus.css_menu.unlock_splash_handler(timer)
        song_playing = ""
        if(game_state != "unlock_splash"):
            update_css_blobs(appcwd)
            resources.graphics_engine.display_css.force_load_blobs()
    elif(game_state == "rules"):
        info_getter = engine.menus.rules_menu.rules_navigation(timer, ruleset, previous_screen, appcwd)
        game_state = info_getter[1]
        ruleset = info_getter[2]
    elif(game_state == "p1_mods" or game_state == "p2_mods"):
        game_state, info_getter = engine.menus.rules_menu.player_mods_navigation(timer, ruleset, game_state, appcwd)
    elif(game_state == "settings"):
        info_getter = engine.menus.settings_menu.settings_navigation(timer, settings, previous_screen, appcwd)
        game_state = info_getter[1]
    elif(game_state == "rebind"):
        game_state, info_getter = engine.rebind.rebind_menu()
    elif(game_state == "controller_config"):
        game_state,info_getter = engine.rebind.handle_joystick_config()
    elif(game_state == "almanac"):
        info_getter = engine.menus.almanac_menu.almanac_navigation(timer, previous_screen, ruleset)
        game_state = info_getter[1]
        song_playing = "bb_credits_theme"
        if(game_state != "almanac"):
            timer = 10
    elif(game_state == "blob_info"):
        game_state, info_getter = engine.menus.blob_info_menu.general_navigation()
        song_playing = "bb_credits_theme"
    elif(game_state == "medals"):
        game_state, info_getter = engine.menus.medal_milestone_menu.medal_navigation(timer)
        song_playing = "bb_credits_theme"
    elif(game_state == "almanac_stats"):
        info_getter = engine.menus.almanac_menu.almanac_stats_navigation_1(timer)
        game_state = info_getter[0]
        song_playing = "bb_credits_theme"
        if(game_state != "almanac_stats"):
            timer = 10
    elif(game_state == "almanac_stats_page_2"):
        info_getter = engine.menus.almanac_menu.almanac_stats_navigation_2(timer)
        game_state = info_getter[0]
        song_playing = "bb_credits_theme"
        if(game_state != "almanac_stats_page_2"):
            timer = 10
    elif(game_state == "almanac_stats_page_3"):
        game_state, info_getter = engine.menus.almanac_menu.almanac_stats_navigation_3()
        song_playing = "bb_credits_theme"
        if(game_state != "almanac_stats_page_3"):
            timer = 10
    elif(game_state == "almanac_art"):
        info_getter = engine.menus.almanac_menu.almanac_art_navigation(timer)
        game_state = info_getter[1]
        song_playing = "bb_credits_theme"
        if(game_state != "almanac_art"):
            timer = 10
    elif(game_state == "almanac_art_backgrounds"):
        info_getter = engine.menus.almanac_menu.almanac_art_backgrounds_navigation(timer)
        game_state = info_getter[1]
        song_playing = "bb_credits_theme"
    elif(game_state == "almanac_art_blobs"):
        info_getter = engine.menus.almanac_menu.almanac_art_blobs_navigation(timer)
        game_state = info_getter[1]
        song_playing = "bb_credits_theme"
    elif(game_state == "credits"):
        info_getter = engine.menus.almanac_menu.credits_navigation(timer)
        game_state = info_getter[0]
        song_playing = "bb_credits_theme"
    elif(game_state == "tutorial"):
        game_state, info_getter = engine.tutorial.handle_tutorial()
        if(game_state == "tutorial_complete"):
            timer = 60
    elif(game_state == "tutorial_complete"):
        game_state, info_getter = engine.tutorial.handle_tutorial_menu(timer)
    elif(game_state == "quit"):
        info_getter = []
    return game_state, info_getter, song_playing, settings, ruleset

def update_replay_blobs():
    '''
    Updates several global variables for use in replays

    Inputs/Outputs
        - replay_ruleset [dict] (global): Keeps track of the ruleset of that particular replay
        - p1_blob [varies] (global): Keeps track of the current selected blob of P1
        - p2_blob [varies] (global): Keeps track of the current selected blob of P2 
        - p1_costume [int] (global): Keeps track of P1's selected costume
        - p2_costume [int] (global): Keeps track of P2's selected costume

    '''
    global replay_ruleset
    global p1_blob
    global p2_blob
    global p1_costume
    global p2_costume
    extracted_info = return_replay_info()
    replay_ruleset = extracted_info[1]
    p1_blob = extracted_info[2]
    p1_costume = extracted_info[3]
    p2_blob = extracted_info[4]
    p2_costume = extracted_info[5]

def return_blobs():
    '''
    Returns the blobs and whether or not they are CPUs by pulling globals. Used when the game crashes

    Outputs:
        - p1_blob (global): Keeps track of the current selected blob of P1
        - p2_blob (global): Keeps track of the current selected blob of P2 
        - p1_is_cpu (global): Keeps track of P1's status as a CPU or human player
        - p2_is_cpu (global): Keeps track of P2's status as a CPU or human player 
    '''
    return p1_blob, p2_blob, p1_is_cpu, p2_is_cpu