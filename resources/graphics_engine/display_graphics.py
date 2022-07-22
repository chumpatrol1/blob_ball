import pygame as pg
import os

from pygame import image
from pygame.constants import FULLSCREEN, RESIZABLE
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_blob_info import draw_blob_info
from resources.graphics_engine.display_main_menu import draw_main_menu
from resources.graphics_engine.display_css import draw_css
from resources.graphics_engine.display_gameplay import draw_gameplay as draw_gameplay
from resources.graphics_engine.display_pause import capture_gameplay, draw_pause_background, draw_pause_screen
from resources.graphics_engine.display_tutorial import draw_tutorial, draw_tutorial_completion
from resources.graphics_engine.display_win_screen import draw_win_screen as draw_win_screen
from resources.graphics_engine.display_gameplay import unload_image_cache as unload_image_cache
from resources.graphics_engine.display_settings import draw_controller_bind_screen, draw_rebind_screen, draw_settings_screen, draw_rules_screen, draw_pmods_screen
from resources.graphics_engine.display_almanac import draw_almanac_art, draw_almanac_backgrounds, draw_almanac_blobs, draw_almanac_stats, draw_almanac_stats_2, draw_almanac_stats_3, draw_almanac_main as draw_almanac_main
from resources.graphics_engine.display_medals_and_milestones import draw_mam
from resources.graphics_engine.display_almanac import draw_almanac_credits as draw_almanac_credits
from resources.graphics_engine.display_splash import draw_splash_screen as draw_splash_screen
from resources.graphics_engine.display_pop_up import draw_pop_up as draw_pop_up, process_controller_popups
from resources.graphics_engine.display_debug import draw_debug
from engine.handle_input import toggle_fullscreen

from engine.get_events import get_events

from resources.graphics_engine.handle_screen_size import initialize_screen_size, return_real_screen_size, return_width_and_height, update_mouse_wh, update_width_and_height

cwd = os.getcwd()
pg.quit()
os.environ['SDL_VIDEO_CENTERED'] = '1'

x = 100
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pg.init()

display_width, display_height = return_width_and_height()

pg.display.set_caption('Blob Ball')
game_display = pg.display.set_mode((display_width, display_height)) # The canvas
game_surface = pg.Surface((1366, 768))
pg.display.set_icon(pg.image.load(cwd+"/resources/images/ico_blob.ico"))

p1_blob = []
p2_blob = []
p1_is_cpu = False
p2_is_cpu = False
timer = 0

game_stats = ()
previous_screen = ""
toggle_timer = 0
full_screen = False

def capture_screen():
    global game_surface
    capture_gameplay(game_surface)

def handle_graphics(game_state, main_cwd, info_getter, settings):
    real_screen_size = return_real_screen_size()
    global game_surface
    global game_display
    global p1_blob
    global p2_blob
    global p1_is_cpu
    global p2_is_cpu
    global cwd
    global timer
    global game_stats
    global previous_screen

    cwd = main_cwd
    if(game_state == "control_splash"):
        draw_splash_screen(game_surface, info_getter, settings)
    if(game_state == "main_menu"):
        draw_main_menu(game_surface, info_getter, settings)
    elif(game_state == "css"):
        draw_css(game_surface, info_getter, settings)
    elif(game_state == "casual_match" or game_state == "replay_match"):
        draw_gameplay(game_surface, info_getter, settings)
        #capture_gameplay(game_surface) # TODO: If this can be faster, make it faster
    elif(game_state == "tutorial"):
        draw_tutorial(game_surface, info_getter, settings)
    elif(game_state == "tutorial_complete"):
        draw_tutorial_completion(game_surface, info_getter, settings)
    elif(game_state == "pause"):
        draw_pause_background(game_surface)
        draw_pause_screen(game_surface, info_getter, settings)
    elif(game_state == "replay_pause"):
        draw_pause_background(game_surface)
        draw_pause_screen(game_surface, info_getter, settings)
    elif(game_state == "casual_win" or game_state == "replay_win"):
        draw_win_screen(game_surface, info_getter, settings)
    elif(game_state == "pop_up"):
        draw_pop_up(game_surface, info_getter, settings)
    elif(game_state == "rules"):
        selector_position = info_getter[0]
        game_state = info_getter[1]
        ruleset = info_getter[2]
        draw_rules_screen(game_surface, ruleset, selector_position, settings)
    elif(game_state == "p1_mods" or game_state == "p2_mods"):
        draw_pmods_screen(game_surface, info_getter, settings)
    elif(game_state == "settings"):
        selector_position = info_getter[0]
        game_state = info_getter[1]
        the_settings = info_getter[2]
        draw_settings_screen(game_surface, the_settings, selector_position)
    elif(game_state == "rebind"):
        draw_rebind_screen(game_surface, settings, info_getter)
    elif(game_state == "controller_config"):
        draw_controller_bind_screen(game_surface, info_getter, settings)
    elif(game_state == "almanac"):
        selector_position = info_getter[0]
        draw_almanac_main(game_surface, selector_position, settings)
    elif(game_state == "blob_info"):
        draw_blob_info(game_surface, info_getter, settings)
    elif(game_state == "medals"):
        draw_mam(game_surface, info_getter, settings)
    elif(game_state == "almanac_stats"):
        draw_almanac_stats(game_surface, settings)
    elif(game_state == "almanac_stats_page_2"):
        draw_almanac_stats_2(game_surface, settings)
    elif(game_state == "almanac_stats_page_3"):
        draw_almanac_stats_3(game_surface, settings, info_getter)
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

    # Draw Debug info (really laggily)
    #draw_debug(game_surface)
    process_controller_popups(game_surface)

    global toggle_timer
    global full_screen
    display_width, display_height = return_width_and_height()
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
                update_mouse_wh(display_width, display_height)
                full_screen = False
            else: 
                game_display = pg.display.set_mode(real_screen_size, FULLSCREEN)
                update_width_and_height(1024, 576)
                update_mouse_wh(*real_screen_size)
                display_width, display_height = return_width_and_height()
                full_screen = True
            
            toggle_timer = 10


    if(full_screen):
        if(settings['smooth_scaling']):
            game_display.blit(pg.transform.smoothscale(game_surface, (real_screen_size[0], real_screen_size[1])), (0, 0))
        else:
            game_display.blit(pg.transform.scale(game_surface, (real_screen_size[0], real_screen_size[1])), (0, 0))
    else:
        for event in get_events():
            if(event.type == pg.VIDEORESIZE):
                display_width, display_height = update_width_and_height(event.w, event.h)
        if(settings['smooth_scaling']):
            game_display.blit(pg.transform.smoothscale(game_surface, (display_width, display_height)), (0, 0))
        else:
            game_display.blit(pg.transform.scale(game_surface, (display_width, display_height)), (0, 0))
    pg.display.flip()
