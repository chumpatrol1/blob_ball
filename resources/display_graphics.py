import pygame as pg
import os
import ctypes
import engine.main_menu
pg.font.init()
cwd = os.getcwd()
print("GRAPHICS CWD: "+cwd)
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
game_display = pg.display.set_mode((0, 0)) # The canvas

pg.init()
clock = pg.time.Clock()
clock.tick(60)

def draw_background(screen_size, game_display, game_screen):
    global cwd
    if(game_screen == "main_menu"):
        background = pg.image.load(cwd + "\\resources\\images\\triforce.jpg")
    if(game_screen == "casual_css"):
        background = pg.image.load(cwd + "\\resources\\images\\triforce.jpg")
    background = pg.transform.scale(background, screen_size)
    game_display.blit(background, (0, 0))

def draw_main_menu(screen_size, game_display, selector_position):
    draw_background(screen_size, game_display, 'main_menu')
    menu_font = pg.font.SysFont('Arial', round(40*(screen_size[1]/768)))
    text_array = [
        menu_font.render('Casual', False, (255, 0, 0)),
        menu_font.render('Competitive', False, (255, 0, 0)),
        menu_font.render('Online (Unimplemented)', False, (255, 0, 0)),
        menu_font.render('Almanac', False, (255, 0, 0)),
        menu_font.render('Rules', False, (255, 0, 0)),
        menu_font.render('Settings', False, (255, 0, 0)),
        menu_font.render('Quit', False, (255, 0, 0))
    ]


    ball = pg.image.load(cwd + "\\resources\\images\\soccer_ball.png")
    ball = pg.transform.scale(ball, (screen_size[1]//10, screen_size[1]//10))
    game_display.blit(ball, (screen_size[0]*(2/3), ((screen_size[1]//10) * selector_position) + (0.5 * screen_size[1]//10)))

    text_y = screen_size[1]//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (screen_size[0]//2, text_y)
        game_display.blit(text_box, text_rect)
        text_y += screen_size[1]//10

blob_array = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "Quirkless Blob", "No Ability"]]
] #TODO: Incorporate this at a later time.


def css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position):
    '''
    Draws the blobs on screen, and handles "mousing over" blobs.
    '''
    global cwd
    quirkless_blob = pg.image.load(cwd + "\\resources\\images\\blobs\\quirkless_blob.png")
    quirkless_blob = pg.transform.scale(quirkless_blob, (screen_size[0]//15, screen_size[1]//15))
    for x in range(2, 9): #Temporary, until we make more blobs
        for y in range (1, 6):
            game_display.blit(quirkless_blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(20/768))))
    quirkless_blob = pg.transform.scale(quirkless_blob, (screen_size[0]//7, screen_size[1]//7))
    if(p2_selector_position[0] > 0):
        game_display.blit(quirkless_blob, (screen_size[0]* (3/4), screen_size[1]*(3/4)))
    quirkless_blob = pg.transform.flip(quirkless_blob, True, False)
    if(p1_selector_position[0] > 0):
        game_display.blit(quirkless_blob, (screen_size[0]/10, screen_size[1]*(3/4)))
    
    

def draw_casual_css(screen_size, game_display, p1_selector_position, p2_selector_position):
    global cwd
    draw_background(screen_size, game_display, "casual_css")
    for x in range(0, 8):
        for y in range (0, 5):
            pg.draw.rect(game_display, (255, 255, 255), ((x*screen_size[0]*0.1) + (screen_size[0]/10), (y*screen_size[1]*(100/768))+(screen_size[1]*50/768), screen_size[0]*0.1, screen_size[1]*(100/768)), width = 3)
    css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position)
    back_arrow = pg.image.load(cwd + "\\resources\\images\\back_arrow.png")
    back_arrow = pg.transform.scale(back_arrow, (screen_size[1]//15, screen_size[1]//15))
    game_display.blit(back_arrow, (screen_size[0]*(1/8), screen_size[1]//10))
    if(p1_selector_position[2] == 0):
        p1_ball = pg.image.load(cwd + "\\resources\\images\\p1_token.png")
    else:
        p1_ball = pg.image.load(cwd + "\\resources\\images\\p1_check.png")
    if(p2_selector_position[2] == 0):
        p2_ball = pg.image.load(cwd + "\\resources\\images\\p2_token.png")
    else:
        p2_ball = pg.image.load(cwd + "\\resources\\images\\p2_check.png")

    p1_ball = pg.transform.scale(p1_ball, (screen_size[1]//15, screen_size[1]//15))
    p2_ball = pg.transform.scale(p2_ball, (screen_size[1]//15, screen_size[1]//15))
    game_display.blit(p1_ball, ((screen_size[0]//10 * (p1_selector_position[0] + 1) + screen_size[0]*(1/135)), (screen_size[1]*(100/768)) * (p1_selector_position[1] + 1) - (screen_size[1] * (25/768))))
    game_display.blit(p2_ball, ((screen_size[0]//10 * (p2_selector_position[0] + 1) + screen_size[0]*(8/135)), (screen_size[1]*(100/768)) * (p2_selector_position[1] + 1) - (screen_size[1] * (25/768))))

    if(p1_selector_position[2] >= 1 and p2_selector_position[2] >= 1):
        pg.draw.rect(game_display, (255, 255, 0), (0, screen_size[1]*(2/5), screen_size[0], screen_size[1]/5))
        menu_font = pg.font.SysFont('Arial', round(80*(screen_size[1]/768)))
        menu_text = menu_font.render('CONFIRM READY WITH "ABILITY"', False, (255, 124, 0))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]//2, screen_size[1]//2)
        game_display.blit(menu_text, text_rect)
        if(p1_selector_position[2] == 2):
            game_display.blit(p1_ball, ((screen_size[0]*(1/10), screen_size[1]*(2/5))))
        if(p2_selector_position[2] == 2):
            game_display.blit(p2_ball, ((screen_size[0]*(9/10), screen_size[1]*(2/5))))


def handle_graphics(game_state):
    global screen_size
    global game_display
    if(game_state == "main_menu"):
        info_getter = engine.main_menu.menu_navigation()
        selector_position = info_getter[0]
        draw_main_menu(screen_size, game_display, selector_position)
        game_state = info_getter[1]
    elif(game_state == "casual_css"):
        info_getter = engine.main_menu.casual_css_navigation()
        p1_selector_position = info_getter[0]
        p2_selector_position = info_getter[1]
        draw_casual_css(screen_size, game_display, p1_selector_position, p2_selector_position)
        game_state = info_getter[2]
    #print(selector_position)
    pg.display.flip()
    return game_state