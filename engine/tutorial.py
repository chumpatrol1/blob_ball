import engine.blobs.blob_handler
from engine.ball import Ball, type_to_image
from engine.handle_input import gameplay_input, menu_input, merge_inputs
from engine.environmental_modifiers import clear_environmental_modifiers, return_environmental_modifiers, update_environmental_modifiers
from engine.endgame import save_tutorial_stats
from resources.sound_engine.sfx_event import createSFXEvent
# Is similar to gameplay.py
# Step 1: Move Left/Right
# Step 2: Jumping
# Step 3: Kicking the ball, but there's an invisible wall that prevents us from moving!


# Tutorial has speedrun clock
# Blobs have special "tutorial_move" function which filters out certain inputs depending on the tutorial stage
# Stage 1: Horizontal movement. Push the ball into the goal to advance to the next stage
# Stage 2: Vertical movement. Jump over the ball, and push it into the goal to advance
# Stage 3: Kick. There's an invisible wall that can't be crossed, you need to kick the ball to advance
# Stage 4: Assault. KO the enemy blob
# Stage 5: Block. Ball is coming in but you can't move. Block 3 times to advance!
# Stage 6: Parry. Enemy is approaching and you need to parry.
# Stage 7: Boost. Move across the field to score a goal within the time limit
# Stage 8: Boost Kick. Regenerating Blob needs to be OHKO'd.
# Stage 9: Focusing. Charge ability energy to maximum within the time limit.
# Stage 10: Ability (Cop). Shows off instant abilities. Use to stop the ball before it reaches the goal
# Stage 11: Ability (Wind). Shows off held abilities. Use to push the ball into the goal.
# Stage 12: Ability (Boxer). Shows off delayed abilities. Also touches on Danger Zone.
# Stage 13: CPU Match. Put it all together!

tutorial_page, countdown, countdown2, blobs, balls, game_score, timer, time_limit, completion_times = 0, 0, 0, {}, {}, [0, 0], 0, 0, {}

def reset_tutorial():
    global tutorial_page, countdown, countdown2, blobs, balls, game_score, timer, time_limit, completion_times
    tutorial_page = 0
    countdown = 0
    countdown2 = 0
    blobs = {}
    balls = {}
    game_score = [0, 0]
    timer = 0
    time_limit = 0
    completion_times = {}

reset_tutorial()

def initialize_scenario(page):
    global blobs
    global balls
    global countdown2

    if(page == 0):
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball()}
        balls[1].all_blobs = blobs
    elif(page == 1):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 1600, facing = 'left')}
        balls = {1: Ball()}
        balls[1].all_blobs = blobs
    elif(page == 2):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball(y_pos = 1240)}
        balls[1].all_blobs = blobs
    elif(page == 3):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 100, facing = 'right'), 2: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 2, x_pos = 800, facing = 'left', stat_overrides={'max_hp': 2})}
        balls = {}
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    elif(page == 4):
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball(x_pos = 1200, y_pos = 1240, x_speed = -20, y_speed = -30)}
        balls[1].all_blobs = blobs
    elif(page == 5):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 100, facing = 'right', stat_overrides={"block_cooldown_rate": 18}), 2: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 2, x_pos = 1450, facing = 'left', stat_overrides={"kick_cooldown_rate": 10})}
        balls = {}
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    elif(page == 6):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='king')(player = 1, x_pos = 150, facing = 'right')}
        blobs[1].special_ability_meter = 3000
        balls = {1: Ball(x_pos = 1500, y_pos = 1240)}
        balls[1].all_blobs = blobs
        countdown2 = 120
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    elif(page == 7):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 1, x_pos = 100, facing = 'right', stat_overrides={'kick_cooldown_rate': 20}), 2: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 2, x_pos = 800, facing = 'left', stat_overrides={'max_hp': 3})}
        blobs[1].special_ability_meter = 840
        balls = {}
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    elif(page == 8):
        countdown2 = 600
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='rock')(player = 1, x_pos = 100, facing = 'right')}
        balls = {}
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    elif(page == 9):
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='cop')(player = 1, x_pos = 1600, facing = 'left')}
        blobs[1].special_ability_meter = 4500
        balls = {1: Ball(x_pos = 1200, y_pos = 1240, x_speed = -20, y_speed = -30)}
        balls[1].all_blobs = blobs
    elif(page == 10):
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='wind')(player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball(x_pos = 902)}
        balls[1].all_blobs = blobs
    elif(page == 11):
        blobs = {1: engine.blobs.blob_handler.blob_list.get_blob(blob_id='boxer')(player = 1, x_pos = 100, facing = 'right'), 2: engine.blobs.blob_handler.blob_list.get_blob(blob_id='quirkless')(player = 2, x_pos = 1600, facing = 'left')}
        blobs[1].all_blobs = blobs
        blobs[2].all_blobs = blobs
        balls = {}
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    elif(page == 12):
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    page += 1

    return page

def check_if_requirements_met(page):
    global countdown, countdown2
    return_value = page
    if(page == 0):
        return initialize_scenario(page)
    elif(page == 1 or page == 2 or page == 3 or page == 11):
        if(balls[1].x_pos > 1745 and balls[1].y_pos > 925 and not balls[1].species == "goal_ball"): #Left Goal
            createSFXEvent('goal')
            balls[1].image = type_to_image("goal_ball")
            balls[1].species = "goal_ball"
            countdown = 60
        elif(balls[1].species == "goal_ball"):
            balls[1].special_timer = 2
            for blob in blobs.values():
                blob.impact_land_frames = 0
                blob.used_ability = {}
            countdown -= 1
            if(countdown == 0):
                return initialize_scenario(page)
        elif(balls[1].x_pos < 60 and balls[1].y_pos > 925):
            createSFXEvent('chime_error')
            return initialize_scenario(page - 1)
    elif(page == 4):
        if(blobs[2].hp <= 0):
            blobs[2].blob_ko()
        if(blobs[2].y_pos >= 1800):
            createSFXEvent('goal')
            return initialize_scenario(page)
    elif(page == 5 or page == 10):
        if(balls[1].x_pos < 60 and balls[1].y_pos > 925):
            createSFXEvent('chime_error')
            return initialize_scenario(page - 1)
        elif(balls[1].species == "blocked_ball" and balls[1].special_timer == 1):
            createSFXEvent('goal')
            return initialize_scenario(page)
        elif(balls[1].x_speed == 0 and balls[1].y_speed == 0 and not balls[1].species == "blocked_ball"):
            return initialize_scenario(page - 1)
    elif(page == 6):
        if(blobs[1].info['parries'] > 0):
            countdown2 -= 1
            if(countdown2 == 0):
                return initialize_scenario(page)
        
        if(blobs[1].hp <= 0):
            blobs[1].blob_ko()

        if(blobs[1].y_pos >= 1800):
            createSFXEvent('chime_error')
            return initialize_scenario(page - 1)
    elif(page == 7):
        if(balls[1].x_pos > 1745 and balls[1].y_pos > 925 and not balls[1].species == "goal_ball"): #Left Goal
            createSFXEvent('goal')
            balls[1].image = type_to_image("goal_ball")
            balls[1].species = "goal_ball"
            countdown = 60
        elif(balls[1].species == "goal_ball"):
            balls[1].special_timer = 2
            for blob in blobs.values():
                blob.impact_land_frames = 0
                blob.used_ability = {}
            countdown -= 1
            if(countdown == 0):
                return initialize_scenario(page)
        elif(countdown2 == 0):
            createSFXEvent('chime_error')
            return initialize_scenario(page - 1)
    elif(page == 8):
        if(blobs[2].hp <= 0):
            blobs[2].blob_ko()
        elif(blobs[2].hp != 3):
            blobs[2].heal_hp(3-blobs[2].hp)
        if(blobs[2].y_pos >= 1800):
            createSFXEvent('goal')
            return initialize_scenario(page)
    elif(page == 9):
        if(countdown2 == 0):
            createSFXEvent('chime_error')
            return initialize_scenario(page - 1)
        if(blobs[1].special_ability_meter >= 9000):
            createSFXEvent('goal')
            return initialize_scenario(page)
    elif(page == 12):
        if(blobs[2].status_effects['stunned'] == 30):
            createSFXEvent('goal')
        if(blobs[2].status_effects['stunned'] == 1):
            return initialize_scenario(page)
        if(blobs[2].hp < blobs[2].max_hp and not blobs[2].status_effects['stunned']):
            blobs[2].heal_hp(5)

    global time_limit
    global completion_times
    completion_times[page] = time_limit

    return return_value
    
def tutorial_1():
    '''
    Horizontal Movement
    '''
    # Step 1: 1 Blob. 1 Ball.
    merged = merge_inputs(gameplay_input(), True)
    pressed = []
    for key in merged:
        pressed.append("p1_" + key)

    # TODO: Environmental Modifiers?
    if(not countdown and blobs[1].hp > 0):
        blobs[1].move(pressed)

    update_environmental_modifiers()

    env_mod = return_environmental_modifiers()
    for blob in blobs.values():
        blob.check_environmental_collisions(env_mod)

    for ball in balls.values():
        ball.check_environmental_collisions(env_mod)
        ball.check_block_collisions()
        ball.check_blob_ability()

    if(not countdown):
        for blob in blobs.values():
            for other_blob in blobs.values():
                if(blob.kick_timer == 1 and blob.player != other_blob.player):
                    blob.check_blob_collision(other_blob)

        for blob in blobs.values():
            for other_blob in blobs.values():
                if(blob.player != other_blob.player):
                    blob.check_ability_collision(other_blob)

        # TODO: Check for Goals
        for blob in blobs.values():
            blob.cooldown()

    for ball in balls.values():
        ball.move()
        ball.check_blob_collisions()

def tutorial_3():
    tutorial_1()
    if(blobs[1].x_pos > 725):
        blobs[1].x_pos = 725

def tutorial_5():
    tutorial_1()
    blobs[1].x_pos, blobs[1].x_speed, blobs[1].facing = 100, 0, "right"

def tutorial_6():
    global countdown2
    tutorial_5()
    blobs[2].move(['p2_left', 'p2_kick'])
    if(blobs[1].parried == 1 or blobs[1].perfect_parried == 1):
        countdown2 = 60

def tutorial_7():
    global countdown2
    tutorial_1()
    countdown2 -= 1

def tutorial_12():
    tutorial_1()
    if(blobs[2].facing == 'left'):
        blobs[2].move(['p2_left'])
    else:
        blobs[2].move(['p2_right'])
    
    if(blobs[2].x_pos == 0):
        blobs[2].move(['p2_right'])
    elif(blobs[2].x_pos == 1700):
        blobs[2].move(['p2_left'])


stage_dict = {
    1: tutorial_1,
    2: tutorial_1,
    3: tutorial_3,
    4: tutorial_1,
    5: tutorial_5,
    6: tutorial_6,
    7: tutorial_7,
    8: tutorial_1,
    9: tutorial_7,
    10: tutorial_1,
    11: tutorial_5,
    12: tutorial_12,
}

def handle_tutorial():
    global tutorial_page
    global timer
    global time_limit
    game_state = "tutorial"
    tutorial_page = check_if_requirements_met(tutorial_page)
    try:
        stage_dict[tutorial_page]()
    except:
        print("Tutorial completed in", time_limit)
        to_draw = [blobs, balls, game_score, timer, time_limit]
        tutorial_page = 0
        timer = 0
        time_limit = 0
        save_tutorial_stats(to_draw)
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
        return "tutorial_complete", [1, to_draw]

    to_draw = [blobs, balls, game_score, timer, time_limit]
    time_limit += 1
    return game_state, [tutorial_page, to_draw]

player_ready = False
flash_timer = 0

def handle_tutorial_menu(timer):
    global player_ready
    global flash_timer
    global completion_times
    pressed = merge_inputs(menu_input(), True)

    if("ability" in pressed and not timer):
        player_ready = True

    if(not player_ready):
        game_state = "tutorial_complete"
    else:
        game_state = "main_menu"
        player_ready = False
        from resources.graphics_engine.display_gameplay import unload_image_cache
        unload_image_cache()
    
    flash_timer += 1
    if(flash_timer > 90):
        flash_timer = 0
    return game_state, [flash_timer, completion_times]