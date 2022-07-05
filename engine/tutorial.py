from engine.blobs import Blob
from engine.ball import Ball
from engine.handle_input import gameplay_input
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

    blobs[1].move(pressed)
    # TODO: Fix the move function!
    balls[1].move(blobs[1], blobs[1])


    to_draw = [blobs, balls, game_score, timer, time_limit]

    return game_state, [tutorial_page, to_draw]