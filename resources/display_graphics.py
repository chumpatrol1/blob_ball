import pygame as pg
import os
import ctypes
import engine.main_menu
pg.font.init()
cwd = os.getcwd()

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
game_display = pg.display.set_mode((0, 0)) # The canvas

print(screen_size)

pg.init()
clock = pg.time.Clock()
clock.tick(5)

def draw_background(screen_size, game_display, game_screen):
    if(game_screen == "main_menu"):
        background = pg.image.load("C:\\Users\\Elijah McLaughlin\\Desktop\\Python Projects\\Blob Ball\\blob_ball\\resources\\images\\triforce.jpg")
    background = pg.transform.scale(background, screen_size)
    game_display.blit(background, (0, 0))

def draw_main_menu(screen_size, game_display, selector_position):
    draw_background(screen_size, game_display, 'main_menu')
    menu_font = pg.font.SysFont('Arial', round(40*(768/768)))
    text_array = [
        menu_font.render('Casual', False, (255, 0, 0)),
        menu_font.render('Competitive', False, (255, 0, 0)),
        menu_font.render('Online (Unimplemented)', False, (255, 0, 0)),
        menu_font.render('Almanac', False, (255, 0, 0)),
        menu_font.render('Rules', False, (255, 0, 0)),
        menu_font.render('Settings', False, (255, 0, 0)),
        menu_font.render('Quit', False, (255, 0, 0))
    ]


    ball = pg.image.load("C:\\Users\\Elijah McLaughlin\\Desktop\\Python Projects\\Blob Ball\\blob_ball\\resources\\images\\soccer_ball.png")
    ball = pg.transform.scale(ball, (screen_size[1]//10, screen_size[1]//10))
    game_display.blit(ball, (screen_size[0]*(2/3), ((screen_size[1]//10) * selector_position) + (0.5 * screen_size[1]//10)))

    text_y = screen_size[1]//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (screen_size[0]//2, text_y)
        game_display.blit(text_box, text_rect)
        text_y += screen_size[1]//10


def handle_graphics(game_state):
    global screen_size
    global game_display
    if(game_state == "main_menu"):
        info_getter = engine.main_menu.menu_navigation()
        selector_position = info_getter[0]
        game_state = info_getter[1]
        draw_main_menu(screen_size, game_display, selector_position)
    #print(selector_position)
    pg.display.flip()

    return game_state