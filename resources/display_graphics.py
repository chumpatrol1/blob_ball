import pygame as pg
import os
import ctypes

from pygame import image
import engine.main_menu
import engine.gameplay
from resources.background_handler import draw_background as draw_background
from resources.display_gameplay import draw_gameplay as draw_gameplay
from resources.display_settings import draw_settings_screen as draw_settings_screen
import math
pg.font.init()
cwd = os.getcwd()
print("GRAPHICS CWD: "+ cwd)
user32 = ctypes.windll.user32
real_screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#real_screen_size = (1040, 650)
game_display = pg.display.set_mode((0, 0)) # The canvas
game_surface = pg.Surface((1366, 768))


pg.init()
clock = pg.time.Clock()
#clock.tick(60)

def draw_main_menu(screen_size, game_display, selector_position, settings):
    draw_background(game_display, 'main_menu', settings)
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
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "Quirkless Blob", "No Ability"], ["\\blobs\\fire_blob.png", "Fire Blob", "Fireball"], ["\\blobs\\ice_blob.png", "Ice Blob", "Snowball"], ["\\blobs\\water_blob.png", "Water Blob", "Geyser"], ["\\blobs\\rock_blob.png", "Rock Blob", "Spire"], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\rules_icon.png", "Rules", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\gear_icon.png", "Settings", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
]

def css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
    '''
    Draws the blobs on screen, and handles "mousing over" blobs.
    '''
    global cwd
    
    x = 0
    y = 0
    directory = cwd + "\\resources\\images"
    for row in blob_array: #Temporary, until we make more blobs
        y += 1
        for icon in row:
            x += 1
            blob = pg.image.load(directory + icon[0])
            if(x == 1):
                blob = pg.transform.scale(blob, (screen_size[0]//15, screen_size[0]//15))
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(45/768))))
            else:
                blob = pg.transform.scale(blob, (screen_size[0]//15, screen_size[1]//15))
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(20/768))))
        x = 0
    p1_selected_blob = pg.image.load(directory + blob_array[p1_selector_position[1]][p1_selector_position[0]][0])
    if(p1_selector_position[0] == 0):
        p1_selected_blob = pg.transform.scale(p1_selected_blob, (screen_size[0]//7, screen_size[0]//7))
    else:
        p1_selected_blob = pg.transform.scale(p1_selected_blob, (screen_size[0]//7, screen_size[1]//7))
    p1_selected_blob = p1_selected_blob.convert_alpha()
    if(p1_selector_position[2] == 0):
        p1_selected_blob.set_alpha(200)
    else:
        p1_selected_blob.set_alpha(255)
    p1_selected_blob = pg.transform.flip(p1_selected_blob, True, False)
    game_display.blit(p1_selected_blob, (screen_size[0]/10, screen_size[1]*(3/4)))
    p2_selected_blob = pg.image.load(directory + blob_array[p2_selector_position[1]][p2_selector_position[0]][0])
    if(p2_selector_position[0] == 0):
        p2_selected_blob = pg.transform.scale(p2_selected_blob, (screen_size[0]//7, screen_size[0]//7))
    else:
        p2_selected_blob = pg.transform.scale(p2_selected_blob, (screen_size[0]//7, screen_size[1]//7))
    p2_selected_blob = p2_selected_blob.convert_alpha()
    if(p2_selector_position[2] == 0):
        p2_selected_blob.set_alpha(200)
    else:
        p2_selected_blob.set_alpha(255)
    game_display.blit(p2_selected_blob, (screen_size[0]*(3/4), screen_size[1]*(3/4)))

    menu_font = pg.font.SysFont('Arial', round(50*(screen_size[1]/768)))
    menu_text = menu_font.render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][1]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*screen_size[0]//6, 11*screen_size[1]//12)
    game_display.blit(menu_text, text_rect)
    menu_text = menu_font.render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][1]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//6, 11*screen_size[1]//12)
    game_display.blit(menu_text, text_rect)

    menu_font = pg.font.SysFont('Arial', round(30*(screen_size[1]/768)))
    menu_text = menu_font.render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][2]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*screen_size[0]//6, 24*screen_size[1]//25)
    game_display.blit(menu_text, text_rect)
    menu_text = menu_font.render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][2]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//6, 24*screen_size[1]//25)
    game_display.blit(menu_text, text_rect)

def draw_casual_css(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
    global cwd
    draw_background(game_display, "casual_css", settings)
    for x in range(0, 8):
        for y in range (0, 5):
            pg.draw.rect(game_display, (255, 255, 255), ((x*screen_size[0]*0.1) + (screen_size[0]/10), (y*screen_size[1]*(100/768))+(screen_size[1]*50/768), screen_size[0]*0.1, screen_size[1]*(100/768)), width = 3)
    css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings)
    #back_arrow = pg.image.load(cwd + "\\resources\\images\\back_arrow.png")
    #back_arrow = pg.transform.scale(back_arrow, (screen_size[1]//15, screen_size[1]//15))
    #game_display.blit(back_arrow, (screen_size[0]*(1/8), screen_size[1]//10))
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
        
def draw_win_screen(screen_size, game_display, game_stats, settings):
    draw_background(game_display, "win_screen", settings)
    menu_font = pg.font.SysFont('Arial', round(50*(screen_size[1]/768)))
    if(game_stats == 3):
        menu_text = menu_font.render("TIE", False, (255, 124, 0))
    else:
        menu_text = menu_font.render("WINNER: "+ str(game_stats), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//2, screen_size[1]//7)
    game_display.blit(menu_text, text_rect)

def draw_rules_screen(screen_size, game_display, ruleset, selector_position, settings):
    draw_background(game_display, "win_screen", settings)
    menu_font = pg.font.SysFont('Arial', round(30*(screen_size[1]/768)))
    text_array = [
        menu_font.render("Goal Limit: " + str(ruleset['goal_limit']), False, (255, 124, 0)),
        menu_font.render("Time Limit: " + str(ruleset['time_limit']), False, (255, 124, 0)),
        menu_font.render("Time Bonus: " + str(ruleset['time_bonus']), False, (255, 124, 0)),
        menu_font.render("NRG Charge Rate: " + str(ruleset['special_ability_charge_base']), False, (255, 124, 0)),
        menu_font.render("Danger Zone Enabled: " + str(ruleset['danger_zone_enabled']), False, (255, 124, 0)),
        menu_font.render("Reset to Default", False, (255, 124, 0)),
        menu_font.render("<-- Back", False, (255, 124, 0)),
    ]
    text_y = screen_size[1]//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (screen_size[0]//20, text_y)
        game_display.blit(text_box, text_rect)
        text_y += screen_size[1]//10

    ball = pg.image.load(cwd + "\\resources\\images\\soccer_ball.png")
    ball = pg.transform.scale(ball, (screen_size[1]//20, screen_size[1]//20))
    game_display.blit(ball, (screen_size[0]*(1/20), ((screen_size[1]//10) * selector_position) + (0.5 * screen_size[1]//10)))



p1_blob = []
p2_blob = []
timer = 0
ruleset = {
    'version': 'v0.5.0a',
    'goal_limit': 5,
    'time_limit': 3600,
    'time_bonus': 600,
    'special_ability_charge_base': 1,
    'danger_zone_enabled': True,
}
settings = {
    'hd_backgrounds': True,
    'hd_blobs': True,
}
game_stats = ()
previous_screen = ""
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
        if(game_state == "rules" or game_state == "settings"):
            previous_screen = "main_menu"
    elif(game_state == "casual_css"):
        info_getter = engine.main_menu.casual_css_navigation()
        p1_selector_position = info_getter[0]
        p2_selector_position = info_getter[1]
        draw_casual_css(screen_size, game_surface, p1_selector_position, p2_selector_position, settings)
        game_state = info_getter[2]
        if(game_state == "casual_match"):
            p1_selector_position[2] = 0
            p2_selector_position[2] = 0
            p1_blob = info_getter[3]
            p2_blob = info_getter[4]
        elif(game_state == "rules" or game_state == "settings"):
            previous_screen = "casual_css"
        elif(game_state == "main_menu"):
            timer = 10
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
            timer = 300
            return game_state
        draw_gameplay(screen_size, game_surface, p1_blob, p2_blob, ball, game_score, timer, game_time, settings)
    elif(game_state == "casual_win"):
        draw_win_screen(screen_size, game_surface, game_stats, settings)
        timer -= 1
        if(timer == 0):
            return "casual_css"
    elif(game_state == "rules"):
        info_getter = engine.main_menu.rules_navigation(timer, ruleset, previous_screen)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        draw_rules_screen(screen_size, game_surface, ruleset, selector_position, settings)
    elif(game_state == "settings"):
        info_getter = engine.main_menu.settings_navigation(timer, settings, previous_screen)
        selector_position = info_getter[0]
        game_state = info_getter[1]
        draw_settings_screen(game_surface, settings, selector_position)
    #print(selector_position)
    game_display.blit(pg.transform.scale(game_surface, (real_screen_size[0], real_screen_size[1])), (0, 0))
    pg.display.flip()
    return game_state