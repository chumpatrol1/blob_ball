from os import getcwd
from resources.background_handler import draw_background as draw_background
from math import ceil
import pygame as pg
cwd = getcwd()

image_cache = {"initialized": False}
def draw_blob(screen_size, game_display, blob):
    global image_cache
    
def draw_ui(screen_size, game_display, p1_blob, p2_blob):
    global image_cache
    ui_font = pg.font.SysFont('Arial', round(35*(screen_size[1]/768)))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (1/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["heart_icon"], (screen_size[0]*(1/20), 0))
    menu_text = ui_font.render(str(p2_blob.hp), False, (0, 255, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0] * (1.37/20), screen_size[1] * (0.65/20))
    game_display.blit(menu_text, text_rect)
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (2/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (3/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["kick_icon"], (screen_size[0]*(3/20), 0))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (4/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["block_icon"], (screen_size[0]*(4/20), 0))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (5/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["boost_icon"], (screen_size[0]*(5/20), 0))
    
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (14/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["heart_icon"], (screen_size[0]*(14/20), 0))
    menu_text = ui_font.render(str(p1_blob.hp), False, (0, 255, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0] * (14.37/20), screen_size[1] * (0.65/20))
    game_display.blit(menu_text, text_rect)
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (15/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (16/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["kick_icon"], (screen_size[0]*(16/20), 0))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (17/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["block_icon"], (screen_size[0]*(17/20), 0))
    pg.draw.rect(game_display, (200, 200, 200), (screen_size[0] * (18/20), 0, screen_size[0] * (50/1366), screen_size[0] * (50/1366)))
    game_display.blit(image_cache["boost_icon"], (screen_size[0]*(18/20), 0))

    nrg_surface = pg.Surface((screen_size[0]*(323/1366), screen_size[1]*(50/768)), pg.SRCALPHA)
    p1_nrg_bar = 323 * p1_blob.special_ability_meter / p1_blob.special_ability_max
    if(p1_blob.special_ability_meter >= p1_blob.special_ability_cost):
        nrg_color = (255, 0, 0)
    else:
        nrg_color = (100, 0, 0)
    if(p1_blob.special_ability_meter >= p1_blob.boost_cost and not p1_blob.boost_cooldown_timer > 0):
        border_color = (255, 255, 0)
    else:
        border_color = (0, 0, 0)
    pg.draw.rect(nrg_surface, (124, 124, 124), (0, 0, nrg_surface.get_width(), nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, nrg_color, (screen_size[0]*(323/1366) - (p1_nrg_bar), 0, p1_nrg_bar, screen_size[1]*(50/768)))
    pg.draw.rect(nrg_surface, border_color, (0, 0, nrg_surface.get_width(), 3*nrg_surface.get_height()/50))
    pg.draw.rect(nrg_surface, border_color, (0, 47*nrg_surface.get_height()/50, nrg_surface.get_width(), 3*nrg_surface.get_height()/50))
    pg.draw.rect(nrg_surface, border_color, (0, 0, 3*nrg_surface.get_width()/323, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (320*nrg_surface.get_width()/323, 0, 3*nrg_surface.get_width()/323, nrg_surface.get_height()))
    game_display.blit(nrg_surface, (screen_size[0]*(14/20), screen_size[1]*50/768))

    menu_text = ui_font.render(("NRG: " + str(p1_blob.special_ability_meter)), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (4*screen_size[0]//5, screen_size[1]//9)
    game_display.blit(menu_text, text_rect)
    
    if(p1_blob.kick_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 50-p1_blob.kick_cooldown_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(16/20), 0))
        menu_text = ui_font.render(str(p1_blob.kick_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(16.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)
    
    if(p1_blob.block_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 50-p1_blob.block_cooldown_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(17/20), 0))
        menu_text = ui_font.render(str(p1_blob.block_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(17.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)

    if(p1_blob.boost_timer_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (255, 124, 0), (0, 50-p1_blob.boost_timer_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(18/20), 0))
        menu_text = ui_font.render(str(p1_blob.boost_timer_visualization), False, (0, 255, 124))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(18.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)
    elif(p1_blob.boost_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 50-p1_blob.boost_cooldown_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(18/20), 0))
        menu_text = ui_font.render(str(p1_blob.boost_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(18.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)

    nrg_surface = pg.Surface((screen_size[0]*(323/1366), screen_size[1]*(50/768)), pg.SRCALPHA)
    p2_nrg_bar = 323 * p2_blob.special_ability_meter / p2_blob.special_ability_max
    if(p2_blob.special_ability_meter >= p2_blob.special_ability_cost):
        nrg_color = (0, 0, 255)
    else:
        nrg_color = (0, 0, 100)
    if(p2_blob.special_ability_meter >= p2_blob.boost_cost and not p2_blob.boost_cooldown_timer > 0):
        border_color = (255, 255, 0)
    else:
        border_color = (0, 0, 0)
    pg.draw.rect(nrg_surface, (124, 124, 124), (0, 0, nrg_surface.get_width(), nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, nrg_color, (0, 0, p2_nrg_bar, screen_size[1]*(50/768)))
    pg.draw.rect(nrg_surface, border_color, (0, 0, nrg_surface.get_width(), 3*nrg_surface.get_height()/50))
    pg.draw.rect(nrg_surface, border_color, (0, 47*nrg_surface.get_height()/50, nrg_surface.get_width(), 3*nrg_surface.get_height()/50))
    pg.draw.rect(nrg_surface, border_color, (0, 0, 3*nrg_surface.get_width()/323, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (320*nrg_surface.get_width()/323, 0, 3*nrg_surface.get_width()/323, nrg_surface.get_height()))
    game_display.blit(nrg_surface, (screen_size[0]*(1/20), screen_size[1]*50/768))

    menu_text = ui_font.render(("NRG: " + str(p2_blob.special_ability_meter)), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//5, screen_size[1]//9)
    game_display.blit(menu_text, text_rect)


    if(p2_blob.kick_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 50-p2_blob.kick_cooldown_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(3/20), 0))
        menu_text = ui_font.render(str(p2_blob.kick_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(3.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)
    
    if(p2_blob.block_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 50-p2_blob.block_cooldown_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(4/20), 0))
        menu_text = ui_font.render(str(p2_blob.block_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(4.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)

    if(p2_blob.boost_timer_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (255, 124, 0), (0, 50-p2_blob.boost_timer_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(5/20), 0))
        menu_text = ui_font.render(str(p2_blob.boost_timer_visualization), False, (0, 255, 124))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(5.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)
    elif(p2_blob.boost_cooldown_visualization > 0):
        cooldown_surface = pg.Surface((screen_size[0] * 50/1366, screen_size[0]*(50/1366)), pg.SRCALPHA)
        cooldown_surface.set_alpha(124)
        pg.draw.rect(cooldown_surface, (50, 50, 50), (0, 50-p2_blob.boost_cooldown_percentage*50, screen_size[0] * 50/1366, screen_size[0]*(50/1366)))
        game_display.blit(cooldown_surface, (screen_size[0]*(5/20), 0))
        menu_text = ui_font.render(str(p2_blob.boost_cooldown_visualization), False, (0, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]*(5.35/20), screen_size[1] * (0.6)/20)
        game_display.blit(menu_text, text_rect)

def draw_timer(screen_size, game_display, timer):
    if(timer > 0):
            timer_font = pg.font.SysFont('Arial', round(35*(screen_size[1]/768)))
            timer_text = timer_font.render(str(ceil(timer/6)/10), False, (255, 124, 0))
            text_rect = timer_text.get_rect()
            text_rect.center = (screen_size[0]//2, 2*screen_size[1]//7)
            game_display.blit(timer_text, text_rect)

def draw_gameplay(screen_size, game_display, p1_blob, p2_blob, ball, game_score, timer, game_time):
    #TODO: Simplify and remove
    draw_background(screen_size, game_display, "casual_match")
    global cwd
    global image_cache
    if not image_cache['initialized']: #Load in the images so we don't keep importing them
        image_cache['initialized'] = True
        image_cache['ball'] = pg.transform.scale(pg.image.load(ball.image), (round(screen_size[0]*(40/1366)), round(screen_size[1]*(40/768))))
        image_cache['ball_clone'] = ball.image
        image_cache['p1_blob'] = pg.transform.scale(pg.image.load(p1_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p1_blob_clone'] = p1_blob.image
        image_cache['p2_blob'] = pg.transform.scale(pg.image.load(p2_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p2_blob_clone'] = p2_blob.image
        image_cache['p2_darkened'] = False
        image_cache['kick_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\kick_icon.png"), (round(screen_size[0]*(50/1366)), round(screen_size[0]*(50/1366))))
        image_cache['block_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\block_icon.png"), (round(screen_size[0]*(50/1366)), round(screen_size[0]*(50/1366))))
        image_cache['boost_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\boost_icon.png"), (round(screen_size[0]*(50/1366)), round(screen_size[0]*(50/1366))))
        image_cache['heart_icon'] = pg.transform.scale(pg.image.load(cwd + "\\resources\\images\\heart_icon.png"), (round(screen_size[0]*(50/1366)), round(screen_size[0]*(50/1366))))

    blob_special = pg.image.load(cwd + "\\resources\\images\\blobs\\special_blob.png")
    blob_special = blob_special.convert_alpha()

    if not (p1_blob.image == image_cache['p1_blob_clone']):
        image_cache['p1_blob'] = pg.transform.scale(pg.image.load(p1_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p1_blob_clone'] = p1_blob.image

    if(p1_blob.facing == "right"):
        game_display.blit(pg.transform.flip(image_cache['p1_blob'], True, False), ((screen_size[0]/1366)*p1_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(400/768))))
    else:
        game_display.blit(image_cache['p1_blob'], ((screen_size[0]/1366)*p1_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(400/768))))
    
    if(p1_blob.boost_timer):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((255, 255, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))
    if(p1_blob.focusing):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((255, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))
    if(p1_blob.block_timer):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((0, 0, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))
        p1_block_surface = pg.Surface((screen_size[0] * 96/1366, screen_size[1]*(220/768)), pg.SRCALPHA)
        p1_block_surface.set_alpha(124)
        pg.draw.rect(p1_block_surface, (0, 0, 255), (0, 0, screen_size[0] * 96/1366, screen_size[1]*(220/768)), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
        #TODO: Scaling based off of block size
        if(p1_blob.facing == 'left'):
            #Grab Box Visualization
            game_display.blit(p1_block_surface, ((screen_size[0]/1366)*(p1_blob.x_pos - 150)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos - 105)*(382/768)))
        else:
            game_display.blit(p1_block_surface, ((screen_size[0]/1366)*(p1_blob.x_pos + 186)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos - 105)*(382/768)))
    if(p1_blob.kick_visualization):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p1_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(382/768))))
    
    if not (p2_blob.image == image_cache['p2_blob_clone']):
        image_cache['p2_blob'] = pg.transform.scale(pg.image.load(p2_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p2_blob_clone'] = p2_blob.image
        image_cache['p2_darkened'] = False

    if(p2_blob.type == p1_blob.type):
        if(not image_cache['p2_darkened']):
            image_cache['p2_blob'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
            image_cache['p2_darkened'] = True

    if(p2_blob.facing == "right"):
        game_display.blit(pg.transform.flip(image_cache['p2_blob'], True, False), ((screen_size[0]/1366)*p2_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(400/768))))
    else:
        game_display.blit(image_cache['p2_blob'], ((screen_size[0]/1366)*p2_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(400/768))))
    
    blob_special = pg.image.load(cwd + "\\resources\\images\\blobs\\special_blob.png")
    blob_special = blob_special.convert_alpha()

    if(p2_blob.focusing):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((255, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))
    if(p2_blob.block_timer):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((0, 0, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))
        p2_block_surface = pg.Surface((screen_size[0] * 96/1366, screen_size[1]*(220/768)), pg.SRCALPHA)
        p2_block_surface.set_alpha(124)
        pg.draw.rect(p2_block_surface, (0, 0, 255), (0, 0, screen_size[0] * 96/1366, screen_size[1]*(220/768)), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
        #TODO: Scaling based off of block size
        if(p2_blob.facing == 'left'):
            #Grab Box Visualization
            game_display.blit(p2_block_surface, ((screen_size[0]/1366)*(p2_blob.x_pos - 150)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos - 105)*(382/768)))
        else:
            game_display.blit(p2_block_surface, ((screen_size[0]/1366)*(p2_blob.x_pos + 186)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos - 105)*(382/768)))
    if(p2_blob.kick_visualization):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))
    if(p2_blob.boost_timer):
        blob_special = pg.transform.scale(blob_special, (round(screen_size[0]*(180/1366)), round(screen_size[1]*(99/768))))
        blob_special.fill((255, 255, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((screen_size[0]/1366)*(p2_blob.x_pos - 42)*(1000/1366), (screen_size[1]/768)*(p2_blob.y_pos*(382/768))))

    if not (ball.image == image_cache['ball_clone']):
        image_cache['ball'] = pg.transform.scale(pg.image.load(ball.image), (round(screen_size[0]*(40/1366)), round(screen_size[1]*(40/768))))
        image_cache['ball_clone'] = ball.image
    game_display.blit(image_cache['ball'], ((screen_size[0]/1366)*ball.x_pos * (1000/1366), (screen_size[1]/768) * ball.y_pos * (400/768)))
    #fade_out = 200

    #DISABLED DUE TO LAG
    '''for frame in ball.previous_locations:
        if(frame[2] >= 35):
            afterimage = pg.image.load(engine.ball.type_to_image(frame[3]))
            afterimage = pg.transform.scale(afterimage, (round(screen_size[0]*(40/1366)), round(screen_size[1]*(40/768))))
            afterimage = afterimage.convert_alpha()
            real_fade = fade_out
            afterimage.set_alpha(real_fade)
            game_display.blit(afterimage, ((screen_size[0]/1366)*frame[0] * (1000/1366), (screen_size[1]/768) * frame[1] * (400/768)))
        fade_out -= 20'''
        
    if(p1_blob.used_ability == "fireball" or p2_blob.used_ability == "fireball"):
        fireball_image = pg.image.load(cwd + "\\resources\\images\\special_ball.png")
        fireball_image = fireball_image.convert_alpha()
        fireball_image = pg.transform.scale(fireball_image, (round(screen_size[0]*(40/1366)), round(screen_size[1]*(40/768))))
        fireball_image.fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(fireball_image, ((screen_size[0]/1366)*ball.x_pos * (1000/1366), (screen_size[1]/768) * ball.y_pos * (400/768)))
    if(p1_blob.used_ability == "snowball" or p2_blob.used_ability == "snowball"):
        snowball_image = pg.image.load(cwd + "\\resources\\images\\special_ball.png")
        snowball_image = snowball_image.convert_alpha()
        snowball_image = pg.transform.scale(snowball_image, (round(screen_size[0]*(40/1366)), round(screen_size[1]*(40/768))))
        snowball_image.fill((0, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(snowball_image, ((screen_size[0]/1366)*ball.x_pos * (1000/1366), (screen_size[1]/768) * ball.y_pos * (400/768)))
    
    menu_font = pg.font.SysFont('Arial', round(35*(screen_size[1]/768)))
    menu_text = menu_font.render("SCORE: "+ str(game_score[0]) + "-" + str(game_score[1]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//2, 0.75*screen_size[1]//14)
    game_display.blit(menu_text, text_rect)
    menu_text = menu_font.render("TIME: "+ str(game_time), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//2, 1.5*screen_size[1]//14)
    game_display.blit(menu_text, text_rect)
    
    draw_ui(screen_size, game_display, p1_blob, p2_blob)    

    draw_timer(screen_size, game_display, timer)