from os import getcwd
from resources.background_handler import draw_background as draw_background
from resources.display_particles import draw_ball_overlay, draw_ball_particles as draw_ball_particles, draw_blob_particles
from resources.display_particles import clear_particle_memory as clear_particle_memory
from math import ceil
import pygame as pg
cwd = getcwd()

image_cache = {"initialized": False}
def draw_blob(screen_size, game_display, blob):
    global image_cache

def draw_ball(screen_size, game_display, ball):
    global image_cache
    if not (ball.image == image_cache['ball_clone']):
        image_cache['ball'] = pg.transform.scale(pg.image.load(ball.image), (40, 40))
        image_cache['ball_clone'] = ball.image
    game_display.blit(image_cache['ball'], ((screen_size[0]/1366)*ball.x_pos * (1000/1366), (screen_size[1]/768) * ball.y_pos * (400/768)))

def draw_ui(screen_size, game_display, p1_blob, p2_blob):
    global image_cache
    ui_font = image_cache['ui_font']
    pg.draw.rect(game_display, (200, 200, 200), (10, 0, screen_size[0] * (70/1366), screen_size[0] * (70/1366)))
    game_display.blit(image_cache["heart_icon"], (10, 0))
    menu_text = ui_font.render(str(p1_blob.hp), False, (0, 255, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (45, 30)
    game_display.blit(menu_text, text_rect)
    pg.draw.rect(game_display, (200, 200, 200), (90, 0, screen_size[0] * (70/1366), screen_size[0] * (70/1366)))
    pg.draw.rect(game_display, (200, 200, 200), (170, 0, screen_size[0] * (70/1366), screen_size[0] * (70/1366)))
    game_display.blit(image_cache["kick_icon"], (170, 0))
    pg.draw.rect(game_display, (200, 200, 200), (250, 0, screen_size[0] * (70/1366), screen_size[0] * (70/1366)))
    game_display.blit(image_cache["block_icon"], (250, 0))
    pg.draw.rect(game_display, (200, 200, 200), (330, 0, screen_size[0] * (70/1366), screen_size[0] * (70/1366)))
    game_display.blit(image_cache["boost_icon"], (330, 0))
    
    pg.draw.rect(game_display, (200, 200, 200), (966, 0, 70, 70))
    game_display.blit(image_cache["heart_icon"], (966, 0))
    menu_text = ui_font.render(str(p2_blob.hp), False, (0, 255, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (1001, 30)
    game_display.blit(menu_text, text_rect)
    pg.draw.rect(game_display, (200, 200, 200), (1046, 0, 70, 70))
    pg.draw.rect(game_display, (200, 200, 200), (1126, 0, 70, 70))
    game_display.blit(image_cache["kick_icon"], (1126, 0))
    pg.draw.rect(game_display, (200, 200, 200), (1206, 0, 70, 70))
    game_display.blit(image_cache["block_icon"], (1206, 0))
    pg.draw.rect(game_display, (200, 200, 200), (1286, 0, 70, 70))
    game_display.blit(image_cache["boost_icon"], (1286, 0))

    nrg_surface = pg.Surface((390, 35), pg.SRCALPHA)
    p2_nrg_bar = nrg_surface.get_width() * p2_blob.special_ability_meter / p2_blob.special_ability_max
    if(p2_blob.special_ability_meter >= p2_blob.special_ability_cost):
        nrg_color = (0, 0, 255)
    else:
        nrg_color = (0, 0, 50)
    if(p2_blob.special_ability_meter >= p2_blob.boost_cost and not p2_blob.boost_cooldown_timer > 0):
        border_color = (255, 255, 0)
    else:
        border_color = (0, 0, 0)
    pg.draw.rect(nrg_surface, (124, 124, 124), (0, 0, nrg_surface.get_width(), nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, nrg_color, (nrg_surface.get_width() - (p2_nrg_bar), 0, p2_nrg_bar, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (0, 0, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, nrg_surface.get_height()-3, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, 0, 3, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (nrg_surface.get_width() - 3, 0, 3, nrg_surface.get_height()))
    game_display.blit(nrg_surface, (966, 75))

    menu_text = ui_font.render(("NRG: " + str(p2_blob.special_ability_meter)), False, (255, 255, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (4*screen_size[0]//5, screen_size[1]//9)
    game_display.blit(menu_text, text_rect)
    
    if(p2_blob.kick_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 70-p2_blob.kick_cooldown_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (1126, 0))
        menu_text = ui_font.render(str(p2_blob.kick_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (1162, 30)
        game_display.blit(menu_text, text_rect)
    
    if(p2_blob.block_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 70-p2_blob.block_cooldown_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (1206, 0))
        menu_text = ui_font.render(str(p2_blob.block_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (1242, 30)
        game_display.blit(menu_text, text_rect)

    if(p2_blob.boost_timer_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (0, 0, 255), (0, 70-p2_blob.boost_timer_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (1286, 0))
        menu_text = ui_font.render(str(p2_blob.boost_timer_visualization), False, (0, 255, 124))
        text_rect = menu_text.get_rect()
        text_rect.center = (1322, 30)
        game_display.blit(menu_text, text_rect)
    elif(p2_blob.boost_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 70-p2_blob.boost_cooldown_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (1286, 0))
        menu_text = ui_font.render(str(p2_blob.boost_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (1322, 30)
        game_display.blit(menu_text, text_rect)

    nrg_surface = pg.Surface((390, 35), pg.SRCALPHA)
    p1_nrg_bar = nrg_surface.get_width() * p1_blob.special_ability_meter / p1_blob.special_ability_max
    if(p1_blob.special_ability_meter >= p1_blob.special_ability_cost):
        nrg_color = (255, 0, 0)
    else:
        nrg_color = (50, 0, 0)
    if(p1_blob.special_ability_meter >= p1_blob.boost_cost and not p1_blob.boost_cooldown_timer > 0):
        border_color = (255, 255, 0)
    else:
        border_color = (0, 0, 0)
    pg.draw.rect(nrg_surface, (124, 124, 124), (0, 0, nrg_surface.get_width(), nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, nrg_color, (0, 0, p1_nrg_bar, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (0, 0, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, nrg_surface.get_height()-3, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, 0, 3, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (nrg_surface.get_width() - 3, 0, 3, nrg_surface.get_height()))
    game_display.blit(nrg_surface, (10, 75))

    menu_text = ui_font.render(("NRG: " + str(p1_blob.special_ability_meter)), False, (255, 255, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//5, screen_size[1]//9)
    game_display.blit(menu_text, text_rect)


    if(p1_blob.kick_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 70-p1_blob.kick_cooldown_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (170, 0))
        menu_text = ui_font.render(str(p1_blob.kick_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (206, 30)
        game_display.blit(menu_text, text_rect)
    
    if(p1_blob.block_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 70-p1_blob.block_cooldown_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (250, 0))
        menu_text = ui_font.render(str(p1_blob.block_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (286, 30)
        game_display.blit(menu_text, text_rect)

    if(p1_blob.boost_timer_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (0, 0, 255), (0, 70-p1_blob.boost_timer_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (330, 0))
        menu_text = ui_font.render(str(p1_blob.boost_timer_visualization), False, (0, 255, 124))
        text_rect = menu_text.get_rect()
        text_rect.center = (366, 30)
        game_display.blit(menu_text, text_rect)
    elif(p1_blob.boost_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 70-p1_blob.boost_cooldown_percentage*70, 70, 70))
        game_display.blit(cooldown_surface, (330, 0))
        menu_text = ui_font.render(str(p1_blob.boost_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (366, 30)
        game_display.blit(menu_text, text_rect)

def draw_timer(screen_size, game_display, timer):
    global image_cache
    if(timer > 0):
            timer_font = image_cache['menu_font']
            timer_text = timer_font.render(str(ceil(timer/6)/10), False, (220, 100, 2))
            text_rect = timer_text.get_rect()
            text_rect.center = (screen_size[0]//2, 2*screen_size[1]//7)
            game_display.blit(timer_text, text_rect)

def draw_gameplay(screen_size, game_display, p1_blob, p2_blob, ball, game_score, timer, game_time, settings):

    #TODO: Simplify and remove
    draw_background(game_display, "casual_match", settings)
    global cwd
    global image_cache
    if not image_cache['initialized']: #Load in the images so we don't keep importing them
        image_cache['initialized'] = True
        image_cache['ball'] = pg.transform.scale(pg.image.load(ball.image), (40, 40))
        image_cache['ball_clone'] = ball.image
        image_cache['p1_blob'] = pg.transform.scale(pg.image.load(p1_blob.image).convert_alpha(), (120, 66))
        image_cache['p1_blob_clone'] = p1_blob.image
        image_cache['p2_blob'] = pg.transform.scale(pg.image.load(p2_blob.image).convert_alpha(), (120, 66))
        image_cache['p2_blob_clone'] = p2_blob.image
        image_cache['p2_darkened'] = False
        image_cache['blob_special'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\blobs\\special_blob.png"), (180, 99)).convert_alpha()
        image_cache['kick_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\kick_icon.png"), (70, 70))
        image_cache['block_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\block_icon.png"), (70, 70))
        image_cache['boost_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\boost_icon.png"), (70, 70))
        image_cache['heart_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\heart_icon.png"), (70, 70))
        image_cache['menu_font'] = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", 25)
        image_cache['ui_font'] = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", 25)

    if not (p1_blob.image == image_cache['p1_blob_clone']):
        image_cache['p1_blob'] = pg.transform.scale(pg.image.load(p1_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p1_blob_clone'] = p1_blob.image

    if(p1_blob.facing == "right"):
        game_display.blit(pg.transform.flip(image_cache['p1_blob'], True, False), ((screen_size[0]/1366)*p1_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(400/768))))
    else:
        game_display.blit(image_cache['p1_blob'], ((screen_size[0]/1366)*p1_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(400/768))))

    if(p1_blob.boost_timer):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 255, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((p1_blob.x_pos - 42)*(1000/1366), (p1_blob.y_pos*(382/768))))

    if(p1_blob.focusing):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))
    if(p1_blob.block_timer):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((0, 0, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))
        p1_block_surface = pg.Surface((screen_size[0] * 110/1366, screen_size[1]*(220/768)), pg.SRCALPHA)
        p1_block_surface.set_alpha(124)
        if(p1_blob.block_timer < p1_blob.block_timer_max - 3):
            p1_block_surface.set_alpha(124 - 10 * (p1_blob.block_timer_max - p1_blob.block_timer))
        pg.draw.rect(p1_block_surface, (0, 0, 255), (0, 0, screen_size[0] * 110/1366, screen_size[1]*(220/768)), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
        #TODO: Scaling based off of block size
        if(p1_blob.facing == 'left'):
            #Grab Box Visualization
            game_display.blit(p1_block_surface, ((screen_size[0]/1366)*(p1_blob.x_pos - 150)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos - 105)*(382/768)))
        else:
            game_display.blit(p1_block_surface, ((screen_size[0]/1366)*(p1_blob.x_pos + 186)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos - 105)*(382/768)))
    if(p1_blob.kick_visualization):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        blob_special.set_alpha(255 - 16 * (p1_blob.kick_visualization_max - p1_blob.kick_visualization))
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))

    draw_blob_particles(game_display, ball, p1_blob)
    
    if not (p2_blob.image == image_cache['p2_blob_clone']):
        image_cache['p2_blob'] = pg.transform.scale(pg.image.load(p2_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p2_blob_clone'] = p2_blob.image
        image_cache['p2_darkened'] = False

    if(p2_blob.species == p1_blob.species):
        if(not image_cache['p2_darkened']):
            image_cache['p2_blob'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
            image_cache['p2_darkened'] = True

    if(p2_blob.facing == "right"):
        game_display.blit(pg.transform.flip(image_cache['p2_blob'], True, False), ((screen_size[0]/1366)*p2_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(400/768))))
    else:
        game_display.blit(image_cache['p2_blob'], ((screen_size[0]/1366)*p2_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(400/768))))

    if(p2_blob.focusing):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))
    if(p2_blob.block_timer):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((0, 0, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))
        p2_block_surface = pg.Surface((screen_size[0] * 110/1366, screen_size[1]*(220/768)), pg.SRCALPHA)
        p2_block_surface.set_alpha(124)
        if(p2_blob.block_timer < p2_blob.block_timer_max - 3):
            p2_block_surface.set_alpha(124 - 10 * (p2_blob.block_timer_max - p2_blob.block_timer))
        pg.draw.rect(p2_block_surface, (0, 0, 255), (0, 0, screen_size[0] * 110/1366, screen_size[1]*(220/768)), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
        #TODO: Scaling based off of block size
        if(p2_blob.facing == 'left'):
            #Grab Box Visualization
            game_display.blit(p2_block_surface, ((screen_size[0]/1366)*(p2_blob.x_pos - 150)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos - 105)*(382/768)))
        else:
            game_display.blit(p2_block_surface, ((screen_size[0]/1366)*(p2_blob.x_pos + 186)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos - 105)*(382/768)))
    if(p2_blob.kick_visualization):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        blob_special.set_alpha(255 - 16 * (p2_blob.kick_visualization_max - p2_blob.kick_visualization))
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))
    if(p2_blob.boost_timer):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 255, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))

    draw_blob_particles(game_display, ball, p2_blob)

    #fade_out = 200
    draw_ball_particles(screen_size, game_display, ball, p1_blob, p2_blob)
    draw_ball(screen_size, game_display, ball)
    draw_ball_overlay(screen_size, game_display, ball, p1_blob, p2_blob)

    menu_font = image_cache['menu_font']
    menu_text = menu_font.render("SCORE: "+ str(game_score[0]) + "-" + str(game_score[1]), False, (200, 230, 200))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//2, 0.75*screen_size[1]//14)
    game_display.blit(menu_text, text_rect)
    try:
        menu_text = menu_font.render("TIME: "+ '{:.2f}'.format(round(game_time/60, 2)), False, (200, 230, 200))
    except:
        menu_text = menu_font.render("NO TIME LIMIT", False, (0, 0, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//2, 1.5*screen_size[1]//14)
    game_display.blit(menu_text, text_rect)
    
    draw_ui(screen_size, game_display, p1_blob, p2_blob)    

    draw_timer(screen_size, game_display, timer)

def draw_win_screen(screen_size, game_display, game_stats, settings):
    draw_background(game_display, "win_screen", settings)
    clear_particle_memory()
    menu_font = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", round(50*(screen_size[1]/768)))
    if(game_stats == 3):
        menu_text = menu_font.render("TIE", False, (0, 0, 255))
    else:
        menu_text = menu_font.render("WINNER: "+ str(game_stats), False, (0, 0, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//2, screen_size[1]//7)
    game_display.blit(menu_text, text_rect)
