from imp import cache_from_source
from os import getcwd
from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import draw_ball_overlay, draw_ball_particles as draw_ball_particles, draw_blob_particles, draw_shatter
from resources.graphics_engine.display_particles import clear_particle_memory as clear_particle_memory
from resources.graphics_engine.display_particles import draw_recharge_flash, draw_ui_particles, draw_damage_flash, draw_heal_flash, draw_energy_flash, draw_block_flash, draw_boost_flash
from resources.graphics_engine.display_environmental_modifiers import draw_environmental_modifiers
from math import ceil

from engine.blob_stats import species_to_stars, ability_image_dict

import pygame as pg
cwd = getcwd()

image_cache = {"initialized": False, "ui_initialized": False}

def return_image_cache():
    return image_cache

def unload_image_cache():
    global image_cache
    image_cache = {"initialized": False, "ui_initialized": False}
    image_cache['p1_ability_icon'] = None
    image_cache['p2_ability_icon'] = None
    image_cache['joker_card'] = None
    image_cache['icons'] = {}
    image_cache['monado'] = {
        "SPEED": pg.transform.scale(pg.image.load(cwd+"/resources/images/ui_icons/boost_icon.png"), (70, 70)),
        "SMASH": pg.transform.scale(pg.image.load(cwd+"/resources/images/ability_icons/pill_boost.png"), (70, 70)),
        "SHIELD": pg.transform.scale(pg.image.load(cwd+"/resources/images/particles/shield_particle.png"), (70, 70)),
        "CHILL": pg.transform.scale(pg.image.load(cwd+"/resources/images/ability_icons/snowball_v2.png"), (70, 70)),
    }
    for icon in ability_image_dict:
        try:
            ability_key = species_to_stars(icon, {})['special_ability']
            image_cache['icons'][ability_key] = pg.transform.scale(pg.image.load(ability_image_dict[icon]), (70, 70))
        except:
            image_cache['icons'][icon] = pg.transform.scale(pg.image.load(cwd+"/resources/images/ability_icons/404.png"), (70, 70))

unload_image_cache()

def draw_blob(game_display, blob):
    # TODO: Make this do something
    global image_cache

def draw_ball(game_display, ball):
    global image_cache
    bname = "ball_" + str(ball.id)
    if not (ball.image == image_cache[bname + '_clone']):
        image_cache[bname] = pg.transform.scale(pg.image.load(ball.image), (40, 40))
        image_cache[bname + '_clone'] = ball.image
    y_pos = ball.y_pos
    if(ball.y_pos < 210): # Why is this here?
        y_pos = 210 # TODO: Get to the bottom of this.
    game_display.blit(image_cache[bname], (ball.x_pos * (1000/1366),  y_pos * (400/768)))

cooldown_species = ['instant', 'delayed']

def create_ui_icons(ui_font, blob):
    '''
    Creates the UI icons and blits them onto a surface
    The surface generally doesn't change frame to frame
    Returns the surface created with the parameters
    '''
    game_display = pg.Surface((390, 70), pg.SRCALPHA)
    if(blob.player == 1):
        ability_icon = image_cache['p1_ability_icon']
    else:
        ability_icon = image_cache['p2_ability_icon']
    if(blob.status_effects['cards']['ability']):
        ability_icon = image_cache['icons'][blob.status_effects['cards']['ability']]
    pg.draw.rect(game_display, (200, 200, 200), (0, 0, 70, 70))
    game_display.blit(image_cache["heart_icon"], (0, 0))
    
    
    pg.draw.rect(game_display, (200, 200, 200), (80, 0, 70, 70))
    game_display.blit(ability_icon, (80, 0))

    if(not blob.status_effects['cards']['kick']):
        kick_icon = image_cache["kick_icon"]
    else:
        kick_icon = image_cache['icons'][blob.status_effects['cards']['kick']]
    pg.draw.rect(game_display, (200, 200, 200), (160, 0, 70, 70))
    game_display.blit(kick_icon, (160, 0))
    
    if(not blob.status_effects['cards']['block']):
        block_icon = image_cache["block_icon"]
    else:
        block_icon = image_cache['icons'][blob.status_effects['cards']['block']]
    pg.draw.rect(game_display, (200, 200, 200), (240, 0, 70, 70))
    game_display.blit(block_icon, (240, 0))

    if(not blob.status_effects['cards']['boost']):
        boost_icon = image_cache["boost_icon"]
    else:
        boost_icon = image_cache['icons'][blob.status_effects['cards']['boost']]
    pg.draw.rect(game_display, (200, 200, 200), (320, 0, 70, 70))
    game_display.blit(boost_icon, (320, 0))

    return game_display

def draw_cooldown(game_display, blob, ui_font, align, blob_function, boost_active = False, ability_active = False):
    #Draws the cooldown squares for abilities, kicks, blocks and boosts.
    #Blob function is a tuple with percentage first, and visualization second
    #Valid blob_functions:
    #get_ability_visuals
    #get_kick_visuals
    #get_block_visuals
    #get_boost_timer_visuals
    #get_boost_cooldown_visuals
    box_x, box_y = align[0], align[1]
    cooldown_percentage, cooldown_visualization = blob_function
    if(boost_active):
        square_color = (0, 0, 255)
        text_color = (0, 255, 124)
    else:
        square_color = (50, 50, 50)
        text_color = (0, 255, 255)
    cooldown_surface = pg.Surface((70, 70), pg.SRCALPHA)
    cooldown_surface.set_alpha(124)
    if(cooldown_percentage > 1):
        cooldown_percentage = 1
    pg.draw.rect(cooldown_surface, square_color, (0, 70-cooldown_percentage*70, 70, 70))
    game_display.blit(cooldown_surface, (box_x, box_y))
    menu_text = ui_font.render(str(cooldown_visualization), False, text_color)
    text_rect = menu_text.get_rect()
    text_rect.center = (box_x + 36, 30)
    game_display.blit(menu_text, text_rect)

def draw_judgement(game_display, blob, ui_font, box_x):
    game_display.blit(image_cache['judgement'], box_x)
    # TODO: Blot out the underlying ability, add text and cooldown rectangle
    cooldown_percentage = blob.status_effects['judged']/60
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

def draw_nrg_bar(game_display, blob, align):
    x_offset = align[0]
    y_offset = align[1] + 75
    nrg_surface = pg.Surface((390, 35), pg.SRCALPHA)
    nrg_bar = nrg_surface.get_width() * blob.special_ability_meter / blob.special_ability_max
    nrg_color = find_nrg_color(blob)
    if(blob.special_ability_meter >= blob.boost_cost and not blob.boost_cooldown_timer > 0):
        border_color = (255, 255, 0)
    else:
        border_color = (0, 0, 0)
    pg.draw.rect(nrg_surface, (124, 124, 124), (0, 0, nrg_surface.get_width(), nrg_surface.get_height()))
    # TODO: Rectangle growth depending on the x alignment
    if(blob.player == 1):
        pg.draw.rect(nrg_surface, nrg_color, (0, 0, nrg_bar, nrg_surface.get_height()))
    else:
        pg.draw.rect(nrg_surface, nrg_color, (nrg_surface.get_width() - (nrg_bar), 0, nrg_bar, nrg_surface.get_height()))
    
    pg.draw.rect(nrg_surface, border_color, (0, 0, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, nrg_surface.get_height()-3, nrg_surface.get_width(), 3))
    pg.draw.rect(nrg_surface, border_color, (0, 0, 3, nrg_surface.get_height()))
    pg.draw.rect(nrg_surface, border_color, (nrg_surface.get_width() - 3, 0, 3, nrg_surface.get_height()))
    game_display.blit(nrg_surface, (x_offset, y_offset))

def draw_ui(game_display, blobs):
    '''
    Draws all elements of the UI, including the icons, cooldowns, and Energy Bar
    '''
    global image_cache
    ui_font = image_cache['ui_font']
    
    if not (image_cache['ui_initialized']):
        for blob in blobs:
            cache_key = "p" + str(blob.player) + "_ui_icons"
            image_cache[cache_key] = create_ui_icons(ui_font, blob)

        image_cache['ui_initialized'] = True

    ui_draw = [(10, 0), (966, 0), (10, 70), (966, 70)]
    ui_idx = 0
    for blob in blobs:
        pname = str(blob.player)
        align = ui_draw[ui_idx]
        game_display.blit(image_cache['p'+pname+'_ui_icons'], align)
        

        menu_text = ui_font.render(str(blob.hp), False, (0, 255, 0))
        text_rect = menu_text.get_rect()
        text_rect.center = (align[0] + 35, align[1] + 30)
        game_display.blit(menu_text, text_rect)

        draw_nrg_bar(game_display, blob, align)

        ui_idx += 1

        #DEBUG TEXT
        menu_text = ui_font.render(("NRG: " + str(blob.special_ability_meter)), False, (255, 255, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (align[0] + 263, align[1] + 85)
        game_display.blit(menu_text, text_rect)

        # For each blob:
        # Check for damage flash
        # Check for reflect break
        # Check for heal
        # Check for Judged
        # If not judged draw cooldowns
        # Then draw energy flash

        ab_align = (align[0] + 80, align[1])
        k_align = (align[0] + 160, align[1])
        bl_align = (align[0] + 240, align[1])
        boo_align = (align[0] + 320, align[1])
        if(blob.recharge_indicators['damage']):
            draw_damage_flash(align)
        
        if(blob.status_effects['reflect_break']):
            draw_shatter(ab_align, blob.status_effects['reflect_break'])

        if(blob.recharge_indicators['heal']):
            draw_heal_flash(align)

        if(blob.status_effects['judged']):
            draw_judgement(game_display, blob, ui_font, ab_align)
            draw_judgement(game_display, blob, ui_font, k_align)
            draw_judgement(game_display, blob, ui_font, bl_align)
            draw_judgement(game_display, blob, ui_font, boo_align)
        else:
            if(blob.status_effects['silenced']):
                draw_cooldown(game_display, blob, ui_font, ab_align, (blob.status_effects['silenced']/360, ceil(blob.status_effects['silenced']/6)/10))
            elif(blob.ability_classification in cooldown_species):
                if(blob.special_ability_cooldown):
                    draw_cooldown(game_display, blob, ui_font, ab_align, blob.get_ability_visuals())
                elif(blob.recharge_indicators['ability']):
                    draw_recharge_flash(ab_align)
            
            if(blob.kick_cooldown_visualization > 0):
                draw_cooldown(game_display, blob, ui_font, k_align, blob.get_kick_visuals())
                
            if(blob.recharge_indicators['kick']):
                    draw_damage_flash(k_align)

            if(blob.block_cooldown_visualization > 0):
                draw_cooldown(game_display, blob, ui_font, bl_align, blob.get_block_visuals())
            
            if(blob.recharge_indicators['block']):
                    draw_block_flash(bl_align)

            if(blob.boost_timer_visualization > 0):
                draw_cooldown(game_display, blob, ui_font, boo_align, blob.get_boost_timer_visuals(), boost_active = True)
            elif(blob.boost_cooldown_visualization > 0):
                draw_cooldown(game_display, blob, ui_font, boo_align, blob.get_boost_cooldown_visuals())
            
            if(blob.recharge_indicators['boost']):
                draw_boost_flash(boo_align)

        if(blob.recharge_indicators['ability_energy']):
            draw_energy_flash(align)

    draw_ui_particles(game_display)

def draw_timer(game_display, timer):
    global image_cache
    if(timer > 0):
        timer_font = image_cache['menu_font']
        timer_text = timer_font.render(str(ceil(timer/6)/10), False, (220, 100, 2))
        text_rect = timer_text.get_rect()
        text_rect.center = (683, 218)
        game_display.blit(timer_text, text_rect)

def draw_blob_special(blob, game_display): # Blob special appears when kicking, blocking, boosting or focusing
    '''
    Gets the blob and draws glowy shells around the blob
    Each shell represents a different state
    Red means the blob is kicking
    Blue means the blob is blocking
    Yellow means the blob is boosting
    White means the blob is focusing, and can only jump
    Grey means the blob is focusing, but can let go of the button to move
    '''
    if(blob.boost_timer):
        game_display.blit(image_cache['blob_special_boost'], ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))

    if(blob.focusing):
        if(blob.focus_lock):
            game_display.blit(image_cache['blob_special_focus_lock'], ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))
        else:
            game_display.blit(image_cache['blob_special_focus_free'], ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))

    if(blob.block_timer):
        game_display.blit(image_cache['blob_special_block'], ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))
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
        blob_special = image_cache['blob_special_kick'].convert_alpha()
        blob_special.set_alpha(255 - 16 * (blob.kick_visualization_max - blob.kick_visualization))
        game_display.blit(blob_special, ((blob.x_pos - 42)*(1000/1366), (blob.y_pos*(382/768))))

def draw_menu(game_display, blob):
    #print("1", blob.status_effects['cards']['pulled'][0])
    if(blob.status_effects['menu']['type'] == 'cardpack'):
        if(blob.status_effects['menu']['direction'] == 'left'):
            game_display.blit(image_cache['joker_card'], ((blob.x_pos - 105) * (1000/1366), ((blob.y_pos - 25)*(382/768))))
            game_display.blit(image_cache['icons'][blob.status_effects['cards']['pulled'][0]], ((blob.x_pos - 100) * (1000/1366), ((blob.y_pos - 20) *(382/768))))
        else:
            game_display.blit(image_cache['joker_card'], ((blob.x_pos - 105) * (1000/1366), ((blob.y_pos - 5)*(382/768))))
            game_display.blit(image_cache['icons'][blob.status_effects['cards']['pulled'][0]], ((blob.x_pos - 100) * (1000/1366), (blob.y_pos*(382/768))))
        #print("3", blob.status_effects['cards']['pulled'][2])
        if(blob.status_effects['menu']['direction'] == 'up'):
            game_display.blit(image_cache['joker_card'], ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos - 225) *(382/768))))
            game_display.blit(image_cache['icons'][blob.status_effects['cards']['pulled'][1]], ((blob.x_pos + 25) * (1000/1366), ((blob.y_pos - 220) *(382/768))))
        else:
            game_display.blit(image_cache['joker_card'], ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos - 205) *(382/768))))
            game_display.blit(image_cache['icons'][blob.status_effects['cards']['pulled'][1]], ((blob.x_pos + 25) * (1000/1366), ((blob.y_pos - 200) *(382/768))))
        #print("2", blob.status_effects['cards']['pulled'][1])
        if(blob.status_effects['menu']['direction'] == 'right'):
            game_display.blit(image_cache['joker_card'], ((blob.x_pos + 160) * (1000/1366), ((blob.y_pos - 25)*(382/768))))
            game_display.blit(image_cache['icons'][blob.status_effects['cards']['pulled'][2]], ((blob.x_pos + 165) * (1000/1366), ((blob.y_pos-20)*(382/768))))
        else:
            game_display.blit(image_cache['joker_card'], ((blob.x_pos + 160) * (1000/1366), ((blob.y_pos - 5)*(382/768))))
            game_display.blit(image_cache['icons'][blob.status_effects['cards']['pulled'][2]], ((blob.x_pos + 165) * (1000/1366), (blob.y_pos*(382/768))))
    elif(blob.status_effects['menu']['type'] == 'monado'):
        if(blob.status_effects['menu']['direction'] == 'left' and blob.status_effects['monado_smash_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos - 105) * (1000/1366), ((blob.y_pos - 25)*(382/768))))
            game_display.blit(image_cache['monado']["SMASH"], ((blob.x_pos - 100) * (1000/1366), ((blob.y_pos - 10) *(382/768))))
        elif(blob.status_effects['monado_smash_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos - 105) * (1000/1366), ((blob.y_pos - 5)*(382/768))))
            game_display.blit(image_cache['monado']["SMASH"], ((blob.x_pos - 100) * (1000/1366), ((blob.y_pos+10)*(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((blob.x_pos - 105) * (1000/1366), ((blob.y_pos + 55)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((blob.x_pos - 105) * (1000/1366), ((blob.y_pos + 55)*(382/768)), 80*(blob.status_effects['monado_smash_cooldown']/900), 20))
        #print("3", blob.status_effects['cards']['pulled'][2])
        if(blob.status_effects['menu']['direction'] == 'up' and blob.status_effects['monado_shield_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos - 225) *(382/768))))
            game_display.blit(image_cache['monado']["SHIELD"], ((blob.x_pos + 25) * (1000/1366), ((blob.y_pos - 180) *(382/768))))
        elif(blob.status_effects['monado_shield_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos - 205) *(382/768))))
            game_display.blit(image_cache['monado']["SHIELD"], ((blob.x_pos + 25) * (1000/1366), ((blob.y_pos - 160) *(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos - 95)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos - 95)*(382/768)), 80*(blob.status_effects['monado_shield_cooldown']/900), 20))
        #print("2", blob.status_effects['cards']['pulled'][1])
        if(blob.status_effects['menu']['direction'] == 'right' and blob.status_effects['monado_speed_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos + 160) * (1000/1366), ((blob.y_pos - 25)*(382/768))))
            game_display.blit(image_cache['monado']["SPEED"], ((blob.x_pos + 165) * (1000/1366), ((blob.y_pos-20)*(382/768))))
        elif(blob.status_effects['monado_speed_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos + 160) * (1000/1366), ((blob.y_pos - 5)*(382/768))))
            game_display.blit(image_cache['monado']["SPEED"], ((blob.x_pos + 165) * (1000/1366), (blob.y_pos*(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((blob.x_pos + 160) * (1000/1366), ((blob.y_pos + 55)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((blob.x_pos + 160) * (1000/1366), ((blob.y_pos + 55)*(382/768)), 80*(blob.status_effects['monado_speed_cooldown']/900), 20))
        if(blob.status_effects['menu']['direction'] == 'down' and blob.status_effects['monado_chill_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos + 185) *(382/768))))
            game_display.blit(image_cache['monado']["CHILL"], ((blob.x_pos + 25) * (1000/1366), ((blob.y_pos+175)*(382/768))))
        elif(blob.status_effects['monado_chill_cooldown'] <= 0):
            #game_display.blit(image_cache['joker_card'], ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos + 205) *(382/768))))
            game_display.blit(image_cache['monado']["CHILL"], ((blob.x_pos + 25) * (1000/1366), ((blob.y_pos+195)*(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos + 240)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((blob.x_pos + 20) * (1000/1366), ((blob.y_pos + 240)*(382/768)), 80*(blob.status_effects['monado_chill_cooldown']/900), 20))
def draw_gameplay(game_display, info_getter, settings): 
    gameplay_surface = pg.Surface((1366, 768))
    blobs = info_getter[0]
    balls = info_getter[1]
    game_score = info_getter[2]
    timer = info_getter[3]
    game_time = info_getter[4]

    # TODO: Simplify and remove things from this function
    # TODO: Make drawing things like blob #'s agnostic to the amount passed
    draw_background(gameplay_surface, "casual_match", settings)
    global cwd
    global image_cache
    # TODO: Cause different things to be loaded with different amounts of blobs
    # TODO: Loop over balls
    if not image_cache['initialized']: #Load in the images so we don't keep importing them
        image_cache['initialized'] = True
        for ball in balls.values():
            bname = "ball_" + str(ball.id)
            image_cache[bname] = pg.transform.scale(pg.image.load(ball.image), (40, 40))
            image_cache[bname + '_clone'] = ball.image
        used_pnames = []
        used_bfx = {'darkened': False, 'brightened': False, 'blackened': False}
        for blob in blobs.values():
            pname = "p" + str(blob.player) + "_"
            used_pnames.append(blob.player)

            blob_height = round(pg.image.load(blob.image).get_height() * 0.6)

            image_cache[pname+'blob_left'] = pg.transform.scale(pg.image.load(blob.image).convert_alpha(), (120, blob_height))
            image_cache[pname+'blob_right'] = pg.transform.flip(image_cache[pname+'blob_left'], True, False)
            image_cache[pname+'dead_left'] = pg.transform.scale(pg.image.load(blob.image_death).convert_alpha(), (120, blob_height))
            image_cache[pname+'dead_right'] = pg.transform.flip(image_cache[pname+'dead_left'], True, False)
            image_cache[pname+'blob_clone'] = blob.image
            try:
                image_cache[pname+'ability_icon'] = pg.transform.scale(pg.image.load(blob.ability_icon).convert_alpha(), (70, 70))
            except:
                image_cache[pname+'ability_icon'] = pg.transform.scale(pg.image.load(cwd+"/resources/images/ability_icons/404.png").convert_alpha(), (70, 70))


            # TODO: Duplicate check to darken the blobs
            for used_blob in used_pnames:
                if(blob.species == blobs[used_blob].species and blob.costume == blobs[used_blob].costume and blob.player != blobs[used_blob].player):
                    if not used_bfx['darkened']:
                        image_cache[pname+'blob_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                        image_cache[pname+'blob_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    elif not used_bfx['brightened']:
                        image_cache[pname+'blob_right'].fill((225, 225, 225, 255), special_flags=pg.BLEND_RGBA_MULT)
                        image_cache[pname+'blob_left'].fill((225, 225, 225, 255), special_flags=pg.BLEND_RGBA_MULT)
                    elif not used_bfx['blackened']:
                        image_cache[pname+'blob_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                        image_cache[pname+'blob_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)

            image_cache[pname+'damage_left'] = image_cache[pname+'blob_left'].copy()
            image_cache[pname+'damage_left'].set_alpha(100)
            image_cache[pname+'damage_right'] = image_cache[pname+'blob_right'].copy()
            image_cache[pname+'damage_right'].set_alpha(100)
        
        image_cache['blob_special'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/blobs/special_blob.png"), (180, 99)).convert_alpha()
        image_cache['blob_special_boost'] = image_cache['blob_special'].convert_alpha()
        image_cache['blob_special_boost'].fill((255, 255, 0, 124), special_flags=pg.BLEND_RGBA_MULT)
        image_cache['blob_special_focus_lock'] = image_cache['blob_special'].convert_alpha()
        image_cache['blob_special_focus_lock'].fill((255, 255, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        image_cache['blob_special_focus_free'] = image_cache['blob_special'].convert_alpha()
        image_cache['blob_special_focus_free'].fill((200, 200, 200, 124), special_flags=pg.BLEND_RGBA_MULT)
        image_cache['blob_special_block'] = image_cache['blob_special'].convert_alpha()
        image_cache['blob_special_block'].fill((0, 0, 255, 124), special_flags=pg.BLEND_RGBA_MULT)
        image_cache['blob_special_kick'] = image_cache['blob_special'].convert_alpha()
        image_cache['blob_special_kick'].fill((255, 0, 0, 124), special_flags=pg.BLEND_RGBA_MULT)

        image_cache['joker_card'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/visible_card.png"), (80, 80))
        image_cache['kick_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/kick_icon.png"), (70, 70))
        image_cache['block_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/block_icon.png"), (70, 70))
        image_cache['boost_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/boost_icon.png"), (70, 70))
        image_cache['heart_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ui_icons/heart_icon.png"), (70, 70))
        image_cache['judgement'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/ability_icons/cnd.png"), (70, 70))
        # TODO: Why are we loading in the same font twice?
        image_cache['menu_font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
        image_cache['ui_font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)

    for blob in blobs.values():
        pname = "p" + str(blob.player) + "_"
        if blob.recharge_indicators['ability_swap_b']:
            try:
                image_cache[pname + 'ability_icon'] = pg.transform.scale(pg.image.load(blob.ability_icon).convert_alpha(), (70, 70))
            except:
                image_cache[pname + 'ability_icon'] = pg.transform.scale(pg.image.load("/resources/images/ui_icons/404.png").convert_alpha(), (70, 70))
            image_cache['ui_initialized'] = False

        if not (blob.image == image_cache[pname+'blob_clone']):
            blob_height = round(pg.image.load(blob.image).get_height()*0.6)
            image_cache[pname+'blob'] = pg.transform.scale(pg.image.load(blob.image).convert_alpha(), (120, blob_height))
            image_cache[pname+'blob_clone'] = blob.image
        if not("invisible" in blob.image):
            blob_y_pos = blob.y_pos - (image_cache[pname+'blob_right'].get_height() - 66)
            if(blob.facing == "right"):
                if(blob.hp > 0):
                    gameplay_surface.blit(image_cache[pname+'blob_right'], (blob.x_pos*(1000/1366), (blob_y_pos*(400/768))))
                else:
                    gameplay_surface.blit(image_cache[pname+'dead_right'], (blob.x_pos*(1000/1366), (blob_y_pos*(400/768))))
            else:
                if(blob.hp > 0):
                    gameplay_surface.blit(image_cache[pname+'blob_left'], (blob.x_pos*(1000/1366), (blob_y_pos*(400/768))))
                else:
                    gameplay_surface.blit(image_cache[pname+'dead_left'], (blob.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        else:
            blob_y_pos = blob.y_pos - (image_cache[pname+'blob_right'].get_height() - 66)
            if(blob.facing == "right"):
                gameplay_surface.blit(image_cache[pname+'damage_right'], (blob.x_pos*(1000/1366), (blob_y_pos*(400/768))))
            else:
                gameplay_surface.blit(image_cache[pname+'damage_left'], (blob.x_pos*(1000/1366), (blob_y_pos*(400/768))))

        draw_blob_special(blob, gameplay_surface)
        draw_blob_particles(gameplay_surface, blobs.values()) # TODO: Fix this!

        if(blob.status_effects['menu']['open']):
            draw_menu(gameplay_surface, blob)
        


    #fade_out = 200
    # TODO: Loop over balls that exist (or don't!)
    for ball in balls.values():
        draw_ball_particles(gameplay_surface, ball, blobs.values())
        draw_ball(gameplay_surface, ball)
        draw_ball_overlay(gameplay_surface, ball, blobs.values())

    draw_environmental_modifiers(gameplay_surface)

    menu_font = image_cache['menu_font']
    menu_text = menu_font.render("SCORE: "+ str(game_score[0]) + "-" + str(game_score[1]), False, (200, 230, 200))
    text_rect = menu_text.get_rect()
    text_rect.center = (683, 40.5)
    gameplay_surface.blit(menu_text, text_rect)
    try:
        menu_text = menu_font.render("TIME: "+ '{:.2f}'.format(round(game_time/60, 2)), False, (200, 230, 200))
    except:
        menu_text = menu_font.render("NO TIME LIMIT", False, (0, 0, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (683, 81)
    gameplay_surface.blit(menu_text, text_rect)
    
    draw_ui(gameplay_surface, blobs.values())    
    draw_timer(gameplay_surface, timer)

    if settings['ui_mode']:
        game_display.blit(gameplay_surface, (0, 0)) # Default drawing
    else:
        # TODO: Make this blit function cleaner - split the background into probably 3 files
        game_display.blit(gameplay_surface, (0, 0), area = (0, 112, 1366, 670)) # The field
        game_display.blit(gameplay_surface, (0, 656), area = (0, 0, 1366, 112)) # The UI
        game_display.blit(gameplay_surface, (0, 766), area = (0, 70, 1366, 73)) # UI Padding at the Bottom