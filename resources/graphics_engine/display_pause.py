import pygame as pg
from os import getcwd, getenv
cwd = getcwd()
appcwd = getenv('APPDATA')+"/BlobBall"
snapshot = None
ball = pg.transform.scale(pg.image.load(cwd + "/resources/images/balls/soccer_ball.png"), (76, 76))
shader = pg.Surface((1366, 768), pg.SRCALPHA)
shader.fill((0, 0, 0, 100))

def capture_gameplay(game_surface):
    global snapshot
    snapshot = game_surface.copy()

def take_screenshot():
    global snapshot
    import time
    current_time = time.localtime()
    time_str = f"{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} {current_time.tm_hour}.{current_time.tm_min}.{current_time.tm_sec}_"
    identifier = 1
    file_str = appcwd + '/screenshots/Blob Ball Screenshot ' + time_str + str(identifier)
    from os.path import exists
    while exists(file_str + ".png"):
        identifier += 1
        file_str = appcwd + '/screenshots/Blob Ball Screenshot ' + time_str + str(identifier)
    
    pg.image.save(snapshot, file_str + ".png")

def draw_pause_background(game_surface):
    global snapshot
    game_surface.blit(snapshot, (0, 0))

def draw_pause_screen(game_display, info_getter, settings):
    selector_position = info_getter[0]
    game_display.blit(shader, (0, 0))
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
    text_array = [
        menu_font.render('Press Escape/Home/Pause to Resume', False, (0, 0, 150)),
        menu_font.render('Screenshot', False, (0, 0, 150)),
        menu_font.render('Music Volume: ' + str(settings['music_volume']), False, (0, 0, 150)),
        menu_font.render('Sound Volume: ' + str(settings['sound_volume']), False, (0, 0, 150)),
        menu_font.render('Quit', False, (0, 0, 150))
    ]

    game_display.blit(ball, (300, (76 * selector_position) + 114))

    text_y = 162
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76