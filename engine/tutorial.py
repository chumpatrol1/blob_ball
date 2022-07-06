from engine.blobs import Blob
from engine.ball import Ball
from engine.handle_input import gameplay_input
from engine.environmental_modifiers import clear_environmental_modifiers, return_environmental_modifiers, update_environmental_modifiers
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

tutorial_page = 0
blobs = {}
balls = {}
game_score = [0, 0]
timer = 0
time_limit = None

def initialize_scenario(page):

    if(page == 0):
        global blobs
        global balls
        blobs = {1: Blob(species = 'quirkless', player = 1, x_pos = 100, facing = 'right')}
        balls = {1: Ball()}
        balls[1].all_blobs = blobs
    
    page += 1

    return page

def check_if_requirements_met(page):
    if(page == 0):
        return initialize_scenario(page)
    else:
        return page
    



def handle_tutorial():
    global tutorial_page
    game_state = "tutorial"
    tutorial_page = check_if_requirements_met(tutorial_page)

    # Step 1: 1 Blob. 1 Ball.
    pressed = gameplay_input()
    # TODO: Environmental Modifiers?
    blobs[1].move(pressed)

    update_environmental_modifiers()

    env_mod = return_environmental_modifiers()
    for blob in blobs.values():
        blob.check_environmental_collisions(env_mod)

    for ball in balls.values():
        ball.check_environmental_collisions(env_mod)
        ball.check_block_collisions()
        ball.check_blob_ability()

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


    to_draw = [blobs, balls, game_score, timer, time_limit]

    return game_state, [tutorial_page, to_draw]