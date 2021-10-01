from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import draw_ball_overlay, draw_ball_particles as draw_ball_particles, draw_blob_particles
from resources.graphics_engine.display_particles import clear_particle_memory as clear_particle_memory
from resources.graphics_engine.display_particles import draw_recharge_flash, draw_ui_particles, draw_damage_flash
from math import ceil
import pygame as pg
cwd = getcwd()

image_cache = {"initialized": False}

def unload_image_cache():
    global image_cache
    image_cache = {"initialized": False}

def draw_blob(screen_size, game_display, blob):
    global image_cache

def draw_ball(screen_size, game_display, ball):
    global image_cache
    if not (ball.image == image_cache['ball_clone']):
        image_cache['ball'] = pg.transform.scale(pg.image.load(ball.image), (40, 40))
        image_cache['ball_clone'] = ball.image
    game_display.blit(image_cache['ball'], ((screen_size[0]/1366)*ball.x_pos * (1000/1366), (screen_size[1]/768) * ball.y_pos * (400/768)))

cooldown_species = ['instant', 'delayed']

def draw_ui_icons(game_display, ui_font, blob, x_offset):
    if(blob.player == 1):
        ability_icon = image_cache['p1_ability_icon']
    else:
        ability_icon = image_cache['p2_ability_icon']
    pg.draw.rect(game_display, (200, 200, 200), (x_offset, 0, 70, 70))
    game_display.blit(image_cache["heart_icon"], (x_offset, 0))
    menu_text = ui_font.render(str(blob.hp), False, (0, 255, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (x_offset+35, 30)
    game_display.blit(menu_text, text_rect)
    pg.draw.rect(game_display, (200, 200, 200), (x_offset + 80, 0, 70, 70))
    game_display.blit(ability_icon, (x_offset + 80, 0))
    pg.draw.rect(game_display, (200, 200, 200), (x_offset + 160, 0, 70, 70))
    game_display.blit(image_cache["kick_icon"], (x_offset + 160, 0))
    pg.draw.rect(game_display, (200, 200, 200), (x_offset + 240, 0, 70, 70))
    game_display.blit(image_cache["block_icon"], (x_offset + 240, 0))
    pg.draw.rect(game_display, (200, 200, 200), (x_offset + 320, 0, 70, 70))
    game_display.blit(image_cache["boost_icon"], (x_offset + 320, 0))

def draw_cooldown(game_display, blob, ui_font, box_x, blob_function, boost_active = False, ability_active = False):
    #Draws the cooldown squares for abilities, kicks, blocks and boosts.
    #Blob function is a tuple with percentage first, and visualization second
    #Valid blob_functions:
    #get_ability_visuals
    #get_kick_visuals
    #get_block_visuals
    #get_boost_timer_visuals
    #get_boost_cooldown_visuals
    cooldown_percentage, cooldown_visualization = blob_function
    if(boost_active):
        square_color = (0, 0, 255)
        text_color = (0, 255, 124)
    else:
        square_color = (50, 50, 50)
        text_color = (0, 255, 255)
    cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
    cooldown_surface.set_alpha(124)
    pg.draw.rect(cooldown_surface, square_color, (0, 70-cooldown_percentage*70, 70, 140))
    game_display.blit(cooldown_surface, (box_x, 0))
    menu_text = ui_font.render(str(cooldown_visualization), False, text_color)
    text_rect = menu_text.get_rect()
    text_rect.center = (box_x + 36, 30)
    game_display.blit(menu_text, text_rect)

def draw_judgement(game_display, blob, other_blob, ui_font, box_x):
    game_display.blit(image_cache['judgement'], (box_x, 0))
    # TODO: Blot out the underlying ability, add text and cooldown rectangle
    cooldown_percentage = blob.status_effects['judged']/other_blob.special_ability_duration
    cooldown_visualization = str(ceil(blob.status_effects['judged']/6)/10)
    judgement_tuple = (cooldown_percentage, cooldown_visualization)
    draw_cooldown(game_display, blob, ui_font, box_x, judgement_tuple)

def find_nrg_color(blob):
    nrg_color = (0, 0, 0)
    if(blob.player == 1):
        if(blob.special_ability_meter >= blob.special_ability_cost):
            nrg_color = (255, 0, 0)
        else:
            nrg_color = (50, 0, 0)
    else:
        if(blob.special_ability_meter >= blob.special_ability_cost):
            nrg_color = (0, 0, 255)
        else:
            nrg_color = (0, 0, 50)
    return nrg_color

def draw_nrg_bar(game_display, blob, x_offset):
    nrg_surface = pg.Surface((390, 35), pg.SRCALPHA)
    nrg_bar = nrg_surface.get_width() * blob.special_ability_meter / blob.special_ability_max
    nrg_color = find_nrg_color(blob)
    if(blob.special_ability_meter >= blob.boost_cost and not blob.boost_cooldown_timer > 0):
        border_color = (255, 255, 0)
    else:
        border_color = (0, 0, 0)
    pg.draw.rect(nrg_surface, (124, 124, 124), (0, 0, nrg_surface.get_width(), nrg_surface.get_height()))
    if(blob.player == 1):
        pg.draw.rect(nrg_surface, nrg_color, (0, 0, nrg_bar, nrg_surface.get_height()))
    else:
        pg.draw.rect(nrg_surface, nrg_color, (nrg_surface.get_width() - (nrg_bar), 0, nrg_bar, nrg_surface.get_height()))
    
    pg.draw.rect(nrg_surface, border_color, (0, 0, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, nrg_surface.get_height()-3, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, 0, 3, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (nrg_surface.get_width() - 3, 0, 3, nrg_surface.get_height()))
    game_display.blit(nrg_surface, (x_offset, 75))

def draw_ui(screen_size, game_display, p1_blob, p2_blob):
    global image_cache
    ui_font = image_cache['ui_font']
    
    draw_ui_icons(game_display, ui_font, p1_blob, 10)
    draw_ui_icons(game_display, ui_font, p2_blob, 966)

    draw_nrg_bar(game_display, p1_blob, 10)
    draw_nrg_bar(game_display, p2_blob, 966)

    #DEBUG TEXT
    menu_text = ui_font.render(("NRG: " + str(p1_blob.special_ability_meter)), False, (255, 255, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//5, screen_size[1]//9)
    game_display.blit(menu_text, text_rect)
    
    #DEBUG TEXT
    menu_text = ui_font.render(("NRG: " + str(p2_blob.special_ability_meter)), False, (255, 255, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (4*screen_size[0]//5, screen_size[1]//9)
    game_display.blit(menu_text, text_rect)

    if(p1_blob.recharge_indicators['damage']):
        draw_damage_flash(10)

    if(p1_blob.status_effects['judged']):
        draw_judgement(game_display, p1_blob, p2_blob, ui_font, 90)
        draw_judgement(game_display, p1_blob, p2_blob, ui_font, 170)
        draw_judgement(game_display, p1_blob, p2_blob, ui_font, 250)
        draw_judgement(game_display, p1_blob, p2_blob, ui_font, 330)
    else:
        if(p1_blob.ability_classification in cooldown_species):
            if(p1_blob.special_ability_cooldown):
                draw_cooldown(game_display, p1_blob, ui_font, 90, p1_blob.get_ability_visuals())
            elif(p1_blob.recharge_indicators['ability']):
                draw_recharge_flash(90)
        if(p1_blob.kick_cooldown_visualization > 0):
            draw_cooldown(game_display, p1_blob, ui_font, 170, p1_blob.get_kick_visuals())
            
        if(p1_blob.recharge_indicators['kick']):
                draw_recharge_flash(170)

        if(p1_blob.block_cooldown_visualization > 0):
            draw_cooldown(game_display, p1_blob, ui_font, 250, p1_blob.get_block_visuals())
        
        if(p1_blob.recharge_indicators['block']):
                draw_recharge_flash(250)

        if(p1_blob.boost_timer_visualization > 0):
            draw_cooldown(game_display, p1_blob, ui_font, 330, p1_blob.get_boost_timer_visuals(), boost_active = True)
        elif(p1_blob.boost_cooldown_visualization > 0):
            draw_cooldown(game_display, p1_blob, ui_font, 330, p1_blob.get_boost_cooldown_visuals())
        
        if(p1_blob.recharge_indicators['boost']):
            draw_recharge_flash(330)

    if(p2_blob.recharge_indicators['damage']):
        draw_damage_flash(966)

    if(p2_blob.status_effects['judged']):
        draw_judgement(game_display, p2_blob, p1_blob, ui_font, 1046)
        draw_judgement(game_display, p2_blob, p1_blob, ui_font, 1126)
        draw_judgement(game_display, p2_blob, p1_blob, ui_font, 1206)
        draw_judgement(game_display, p2_blob, p1_blob, ui_font, 1286)
    else:
        if(p2_blob.ability_classification in cooldown_species):
            if(p2_blob.special_ability_cooldown):
                draw_cooldown(game_display, p2_blob, ui_font, 1046, p2_blob.get_ability_visuals())
            elif(p2_blob.recharge_indicators['ability']):
                draw_recharge_flash(1046)
        
        if(p2_blob.kick_cooldown_visualization > 0):
            draw_cooldown(game_display, p2_blob, ui_font, 1126, p2_blob.get_kick_visuals())

        if(p2_blob.recharge_indicators['kick']):
            draw_recharge_flash(1126)

        if(p2_blob.block_cooldown_visualization > 0):
            draw_cooldown(game_display, p2_blob, ui_font, 1206, p2_blob.get_block_visuals())

        if(p2_blob.recharge_indicators['block']):
            draw_recharge_flash(1206)

        if(p2_blob.boost_timer_visualization > 0):
            draw_cooldown(game_display, p2_blob, ui_font, 1286, p2_blob.get_boost_timer_visuals(), boost_active = True)
        elif(p2_blob.boost_cooldown_visualization > 0):
            draw_cooldown(game_display, p2_blob, ui_font, 1286, p2_blob.get_boost_cooldown_visuals())

        if(p2_blob.recharge_indicators['boost']):
            draw_recharge_flash(1286)
        
    draw_ui_particles(game_display)

def draw_timer(screen_size, game_display, timer):
    global image_cache
    if(timer > 0):
            timer_font = image_cache['menu_font']
            timer_text = timer_font.render(str(ceil(timer/6)/10), False, (220, 100, 2))
            text_rect = timer_text.get_rect()
            text_rect.center = (screen_size[0]//2, 2*screen_size[1]//7)
            game_display.blit(timer_text, text_rect)

def draw_blob_special(blob, game_display):
    
    if(blob.boost_timer):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 255, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))

    if(blob.focusing):
        blob_special = image_cache['blob_special'].convert_alpha()
        if(blob.focus_lock):
            blob_special.fill((255, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        else:
            blob_special.fill((200, 200, 200, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))
    if(blob.block_timer):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((0, 0, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        game_display.blit(blob_special, ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))
        p1_block_surface = pg.Surface((110, 220), pg.SRCALPHA)
        p1_block_surface.set_alpha(124)
        if(blob.block_timer < blob.block_timer_max - 3):
            p1_block_surface.set_alpha(124 - 10 * (blob.block_timer_max - blob.block_timer))
        pg.draw.rect(p1_block_surface, (0, 0, 255), (0, 0, 110, 220), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
        #TODO: Scaling based off of block size
        if(blob.facing == 'left'):
            #Grab Box Visualization
            game_display.blit(p1_block_surface, ((blob.x_pos - 150)*(1000/1366), (blob.y_pos - 105)*(382/768)))
        else:
            game_display.blit(p1_block_surface, ((blob.x_pos + 186)*(1000/1366), (blob.y_pos - 105)*(382/768)))
    if(blob.kick_visualization):
        blob_special = image_cache['blob_special'].convert_alpha()
        blob_special.fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        blob_special.set_alpha(255 - 16 * (blob.kick_visualization_max - blob.kick_visualization))
        game_display.blit(blob_special, ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))

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
        image_cache['p1_ability_icon'] = pg.transform.scale(pg.image.load(p1_blob.ability_icon).convert_alpha(), (70, 70))
        image_cache['p2_blob'] = pg.transform.scale(pg.image.load(p2_blob.image).convert_alpha(), (120, 66))
        image_cache['p2_blob_clone'] = p2_blob.image
        image_cache['p2_ability_icon'] = pg.transform.scale(pg.image.load(p2_blob.ability_icon).convert_alpha(), (70, 70))
        image_cache['p2_darkened'] = False
        image_cache['blob_special'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/blobs/special_blob.png"), (180, 99)).convert_alpha()
        image_cache['kick_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/kick_icon.png"), (70, 70))
        image_cache['block_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/block_icon.png"), (70, 70))
        image_cache['boost_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/boost_icon.png"), (70, 70))
        image_cache['heart_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/heart_icon.png"), (70, 70))
        image_cache['judgement'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ability_icons/cnd.png"), (70, 70))
        image_cache['menu_font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
        image_cache['ui_font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
        

    if not (p1_blob.image == image_cache['p1_blob_clone']):
        image_cache['p1_blob'] = pg.transform.scale(pg.image.load(p1_blob.image).convert_alpha(), (round(screen_size[0]*(120/1366)), round(screen_size[1]*(66/768))))
        image_cache['p1_blob_clone'] = p1_blob.image

    if(p1_blob.facing == "right"):
        game_display.blit(pg.transform.flip(image_cache['p1_blob'], True, False), ((screen_size[0]/1366)*p1_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(400/768))))
    else:
        game_display.blit(image_cache['p1_blob'], ((screen_size[0]/1366)*p1_blob.x_pos*(1000/1366), (screen_size[1]/768)*(p1_blob.y_pos*(400/768))))

    draw_blob_special(p1_blob, game_display)
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

    draw_blob_special(p2_blob, game_display)
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
    # TODO: Move to own file?
    draw_background(game_display, "win_screen", settings)
    clear_particle_memory()
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 50)
    if(game_stats == 3):
        menu_text = menu_font.render("TIE", False, (0, 0, 255))
    else:
        menu_text = menu_font.render("WINNER: "+ str(game_stats[0]), False, (0, 0, 255))

    text_rect = menu_text.get_rect()
    text_rect.center = (683, 60)
    game_display.blit(menu_text, text_rect)

    menu_text = menu_font.render("TIME TAKEN: "+ str(game_stats[5]), False, (0, 0, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (683, 110)
    game_display.blit(menu_text, text_rect)

    menu_text = menu_font.render(f"SCORE: {game_stats[4][0]}-{game_stats[4][1]}", False, (0, 0, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (683, 170)
    game_display.blit(menu_text, text_rect)
    # TODO: P1 Box
    # TODO: P2 Box
    # TODO: General Stats Box