from engine.blobs import Blob
from engine.ball import Ball, type_to_image
from engine.handle_input import gameplay_input
from engine.environmental_modifiers import clear_environmental_modifiers, return_environmental_modifiers, update_environmental_modifiers
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

tutorial_page, countdown, blobs, balls, game_score, timer, time_limit = 0, 0, {}, {}, [0, 0], 0, None

def reset_tutorial():
    global tutorial_page, countdown, blobs, balls, game_score, timer, time_limit
    tutorial_page = 0
    countdown = 0
    blobs = {}
    balls = {}
    game_score = [0, 0]
    timer = 0
    time_limit = None

reset_tutorial()

def initialize_scenario(page):
    global blobs
    global balls
    if(page == 0):
        
        blobs = {1: Blob(species = 'quirkless', player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball()}
        balls[1].all_blobs = blobs
    elif(page == 1):
        blobs = {1: Blob(species = 'quirkless', player = 1, x_pos = 1600, facing = 'left')}
        balls = {1: Ball()}
        balls[1].all_blobs = blobs
    elif(page == 2):
        blobs = {1: Blob(species = 'quirkless', player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball(y_pos = 1240)}
        balls[1].all_blobs = blobs

    page += 1

    return page

def check_if_requirements_met(page):
    global countdown
    return_value = page
    if(page == 0):
        return initialize_scenario(page)
    elif(page == 1 or page == 2 or page == 3):
        if(balls[1].x_pos > 1745 and balls[1].y_pos > 925 and not balls[1].species == "goal_ball"): #Left Goal
            createSFXEvent('goal')
            balls[1].image = type_to_image("goal_ball")
            balls[1].species = "goal_ball"
            countdown = 60
        elif(balls[1].species == "goal_ball"):
            balls[1].special_timer = 2
            for blob in blobs.values():
                blob.impact_land_frames = 0
                blob.used_ability = ""
            countdown -= 1
            if(countdown == 0):
                return initialize_scenario(page)
    return return_value
    
def tutorial_1():
    '''
    Horizontal Movement
    '''
    # Step 1: 1 Blob. 1 Ball.
    pressed = gameplay_input()
    # TODO: Environmental Modifiers?
    if(not countdown):
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


stage_dict = {
    1: tutorial_1,
    2: tutorial_1,
    3: tutorial_3,
}

def handle_tutorial():
    global tutorial_page
    game_state = "tutorial"
    tutorial_page = check_if_requirements_met(tutorial_page)
    try:
        stage_dict[tutorial_page]()
    except:
        to_draw = [blobs, balls, game_score, timer, time_limit]
        tutorial_page = 0
        return "main_menu", [1, to_draw]

    to_draw = [blobs, balls, game_score, timer, time_limit]

    return game_state, [tutorial_page, to_draw]