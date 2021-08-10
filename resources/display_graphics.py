import pygame as pg
import os
import ctypes

from pygame import image
from pygame.constants import FULLSCREEN, RESIZABLE
import engine.main_menu
import engine.gameplay
from resources.background_handler import draw_background as draw_background
from resources.display_main_menu import draw_main_menu
from resources.display_css import draw_css
from resources.display_gameplay import draw_gameplay as draw_gameplay
from resources.display_gameplay import draw_win_screen as draw_win_screen
from resources.display_settings import draw_rebind_screen, draw_settings_screen as draw_settings_screen
from resources.display_settings import draw_rules_screen as draw_rules_screen
from resources.display_almanac import draw_almanac_art, draw_almanac_backgrounds, draw_almanac_blobs, draw_almanac_stats, draw_almanac_main as draw_almanac_main
from resources.display_almanac import draw_almanac_credits as draw_almanac_credits
from engine.handle_input import toggle_fullscreen
import math
from json import loads, dumps

cwd = os.getcwd()
pg.quit()
os.environ['SDL_VIDEO_CENTERED'] = '1'
print("GRAPHICS CWD: "+ cwd)

x = 100
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pg.init()

user32 = ctypes.windll.user32
real_screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#real_screen_size = (960, 540)

display_width = 1024
display_height = 576

pg.display.set_caption('Blob Ball')
game_display = pg.display.set_mode((display_width, display_height)) # The canvas
game_surface = pg.Surface((1366, 768))

p1_blob = []
p2_blob = []
timer = 0
game_version = '0.7.0b'
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
}

try:
    with open(cwd+'\\engine\\config\\ruleset.txt', 'r') as rulesetdoc:
        ruleset = loads(rulesetdoc.readline())
    with open(cwd+'\\engine\\config\\ruleset.txt', 'w') as rulesetdoc:
        ruleset['version'] = game_version
        rulesetdoc.write(dumps(ruleset))
except:
    with open(cwd+'\\engine\\config\\ruleset.txt', 'w') as rulesetdoc:
        rulesetdoc.write(dumps(ruleset))
try:
    with open(cwd+'/engine/config/settings.txt', 'r') as settingsdoc:
        settings = loads(settingsdoc.readline())
except:
    with open(cwd+'/engine/config/settings.txt', 'w') as settingsdoc:
        settingsdoc.write(dumps(settings))

game_stats = ()
previous_screen = ""
toggle_timer = 0
full_screen = False
def handle_graphics(game_state, main_cwd):
    global real_screen_size
    global game_surface
    global game_display
    global p1_blob
    global p2_blob
    global cwd
    global timer
    global ruleset
    global game_stats
    global previous_screen

    screen_size = (1366, 768)
    cwd = main_cwd
    if(game_state == "main_menu"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.menu_navigation(timer)
        selector_position = info_getter[0]
        draw_main_menu(screen_size, game_surface, selector_position, settings)
        game_state = info_getter[1]
        if(game_state == "rules" or game_state == "settings" or game_state == "almanac"):
            previous_screen = "main_menu"
    elif(game_state == "css"):
        info_getter = engine.main_menu.css_handler()
        p1_selector_position = info_getter[0]
        p2_selector_position = info_getter[1]
        draw_css(screen_size, game_surface, p1_selector_position, p2_selector_position, settings)
        game_state = info_getter[2]
        if(game_state == "casual_match"):
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
        info_getter = engine.gameplay.handle_gameplay(p1_blob, p2_blob, ruleset, settings)
        p1_blob = info_getter[0]
        p2_blob = info_getter[1]
        ball = info_getter[2]
        game_score = info_getter[3]
        timer = info_getter[4]
        game_state = info_getter[5]
        game_time = info_getter[6]
        if(game_state == "casual_win"):
            game_stats = info_getter[6]
            timer = 120
            return game_state
        draw_gameplay(screen_size, game_surface, p1_blob, p2_blob, ball, game_score, timer, game_time, settings)
    elif(game_state == "casual_win"):
        draw_win_screen(screen_size, game_surface, game_stats, settings)
        timer -= 1
        if(timer == 0):
            return "css"
    elif(game_state == "rules"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.rules_navigation(timer, ruleset, previous_screen, cwd)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        draw_rules_screen(screen_size, game_surface, ruleset, selector_position, settings)
    elif(game_state == "settings"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.settings_navigation(timer, settings, previous_screen, cwd)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        draw_settings_screen(game_surface, settings, selector_position)
    elif(game_state == "rebind"):
        info_getter = draw_rebind_screen(game_surface, settings)
        game_state = info_getter[0]
    elif(game_state == "almanac"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_navigation(timer, previous_screen)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        if(game_state != "almanac"):
            timer = 10
        draw_almanac_main(game_surface, selector_position, settings)
    elif(game_state == "almanac_stats"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_stats_navigation(timer)
        game_state = info_getter[0]
        if(game_state != "almanac_stats"):
            timer = 10
        draw_almanac_stats(game_surface, settings)
    elif(game_state == "almanac_art"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.almanac_art_navigation(timer)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        if(game_state != "almanac_art"):
            timer = 10
        draw_almanac_art(game_surface, selector_position, settings)
    elif(game_state == "almanac_art_backgrounds"):
        info_getter = engine.main_menu.almanac_art_backgrounds_navigation(timer)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        if(timer > 0):
            timer -=1
        draw_almanac_backgrounds(game_surface, selector_position)
    elif(game_state == "almanac_art_blobs"):
        info_getter = engine.main_menu.almanac_art_blobs_navigation(timer)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        if(timer > 0):
            timer -=1
        draw_almanac_blobs(game_surface, selector_position)
    elif(game_state == "credits"):
        if(timer > 0):
            timer -= 1
        info_getter = engine.main_menu.credits_navigation(timer)
        game_state = info_getter[0]
        draw_almanac_credits(game_surface, settings)
    global toggle_timer
    global full_screen
    global display_height, display_width
    if(toggle_timer > 0):
        toggle_timer -= 1
    else:
        toggle = toggle_fullscreen()
        if(toggle):
            if(full_screen):
                pg.display.quit()
                pg.display.init()
                pg.display.set_caption('Blob Ball')
                game_display = pg.display.set_mode((display_width, display_height))
                full_screen = False
            else: 
                game_display = pg.display.set_mode(real_screen_size, FULLSCREEN)
                display_width = 1024
                display_height = 576
                full_screen = True
            
            toggle_timer = 10


    if(full_screen):
        if(settings['smooth_scaling']):
            game_display.blit(pg.transform.smoothscale(game_surface, (real_screen_size[0], real_screen_size[1])), (0, 0))
        else:
            game_display.blit(pg.transform.scale(game_surface, (real_screen_size[0], real_screen_size[1])), (0, 0))
    else:
        for event in pg.event.get():
            if(event.type == pg.VIDEORESIZE):
                display_width, display_height = event.w, event.h
        if(settings['smooth_scaling']):
            game_display.blit(pg.transform.smoothscale(game_surface, (display_width, display_height)), (0, 0))
        else:
            game_display.blit(pg.transform.scale(game_surface, (display_width, display_height)), (0, 0))
    pg.display.flip()
    return game_state