import pygame as pg
import os
import ctypes

from pygame import image
from pygame.constants import FULLSCREEN, RESIZABLE
import engine.main_menu
import engine.gameplay
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_main_menu import draw_main_menu
from resources.graphics_engine.display_css import draw_css
from resources.graphics_engine.display_gameplay import draw_gameplay as draw_gameplay
from resources.graphics_engine.display_win_screen import draw_win_screen as draw_win_screen
from resources.graphics_engine.display_gameplay import unload_image_cache as unload_image_cache
from resources.graphics_engine.display_settings import draw_rebind_screen, draw_settings_screen as draw_settings_screen
from resources.graphics_engine.display_settings import draw_rules_screen as draw_rules_screen
from resources.graphics_engine.display_almanac import draw_almanac_art, draw_almanac_backgrounds, draw_almanac_blobs, draw_almanac_stats, draw_almanac_stats_2, draw_almanac_stats_3, draw_almanac_main as draw_almanac_main
from resources.graphics_engine.display_almanac import draw_almanac_credits as draw_almanac_credits
from engine.handle_input import toggle_fullscreen
import math
from json import loads, dumps

cwd = os.getcwd()
pg.quit()
os.environ['SDL_VIDEO_CENTERED'] = '1'

x = 100
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pg.init()

try:
    user32 = ctypes.windll.user32
    real_screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
except:
    print("Real Screen Size Exception")
    real_screen_size = (960, 540)

display_width = 1024
display_height = 576

pg.display.set_caption('Blob Ball')
game_display = pg.display.set_mode((display_width, display_height)) # The canvas
game_surface = pg.Surface((1366, 768))
pg.display.set_icon(pg.image.load(cwd+"/resources/images/ico_blob.ico"))

p1_blob = []
p2_blob = []
p1_is_cpu = False
p2_is_cpu = False
timer = 0
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

game_stats = ()
previous_screen = ""
toggle_timer = 0
full_screen = False
def handle_graphics(game_state, main_cwd, info_getter, settings):
    global real_screen_size
    global game_surface
    global game_display
    global p1_blob
    global p2_blob
    global p1_is_cpu
    global p2_is_cpu
    global cwd
    global timer
    global ruleset
    global game_stats
    global previous_screen

    screen_size = (1366, 768)
    cwd = main_cwd
    if(game_state == "main_menu"):
        selector_position = info_getter[0]
        draw_main_menu(screen_size, game_surface, selector_position, settings)
    elif(game_state == "css"):
        p1_selector_position = info_getter[0]
        p2_selector_position = info_getter[1]
        draw_css(screen_size, game_surface, p1_selector_position, p2_selector_position, settings)
    elif(game_state == "casual_match"):
        p1_blob = info_getter[0]
        p2_blob = info_getter[1]
        ball = info_getter[2]
        game_score = info_getter[3]
        timer = info_getter[4]
        game_state = info_getter[5]
        game_time = info_getter[6]
        try:
            draw_gameplay(screen_size, game_surface, p1_blob, p2_blob, ball, game_score, timer, game_time, settings)
        except:
            unload_image_cache()
            print("Weird match end exception:", info_getter)
    elif(game_state == "casual_win"):
        draw_win_screen(game_surface, info_getter, settings)
    elif(game_state == "rules"):
        selector_position = info_getter[0]
        game_state = info_getter[1]
        ruleset = info_getter[2]
        draw_rules_screen(screen_size, game_surface, ruleset, selector_position, settings)
    elif(game_state == "settings"):
        selector_position = info_getter[0]
        game_state = info_getter[1]
        the_settings = info_getter[2]
        draw_settings_screen(game_surface, the_settings, selector_position)
    elif(game_state == "rebind"):
        draw_rebind_screen(game_surface, settings, info_getter[1])
    elif(game_state == "almanac"):
        selector_position = info_getter[0]
        draw_almanac_main(game_surface, selector_position, settings)
    elif(game_state == "almanac_stats"):
        draw_almanac_stats(game_surface, settings)
    elif(game_state == "almanac_stats_page_2"):
        draw_almanac_stats_2(game_surface, settings)
    elif(game_state == "almanac_stats_page_3"):
        selector_position = info_getter[1]
        draw_almanac_stats_3(game_surface, settings, selector_position)
    elif(game_state == "almanac_art"):
        selector_position = info_getter[0]
        draw_almanac_art(game_surface, selector_position, settings)
    elif(game_state == "almanac_art_backgrounds"):
        selector_position = info_getter[0]
        draw_almanac_backgrounds(game_surface, selector_position)
    elif(game_state == "almanac_art_blobs"):
        selector_position = info_getter[0]
        draw_almanac_blobs(game_surface, selector_position)
    elif(game_state == "credits"):
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
            print("SMOOTH")
            game_display.blit(pg.transform.smoothscale(game_surface, (display_width, display_height)), (0, 0))
        else:
            print("ROUGH")
            game_display.blit(pg.transform.scale(game_surface, (display_width, display_height)), (0, 0))
    pg.display.flip()
