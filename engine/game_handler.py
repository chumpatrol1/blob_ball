from engine.gameplay import clear_info_cache
import engine.main_menu
import engine.rebind
import engine.win_screen_handler
import resources.graphics_engine.display_gameplay
import resources.graphics_engine.display_win_screen
import resources.graphics_engine.display_css
from os import getcwd
from json import loads, dumps
cwd = getcwd()

game_version = '0.8.0a'
ruleset = {
    'version': game_version,
    'goal_limit': 5,
    'time_limit': 3600,
    'time_bonus': 600,
    'special_ability_charge_base': 1,
    'danger_zone_enabled': True,
}

settings = {
    'hd_backgrounds': True,
    'hd_blobs': True,
    'smooth_scaling': True,
    'music_volume': 10,
    'sound_volume': 10,
}

try:
    with open(cwd+'/config/ruleset.txt', 'r') as rulesetdoc:
        ruleset = loads(rulesetdoc.readline())
    with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
        ruleset['version'] = game_version
        rulesetdoc.write(dumps(ruleset))
except:
    with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
        rulesetdoc.write(dumps(ruleset))
try:
    with open(cwd+'/config/settings.txt', 'r') as settingsdoc:
        settings = loads(settingsdoc.readline())
except:
    with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
        settingsdoc.write(dumps(settings))

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
    if(game_state == "main_menu"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.menu_navigation(timer)
        game_state = info_getter[1]
        if(game_state == "rules" or game_state == "settings" or game_state == "almanac"):
            previous_screen = "main_menu" 
    elif(game_state == "css"):
        info_getter = engine.main_menu.css_handler()
        p1_selector_position = info_getter[0]
        p2_selector_position = info_getter[1]
        game_state = info_getter[2]
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
            p1_blob = info_getter[3]
            p2_blob = info_getter[4]
        elif(game_state == "rules" or game_state == "settings"):
            timer = 3
            previous_screen = "css"
        elif(game_state == "main_menu"):
            timer = 10
        elif(game_state == "almanac"):
            timer = 10
            previous_screen = "css"
    elif(game_state == "casual_match"):
        info_getter = engine.gameplay.handle_gameplay(p1_blob, p2_blob, ruleset, settings, p1_is_cpu, p2_is_cpu)
        game_state = info_getter[5]
        if(game_state == "casual_win"):
            game_stats = info_getter[6]
            clear_info_cache()
    elif(game_state == "casual_win"):
        game_state, info_getter = engine.win_screen_handler.handle_win_screen(game_stats) 
        if(game_state == "css"):
            engine.win_screen_handler.reset_ready()
            resources.graphics_engine.display_gameplay.unload_image_cache()
            resources.graphics_engine.display_win_screen.unload_win_screen()
    elif(game_state == "rules"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.rules_navigation(timer, ruleset, previous_screen, cwd)
        game_state = info_getter[1]
    elif(game_state == "settings"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.settings_navigation(timer, settings, previous_screen, cwd)
        game_state = info_getter[1]
    elif(game_state == "rebind"):
        info_getter = engine.rebind.handle_rebinding()
        game_state = info_getter[0]
    elif(game_state == "almanac"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_navigation(timer, previous_screen)
        game_state = info_getter[1]
        if(game_state != "almanac"):
            timer = 10
    elif(game_state == "almanac_stats"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_stats_navigation(timer)
        game_state = info_getter[0]
        if(game_state != "almanac_stats"):
            timer = 10
    elif(game_state == "almanac_stats_page_2"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_stats_navigation_2(timer)
        game_state = info_getter[0]
        if(game_state != "almanac_stats_page_2"):
            timer = 10
    elif(game_state == "almanac_stats_page_3"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_stats_navigation_3()
        game_state = info_getter[0]
        if(game_state != "almanac_stats_page_3"):
            timer = 10
    elif(game_state == "almanac_art"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_art_navigation(timer)
        game_state = info_getter[1]
        if(game_state != "almanac_art"):
            timer = 10
    elif(game_state == "almanac_art_backgrounds"):
        info_getter = engine.main_menu.almanac_art_backgrounds_navigation(timer)
        game_state = info_getter[1]
        if(timer > 0):
            timer -= 1
    elif(game_state == "almanac_art_blobs"):
        info_getter = engine.main_menu.almanac_art_blobs_navigation(timer)
        game_state = info_getter[1]
        if(timer > 0):
            timer -=1
    elif(game_state == "credits"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.credits_navigation(timer)
        game_state = info_getter[0]
    return game_state, info_getter, "bb_main_theme", settings, ruleset