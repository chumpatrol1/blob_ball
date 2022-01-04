import pygame as pg
import os

from pygame import image
from pygame.constants import FULLSCREEN, RESIZABLE
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_main_menu import draw_main_menu
from resources.graphics_engine.display_splash import draw_splash_screen as draw_splash_screen
from resources.graphics_engine.display_debug import draw_debug
from engine.handle_input import toggle_fullscreen

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

    screen_size = (1366, 768)
    cwd = main_cwd
    if(game_state == "control_splash"):
        draw_splash_screen(game_surface, info_getter, settings)
    if(game_state == "main_menu"):
        draw_main_menu(game_surface, info_getter, settings)
    # Draw Debug info (really laggily)
    #draw_debug(game_surface)

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
        for event in pg.event.get():
            if(event.type == pg.VIDEORESIZE):
                display_width, display_height = update_width_and_height(event.w, event.h)
        if(settings['smooth_scaling']):
            game_display.blit(pg.transform.smoothscale(game_surface, (display_width, display_height)), (0, 0))
        else:
            game_display.blit(pg.transform.scale(game_surface, (display_width, display_height)), (0, 0))
    pg.display.flip()
