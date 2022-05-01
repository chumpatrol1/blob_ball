def set_timer(frames):
    global timer
    timer = frames

from tkinter import N
from engine.gameplay import clear_info_cache
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
from engine.replays import return_replay_info
from engine.unlocks import update_css_blobs, update_css_medals
import engine.win_screen_handler
import resources.graphics_engine.display_gameplay
import resources.graphics_engine.display_win_screen
import resources.graphics_engine.display_css
from os import getcwd
cwd = getcwd()

ruleset = initialize_ruleset(cwd)
settings = initialize_settings(cwd)
replay_ruleset = None


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
    elif(game_state == "css"):
        game_state, info_getter = engine.menus.css_menu.css_handler()
        p1_selector_position = info_getter[0]
        p2_selector_position = info_getter[1]
        if(game_state == "casual_match"):
            resources.graphics_engine.display_css.unload_css()
            if(p1_selector_position[3]):
                p1_is_cpu = True
            else:
                p1_is_cpu = False
            if(p2_selector_position[3]):
                p2_is_cpu = True
            else:
                p2_is_cpu = False
            p1_selector_position[2] = 0
            p2_selector_position[2] = 0
            p1_blob = info_getter[2]
            p2_blob = info_getter[3]
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
        info_getter = engine.gameplay.handle_gameplay(p1_blob, p2_blob, ruleset, settings, p1_is_cpu, p2_is_cpu, timer)
        game_state = info_getter[5]
        if(game_state == "casual_win"):
            game_stats = info_getter[6]
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
        if(game_state == "css" or game_state == "pop_up"):
            engine.win_screen_handler.reset_ready()
            resources.graphics_engine.display_gameplay.unload_image_cache()
            resources.graphics_engine.display_win_screen.unload_win_screen()
            resources.graphics_engine.display_css.update_css_blobs(cwd)
            if(game_state == "pop_up"):
                timer = 60
    elif(game_state == "replay_match"):
        update_replay_blobs()
        info_getter = engine.gameplay.handle_gameplay(p1_blob, p2_blob, replay_ruleset, settings, False, False, timer, is_replay = True)
        game_state = info_getter[5] # TODO: Fix/parity the output
        if(game_state == "replay_win"):
            game_stats = info_getter[6]
            clear_info_cache()
        elif(game_state == "replay_pause"):
            timer = 10
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
    elif(game_state == "pop_up"):
        game_state, info_getter = engine.menus.css_menu.popup_handler(timer)
        song_playing = ""
        if(game_state != "pop_up"):
            update_css_blobs(cwd)
            resources.graphics_engine.display_css.force_load_blobs()
    elif(game_state == "rules"):
        info_getter = engine.menus.rules_menu.rules_navigation(timer, ruleset, previous_screen, cwd)
        game_state = info_getter[1]
        ruleset = info_getter[2]
    elif(game_state == "p1_mods" or game_state == "p2_mods"):
        game_state, info_getter = engine.menus.rules_menu.player_mods_navigation(timer, ruleset, game_state, cwd)
    elif(game_state == "settings"):
        info_getter = engine.menus.settings_menu.settings_navigation(timer, settings, previous_screen, cwd)
        game_state = info_getter[1]
    elif(game_state == "rebind"):
        game_state, info_getter = engine.rebind.rebind_menu()
    elif(game_state == "controller_config"):
        game_state,info_getter = engine.rebind.handle_joystick_config()
    elif(game_state == "almanac"):
        info_getter = engine.menus.almanac_menu.almanac_navigation(timer, previous_screen)
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
        info_getter = engine.menus.almanac_menu.almanac_stats_navigation(timer)
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
        game_state, info_getter = "main_menu", []
    elif(game_state == "quit"):
        info_getter = []
    return game_state, info_getter, song_playing, settings, ruleset

def update_replay_blobs():
    global replay_ruleset
    global p1_blob
    global p2_blob
    extracted_info = return_replay_info()
    replay_ruleset = extracted_info[1]
    p1_blob = extracted_info[2]
    p2_blob = extracted_info[3]

def return_blobs():
    return p1_blob, p2_blob, p1_is_cpu, p2_is_cpu