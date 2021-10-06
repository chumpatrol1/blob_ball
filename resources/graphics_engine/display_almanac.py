from engine.blobs import Blob
from resources.graphics_engine.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd

blob_array = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/blobs/quirkless_blob.png", "Quirkless Blob", "quirkless"], ["/blobs/fire_blob.png", "Fire Blob", "fire"], ["/blobs/ice_blob.png", "Ice Blob", "ice"], ["/blobs/water_blob.png", "Water Blob", "water"], ["/blobs/rock_blob.png", "Rock Blob", "rock"], ["/blobs/lightning_blob.png", "Lightning Blob", "lightning"], ["/blobs/wind_blob.png", "Wind Blob", "wind"],],
[["/blobs/judge_blob.png", "Judge Blob", "judge"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
]

bic_cached = False
blob_image_cache = [
]
ball = None
ball_state = 'deselected'
mu_chart = None

def load_blobs(blob_image_cache, directory):
    for row in blob_array: #Temporary, until we make more blobs
        blob_image_cache.append([])
        for icon in row:
            blob_image_cache[-1].append(pg.image.load(directory+icon[0]))
    return blob_image_cache

cwd = getcwd()

def draw_almanac_main(game_display, selector_position, settings):
    draw_background(game_display, 'almanac', settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_array = [
        menu_font.render('Blobs and Info', False, (0, 0, 150)),
        menu_font.render('Medals', False, (0, 0, 150)),
        menu_font.render('Game Statistics', False, (0, 0, 150)),
        menu_font.render('Art', False, (0, 0, 150)),
        menu_font.render('Credits', False, (0, 0, 150)),
        menu_font.render('Back', False, (0, 0, 150))
    ]


    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (76, 76))
    game_display.blit(ball, (875, ((76 * selector_position) + (0.5 * 76))))

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

def draw_almanac_stats(game_display, settings):
    draw_background(game_display, 'almanac_stats', settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    tiny_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    from json import loads
    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())
    text_array = [
        menu_font.render('Lifetime Statistics', False, (0, 0, 150)),
    ]
    general_text = [
        tiny_font.render('General Statistics', False, (0, 0, 150)),
        tiny_font.render('Time In Match: ' + str(game_stats['time_in_game']), False, (0, 0, 150)),
        tiny_font.render('Blobs Unlocked: ' + str(game_stats['blobs_unlocked']), False, (0, 0, 150)),
        tiny_font.render('Costumes Unlocked: ' + str(game_stats['costumes_unlocked']), False, (0, 0, 150)),
        tiny_font.render('Backgrounds Unlocked: ' + str(game_stats['backgrounds_unlocked']), False, (0, 0, 150)),
        tiny_font.render('Most Played Blob: ' + game_stats['most_played_character'], False, (0, 0, 150)),
    ]
    match_text = [
        tiny_font.render('Match Statistics', False, (0, 0, 150)),
        tiny_font.render('Matches Played: ' + str(game_stats['matches_played']), False, (0, 0, 150)),
        tiny_font.render('Points Scored: ' + str(game_stats['points_scored']), False, (0, 0, 150)),
        tiny_font.render('Points from KOs: ' + str(game_stats['points_from_kos']), False, (0, 0, 150)),
        tiny_font.render('Points from Goals: ' + str(game_stats['points_from_goals']), False, (0, 0, 150)),
    ]

    blob_text = [
        tiny_font.render('Blob Statistics', False, (0, 0, 150)),
        tiny_font.render('Wavebounces: ' + str(game_stats['wavebounces']), False, (0, 0, 150)),
        tiny_font.render('Jumps: ' + str(game_stats['jumps']), False, (0, 0, 150)),
        tiny_font.render('Jump Cancelled Focuses: ' + str(game_stats['jump_cancelled_focuses']), False, (0, 0, 150)),
        tiny_font.render('Time Focused: ' + str(game_stats['time_focused_seconds']), False, (0, 0, 150)),
        tiny_font.render('Damage Dealt: ' + str(game_stats['damage_dealt']), False, (0, 0, 150)),
        tiny_font.render('Parries: ' + str(game_stats['parries']), False, (0, 0, 150)),
        tiny_font.render('Clanks: ' + str(game_stats['clanks']), False, (0, 0, 150)),
        tiny_font.render('Kicks: ' + str(game_stats['kick_count']), False, (0, 0, 150)),
        tiny_font.render('Blocks: ' + str(game_stats['block_count']), False, (0, 0, 150)),
        tiny_font.render('Boosts: ' + str(game_stats['boost_count']), False, (0, 0, 150)),
    ]

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76
    text_y = 120
    for text_box in general_text:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40
    text_y += 40
    for text_box in match_text:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40
    text_y = 120
    for text_box in blob_text:
        text_rect = text_box.get_rect()
        text_rect.topleft = (550, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40
    text_y = 120

def draw_almanac_stats_2(game_display, settings):
    draw_background(game_display, 'almanac_stats', settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    tiny_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    from json import loads
    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())
    text_array = [
        menu_font.render('Lifetime Statistics', False, (0, 0, 150)),
    ]
    general_text = [
        tiny_font.render('General Statistics', False, (0, 0, 150)),
        tiny_font.render('Times Game Started: ' + str(game_stats['times_bb_started']), False, (0, 0, 150)),
        tiny_font.render('Time Open: ' + str(game_stats['time_open']), False, (0, 0, 150)),
        tiny_font.render('First Played Version: ' + game_stats['original_version'], False, (0, 0, 150)),
    ]

    blob_text = [
        tiny_font.render('Blob Statistics', False, (0, 0, 150)),
        tiny_font.render('X Distance Moved: ' + str(game_stats['blob_x_distance_moved']), False, (0, 0, 150)),
        tiny_font.render('Time Grounded: ' + str(game_stats['time_grounded_seconds']), False, (0, 0, 150)),
        tiny_font.render('Time Airborne: ' + str(game_stats['time_airborne_seconds']), False, (0, 0, 150)),
    ]

    ball_text = [
        tiny_font.render('Ball Statistics', False, (0, 0, 150)),
        tiny_font.render('Wall Collisions: ' + str(game_stats['ball_wall_collisions']), False, (0, 0, 150)),
        tiny_font.render('Ceiling Collisions: ' + str(game_stats['ball_ceiling_collisions']), False, (0, 0, 150)),
        tiny_font.render('Floor Collisions: ' + str(game_stats['ball_floor_collisions']), False, (0, 0, 150)),
        tiny_font.render('Goal Collisions: ' + str(game_stats['ball_goal_collisions']), False, (0, 0, 150)),
        tiny_font.render('Blob Standard Collisions: ' + str(game_stats['blob_standard_collisions']), False, (0, 0, 150)),
        tiny_font.render('Blob Reflect Collisions: ' + str(game_stats['blob_reflect_collisions']), False, (0, 0, 150)),
        tiny_font.render('Blob Warp Collisions: ' + str(game_stats['blob_warp_collisions']), False, (0, 0, 150)),
        tiny_font.render('Kicked: ' + str(game_stats['ball_kicked']), False, (0, 0, 150)),
        tiny_font.render('Blocked: ' + str(game_stats['ball_blocked']), False, (0, 0, 150)),
        tiny_font.render('X Distance Moved: ' + str(game_stats['ball_x_distance_moved']), False, (0, 0, 150)),
        tiny_font.render('Y Distance Moved: ' + str(game_stats['ball_y_distance_moved']), False, (0, 0, 150)),
    ]

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76
    text_y = 120
    for text_box in general_text:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40

    text_y += 40
    for text_box in blob_text:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40
    text_y = 120
    for text_box in ball_text:
        text_rect = text_box.get_rect()
        text_rect.topleft = (750, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40

def load_mu_chart():
    global mu_chart
    from json import loads
    with open(cwd+'/saves/matchup_chart.txt', 'r') as muchart:
        mu_chart = loads(muchart.readline())
    return mu_chart

def read_mu_chart(blob):
    #Reads the MU chart.
    global mu_chart
    global blob_array
    mu_percent_array = []
    if(blob in mu_chart):
        for row in blob_array:
            mu_percent_array.append([])
            for blob_item in row:
                if(blob_item[2] in mu_chart[blob]):
                    record = mu_chart[blob][blob_item[2]]
                    win_rate = record[0]
                    win_rate = round(win_rate / (record[0] + record[1] + record[2]) * 100, 2)
                    win_rate = str(win_rate) + "%"
                    mu_percent_array[-1].append(win_rate)
                else:
                    mu_percent_array[-1].append("-")
    else:
        for i in range(5):
            mu_percent_array.append([])
            for j in range(7):
                mu_percent_array[-1].append("-")
    return mu_percent_array

def draw_almanac_stats_3(game_display, settings, selector_position):
    draw_background(game_display, 'almanac_stats', settings)
    global bic_cached
    global blob_image_cache
    global ball
    global ball_state
    directory = cwd + "/resources/images"
    if not bic_cached:
        blob_image_cache = load_blobs(blob_image_cache, directory)
        bic_cached = True
        ball = pg.transform.scale(pg.image.load(directory+"/balls/soccer_ball.png"), (50, 50))

    x = 0
    y = 0
    for row in blob_image_cache: #Temporary, until we make more blobs
        for icon in row:
            blob = blob_image_cache[y][x]
            blob = pg.transform.scale(blob, (122, 68))
            game_display.blit(blob, (1366*((x + 0.5)/8)+ 20, ((y + 0.5) * 100)))
            x += 1
        x = 0
        y += 1
    if(selector_position[2] == 1 and ball_state == "deselected"):
        ball_state = "selected"
        ball = ball = pg.transform.scale(pg.image.load(directory+"/balls/goal_ball.png"), (50, 50))
        load_mu_chart()
    if(selector_position[2] == 0 and ball_state == "selected"):
        ball_state = "deselected"
        ball = pg.transform.scale(pg.image.load(directory+"/balls/soccer_ball.png"), (50, 50))
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    if(selector_position[2] == 1):
        mu_chart_text = read_mu_chart(blob_array[selector_position[1]][selector_position[0]][2])
        
        text_x = 170
        text_y = 130
        for row in mu_chart_text:
            for mu in row:
                text_box = menu_font.render(mu, False, (255, 255, 255))
                text_rect = text_box.get_rect()
                text_rect.center = (text_x, text_y)
                game_display.blit(text_box, text_rect)
                text_x += 170
            text_y += 100
            text_x = 170
    game_display.blit(ball, ((selector_position[0] + 0.85) * 170, (selector_position[1] + 0.5) * 100))
    game_display.blit(blob_image_cache[selector_position[1]][selector_position[0]], (825, 575))

    text_array = [
        menu_font.render("INSTRUCTIONS: Use movement keys", False, (0, 0, 255)),
        menu_font.render("to navigate the screen. Press", False, (0, 0, 255)),
        menu_font.render("Ability/Select to view the winrate", False, (0, 0, 255)),
        menu_font.render("of a blob compared to others.", False, (0, 0, 255)),
        menu_font.render("Select the middlemost blob to return", False, (0, 0, 255)),
        menu_font.render("   to the almanac.", False, (0, 0, 255)),
    ]

    text_y = 530
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 30

    text_box = menu_font.render(blob_array[selector_position[1]][selector_position[0]][1], False, (0, 0, 255))
    text_rect = text_box.get_rect()
    text_rect.center = (925, 700)
    game_display.blit(text_box, text_rect)

def draw_almanac_credits(game_display, settings):
    draw_background(game_display, 'credits', settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 23)
    text_array = [
        menu_font.render('Game Developers', False, (0, 0, 150)),
        menu_font.render('Elijah "Chumpatrol1" McLaughlin (Lead Programmer, Lead Designer)', False, (0, 0, 150)),
        menu_font.render('Ellexium (Lead Artist, Programmer)', False, (0, 0, 150)),
        menu_font.render('Zion "Chumpatrol2" McLaughlin (Game Balancer, Bug Hunter)', False, (0, 0, 150)),
        menu_font.render('Yael "Chumpatrol3" McLaughlin (Blob and Concept Artist)', False, (0, 0, 150)),
        menu_font.render('NeoPhyte_TPK (Contributor, Bug Hunter)', False, (0, 0, 150)),
        menu_font.render('BoingK (Lead Musician, CPU Programmer)', False, (0, 0, 150)),
    ]

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

def draw_almanac_art(game_display, selector_position, settings):
    draw_background(game_display, 'almanac', settings)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_array = [
        menu_font.render('Backgrounds', False, (0, 0, 150)),
        menu_font.render('Blobs and Icons', False, (0, 0, 150)),
        menu_font.render('Fan Creations', False, (0, 0, 150)),
        menu_font.render('Sound Test', False, (0, 0, 150)),
        menu_font.render('Music Test', False, (0, 0, 150)),
        menu_font.render('Back', False, (0, 0, 150)),
        menu_font.render('Navigate Art Menus with Left and Right', False, (0, 0, 150)),
        menu_font.render('Go back with "Ability" or "Kick"', False, (0, 0, 150)),
        menu_font.render('Sound Menus Unavailable', False, (0, 0, 150)),
    ]


    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (76, 76))
    game_display.blit(ball, (875, ((76 * selector_position) + (0.5 * 76))))

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76
    return

def draw_almanac_backgrounds(game_display, selector_position):
    if(selector_position == 0):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'green_background', settings)
    elif(selector_position == 1):
        settings = {'hd_backgrounds': False,}
        draw_background(game_display, 'casual_match', settings)
    elif(selector_position == 2):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'css', settings)
    elif(selector_position == 3):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'casual_match', settings)
    elif(selector_position == 4):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'rules', settings)
    elif(selector_position == 5):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'settings', settings)
    elif(selector_position == 6):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'almanac', settings)

blob_cached = False
blob_cache = []
def draw_almanac_blobs(game_display, selector_position):
    global blob_cached
    global blob_cache
    if not blob_cached:
        #from resources.display_css import load_blobs
        directory = cwd + "/resources/images"
        blob_cache = load_blobs(blob_cache, directory)
        temp_cache = []
        for row in blob_cache:
            temp_cache = temp_cache + row
        blob_cache = temp_cache
        blob_cached = True
        
    settings = {'hd_backgrounds': False,}
    draw_background(game_display, 'green_background', settings)
    game_display.blit(blob_cache[selector_position], (200, 200))