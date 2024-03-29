import random

# Old CPU Logic. At the very least, this will be replaced with the "classic" beta logic playstyle
# which includes kicking the ball and using boosts.
def handle_logic(blob, other_blob, ball, game_score, timer):
    '''
    Blob is the CPU blob
    Other_blob is the other blob
    Ball is the ball

    Returns pressed (the inputs that the blob will do)
    Returns logic_memory (which lets the blob remember what sort of playstyle or decisions it has done recently)
    '''

    '''
    There are 8 inputs that blobs will accept:
    left (Left input)
    right (Right input)
    up (Upwards input, does a jump)
    down (Downwards input, which can activate a focus while grounded, or a fastfall in the air)
    
    ability (Ability input, which can activate a special power. 
    Powers are usually either single input (ex: Gale, Spire) or held (ex: Fireball, Geyser))
    kick (Kick input, which does damage and smacks the ball really hard)
    blob (Block input, which protects against kicks and can stop the ball)
    boost (Boost input, which increases player stats greatly)
    '''

    '''
    Note to BoingK (8/30/2021):
    Feel free to play with whatever code you'd like to. Don't hesitate to DM me
    If the program compiles I'm fine with it, so don't hesitate to commit things to the dev build!
    Add whatever logic you'd like
    '''
    pressed = []
    logic_memory = blob.cpu_memory
    #Aggress/Defend?
    if ((blob.x_center < ball.x_center+60) and (blob.player != 1)) or ((blob.x_center > ball.x_center-60) and (blob.player == 1)):
        logic_memory = ['defensive']
    elif (abs(other_blob.x_center - ball.x_center)>200)and(((other_blob.facing=='left')and(other_blob.player==1))or((other_blob.facing=='right')and(other_blob.player!=1))):
        logic_memory = ['agressive']
    elif (abs(blob.x_center - ball.x_center) < 600) and (abs(blob.x_center - ball.x_center) < abs(other_blob.x_center - ball.x_center)):
        logic_memory = ['agressive']
    elif abs(other_blob.x_center - ball.x_center) < 500:
        if abs(blob.x_center - ball.x_center) > 500:
            logic_memory = ['agressive']
        if abs(blob.x_center - ball.x_center) < 500:
            logic_memory = ['defensive']
    else:
        logic_memory = ['agressive']
    #Jump?
    if (abs(blob.x_center - ball.x_center)<150) and (blob.y_center>ball.y_center):
        logic_memory.append('jump')

    #Kick?
    if(blob.kick_cooldown == 0 and abs(blob.x_center - other_blob.x_center) <= 150):
        if(random.randint(0, 50) == 0):
            pressed.append('kick')


    #Logic for each strategy goes here
    if(blob.player == 1):
        if 'agressive' in logic_memory:
            pressed.append('right')
        if 'defensive' in logic_memory:
            pressed.append('left')
    else:
        if 'agressive' in logic_memory:
            pressed.append('left')
        if 'defensive' in logic_memory:
            pressed.append('right')
    if 'jump' in logic_memory:
        pressed.append('up')

    #Converts the logic to something readable by the blob's movement function
    if(blob.player == 1):
        for i in range(len(pressed)):
            pressed[i] = "p1_" + pressed[i]
    else:
        for i in range(len(pressed)):
            pressed[i] = "p2_" + pressed[i]

    return pressed, logic_memory

def find_position(blob): # Finds the position of the blob relative to their own goal
    if(blob.player == 1):
        if(blob.x_pos < 325):
            self_position = "home_dz"
        elif(blob.x_pos < 600):
            self_position = "home_mid"
        elif(blob.x_pos < 1100):
            self_position = "mid"
        elif(blob.x_pos < 1375):
            self_position = "away_mid"
        else:
            self_position = "away_dz"
    else:
        if(blob.x_pos < 325):
            self_position = "away_dz"
        elif(blob.x_pos < 600):
            self_position = "away_mid"
        elif(blob.x_pos < 1100):
            self_position = "mid"
        elif(blob.x_pos < 1375):
            self_position = "home_mid"
        else:
            self_position = "home_dz"
    return self_position

def find_ball_loc(ball, blob): # Finds the position of the ball relative to the blob.
    # There might be some sort of bug, I don't know. I made this at 4AM.
    if(830 < ball.x_center < 1030):
        ball_position = "mid"
    else:
        if(blob.player == 1):
            if(ball.x_center < 275):
                ball_position = "home_dz"
            elif(ball.x_center < 850):
                ball_position = "home_mid"
            elif(ball.x_center > 1600):
                ball_position = "away_dz"
            else:
                ball_position = "away_mid"
        else:
            if(ball.x_center < 275):
                ball_position = "away_dz"
            elif(ball.x_center < 850):
                ball_position = "away_mid"
            elif(ball.x_center > 1600):
                ball_position = "home_dz"
            else:
                ball_position = "home_mid"
    return ball_position

def check_if_winning(blob, game_score):
    # Checks if this blob is winning.
    # Not sure if we need to use this very much.
    if(blob.player == 1):
        if(game_score[0] > game_score[1]):
            winning = "winning"
        elif(game_score[1] > game_score[0]):
            winning = "losing"
        else:
            if(game_score[0] == 0):
                winning = "game_start"
            else:
                winning = "tied"

    else:
        if(game_score[0] < game_score[1]):
            winning = "winning"
        elif(game_score[1] < game_score[0]):
            winning = "losing"
        else:
            if(game_score[0] == 0):
                winning = "game_start"
            else:
                winning = "tied"
    
    return winning

def compile_openings(blob, other_blob):
    # Options: You are expensive t/f, you are fast t/f, enemy is expensive t/f, enemy is fast t/f
    self_fast = bool(blob.top_speed > 13 and blob.top_speed > other_blob.top_speed)
    self_expensive = bool(blob.special_ability_cost >= 600) or bool(blob.ability_classification == "held")
    foe_fast = bool(other_blob.top_speed > 13 and other_blob.top_speed > blob.top_speed)
    foe_expensive = bool(other_blob.special_ability_cost >= 600)
    foe_low_hp = bool(other_blob.hp < 6)
    # You want to play 2 if you are fast and your ability is inexpensive
    # You want to play 1 if you are slow and your ability is expensive
    # You want to play 3 if you are fast and your ability is expensive
    # You want to play 3 if you are slow and your ability is inexpensive
    decision_array = []
    if(self_fast):
        decision_array += ['opening_2', 'opening_2', 'opening_3']
    if(self_expensive):
        decision_array += ['opening_1', 'opening_1', 'opening_3']
    if(foe_fast):
        decision_array += ['opening_3', 'opening_3', 'opening_1']
    if(foe_expensive):
        decision_array += ['opening_2', 'opening_2', 'opening_1']
    if(foe_low_hp):
        decision_array += ['opening_4', 'opening_4', 'opening_4']
    return decision_array # This is a combination of all valid openings we can play, one of which is chosen randomly

def block_attacks(blob, other_blob, pressed):
    if(blob.block_cooldown == 0 and 150 > abs(blob.x_center - other_blob.x_center)\
        and other_blob.kick_cooldown == 0 and \
        random.randint(0, 35 - (blob.hp + (5 * int(blob.player == 1 and blob.x_pos <= blob.danger_zone) \
        + (5 * int(bool(other_blob.boost_timer)))))) == 0): # More likely to block if in danger or enemy boosting
        pressed.append('block') # More likely to block the lower hp we have

    if((other_blob.used_ability == "spire_wait" or other_blob.used_ability == "thunderbolt_wait" or other_blob.used_ability == "starpunch_wait") and random.randint(0, 40 - (other_blob.special_ability_cooldown_max - other_blob.special_ability_timer)) == 0):
        pressed.append('block')

def fire_blob(blob, other_blob, ball, pressed):
    if(blob.player == 1 and ball.x_speed > 0 and (ball.y_speed > -15 or ball.y_pos > 925) and (blob.special_ability_meter > blob.special_ability_cost * 2.5 or blob.ability_holding_timer > 0 or ball.x_pos > 1605)):
        pressed.append('ability')
    elif(blob.player == 2 and ball.x_speed < 0 and (ball.y_speed > -15 or ball.y_pos > 925) and (blob.special_ability_meter > blob.special_ability_cost * 2.5 or blob.ability_holding_timer > 0 or ball.x_pos < 200)):
        pressed.append('ability')

def ice_blob(blob, other_blob, ball, pressed):
    if(blob.player == 1 and ball.x_speed < -10 and (ball.y_speed > -15 or ball.y_pos > 925) and (blob.special_ability_meter > blob.special_ability_cost * 2.5 or blob.ability_holding_timer > 0 or ball.x_pos < 400)):
        pressed.append('ability')
    elif(blob.player == 2 and ball.x_speed > 10 and (ball.y_speed > -15 or ball.y_pos > 925) and (blob.special_ability_meter > blob.special_ability_cost * 2.5 or blob.ability_holding_timer > 0 or ball.x_pos > 1405)):
        pressed.append('ability')

def water_blob(blob, other_blob, ball, pressed):
    if(blob.player == 1 and ball.x_speed < -10 and (ball.y_speed > -15 or ball.y_pos > 925) and (blob.special_ability_meter > blob.special_ability_cost * 2.5 or blob.ability_holding_timer > 0 or ball.x_pos < 300)):
        pressed.append('ability')
        blob.cpu_memory['press_queue'].append('ability')
    elif(blob.player == 2 and ball.x_speed > 10 and (ball.y_speed > -15 or ball.y_pos > 925) and (blob.special_ability_meter > blob.special_ability_cost * 2.5 or blob.ability_holding_timer > 0 or ball.x_pos > 1505)):
        pressed.append('ability')
        blob.cpu_memory['press_queue'].append('ability')

def rock_blob(blob, other_blob, ball, pressed):
    if(blob.player == 1 and ball.x_pos + (ball.x_speed * blob.special_ability_delay) < 100 and ball.y_pos + (ball.y_speed * blob.special_ability_timer) > 925):
        pressed.append('ability')
    elif(blob.player == 2 and ball.x_pos + (ball.x_speed * blob.special_ability_delay) > 1705 and ball.y_pos + (ball.y_speed * blob.special_ability_timer) > 925):
        pressed.append('ability')

def lightning_blob(blob, other_blob, ball, pressed):
    if(blob.player == 1 and ball.x_pos + (ball.x_speed * blob.special_ability_delay) > 1405 and ball.y_pos < 800 and ball.x_speed >= 0):
        pressed.append('ability')
    elif(blob.player == 2 and ball.x_pos + (ball.x_speed * blob.special_ability_delay) < 400 and ball.y_pos < 800 and ball.x_speed <= 0):
        pressed.append('ability')

def wind_blob(blob, other_blob, ball, pressed):
    # IF the ball is close to your goal
    # IF the ball is behind the enemy
    # IF SA Meter is 3x
    # IF we are already using ability
    if(blob.player == 1 and (ball.x_pos < 400 or (ball.x_pos > 1405 and other_blob.x_center < ball.x_center)) and  (ball.y_speed > -15 or ball.y_pos > 925) and (ball.x_speed > -10) and (blob.special_ability_meter > blob.special_ability_cost * 3 or blob.ability_holding_timer > 0)):
        pressed.append('ability')
        blob.cpu_memory['press_queue'].append('ability')
    elif(blob.player == 1 and (ball.x_pos > 1405 or (ball.x_pos < 400 and other_blob.x_center > ball.x_center)) and  (ball.y_speed > -15 or ball.y_pos > 925) and (ball.x_speed < 10) and (blob.special_ability_meter > blob.special_ability_cost * 3 or blob.ability_holding_timer > 0)):
        pressed.append('ability')
        blob.cpu_memory['press_queue'].append('ability')

# This is the current version of handle_logic, the one that is going to V0.11.0b
def handle_logic_beta(blob, other_blob, ball, game_score, timer):

    pressed = []
    logic_memory = dict(blob.cpu_memory) # TODO: Remove this at some point
    blob.cpu_memory['press_queue'] = []
    '''
    Logic Memory:
    game_state: What state is the game currently in?
    current_play: What play are we attempting right now?
    press_queue: What buttons are queued for next frame?
    '''
    for key in logic_memory['press_queue']:
        pressed.append(key)

    # The first action we take is to check and update the current game state
    # There are 3 right now, one for openings, one to continue openings, and other cases
    # Based on the game state, we store the current play
    # Based on the current play, we take action

    # Identify the Game State
    self_position = find_position(blob) # Position is relative to self
    foe_position = find_position(other_blob) # Position is relative to foe
    ball_position = find_ball_loc(ball, blob)
    score_position = check_if_winning(blob, game_score)
    
    if((self_position == "home_dz" or self_position == "home_mid") and foe_position == "home_dz" and ball_position == "mid" and abs(ball.x_speed) < 20):
        current_game_state = 'opening'
    elif(self_position == "mid" and foe_position == "home_dz" and (ball_position == "mid" or ball_position == "foe_mid" or ball_position == "foe_dz")):
        current_game_state = 'sub_offense'
    else:
        current_game_state = 'other'

    #if not  (timer%60):
    #    print(logic_memory)

    # If the Game State is Different from the one in Memory, change your Play
    if(logic_memory['game_state'] != current_game_state):
        if(current_game_state == 'opening'):
            decision_array = compile_openings(blob, other_blob)
            if(score_position == "game_start"):
                decision_array.append('opening_1')
            else:
                decision_array.append('opening_3')
            logic_memory['current_play'] = random.choice(decision_array) # Stay at your goal and focus energy
        elif(current_game_state == 'sub_offense'):
            decision_array = compile_openings(blob, other_blob)
            if(score_position == "winning"):
                decision_array.append('opening_3')
            else:
                decision_array.append('opening_2')
            logic_memory['current_play'] = random.choice(decision_array)
        else:
            logic_memory['current_play'] = "classic" # BoingK CPU Time!
        logic_memory['game_state'] = current_game_state

    # Based on the Play, do an action.
    if(logic_memory['current_play'] == 'opening_1'): # Stay at your goal and focus energy
        pressed.append('down')
        if(blob.special_ability_meter > 0.8 * blob.special_ability_max):
            logic_memory['current_play'] = random.choice(['opening_2', 'opening_3'])
        block_attacks(blob, other_blob, pressed)
    elif(logic_memory['current_play'] == 'opening_2'): # Rush the ball!
        pressed.append('toward')
        if (abs(blob.x_center - ball.x_center)<150) and (blob.y_center - 125 > ball.y_center):
            pressed.append('up')
    
        if(blob.kick_cooldown == 0 and 150 < abs(blob.x_center - ball.x_center) < 185\
            and (blob.y_center > ball.y_center) and random.randint(0, 10) == 0):
            pressed.append('kick')

        if(blob.boost_cooldown_timer == 0 and blob.special_ability_meter >= blob.boost_cost and not random.randint(0, 5)):
            pressed.append('boost')
    elif(logic_memory['current_play'] == 'opening_3'): # Run to the ball and guard it
        if(abs(blob.x_center - ball.x_center) > 300):
            pressed.append('toward')
        else:
            if(abs(blob.x_center - other_blob.x_center) < 400 and random.randint(0, 20) == 0):
                if(blob.focus_lock):
                    pressed.append('up')
                    logic_memory['press_queue'].append('block')
                else:
                    pressed.append('block')
            else:
                pressed.append('down')
                if(blob.special_ability_meter > 0.8 * blob.special_ability_max):
                    logic_memory['current_play'] = 'opening_2'
    elif(logic_memory['current_play'] == 'opening_4'): # Kick the enemy to death.
        pressed.append('toward')
        if(blob.kick_cooldown == 0 and 150 > abs(blob.x_center - other_blob.x_center)\
            and random.randint(0, 5) == 0):
            pressed.append('kick')
            logic_memory['current_play'] = 'classic'
        
    elif(logic_memory['current_play'] == 'classic'): # BoingK Time!
        if ((blob.x_center < ball.x_center+60) and (blob.player != 1)) or ((blob.x_center > ball.x_center-60) and (blob.player == 1)):
            pressed.append('away')
        elif (abs(other_blob.x_center - ball.x_center)>200)and(((other_blob.facing=='left')and(other_blob.player==1))or((other_blob.facing=='right')and(other_blob.player!=1))):
            pressed.append('toward')
        elif (abs(blob.x_center - ball.x_center) < 600) and (abs(blob.x_center - ball.x_center) < abs(other_blob.x_center - ball.x_center)):
            pressed.append('toward')
        elif abs(other_blob.x_center - ball.x_center) < 500:
            if abs(blob.x_center - ball.x_center) > 500:
                pressed.append('toward')
            if abs(blob.x_center - ball.x_center) < 500:
                pressed.append('away')
        else:
            pressed.append('toward')
        #Jump?
        if (abs(blob.x_center - ball.x_center)<150) and (blob.y_center - 125>ball.y_center):
            pressed.append('up')
        
        kick_chance = 10 # Smaller is better
        if(other_blob.hp < 6): # Almost dead? Finish him!
            kick_chance -= 1
        if(other_blob.player == 1 and other_blob.x_pos <= other_blob.danger_zone) or (other_blob.player == 2 and other_blob.x_pos >= other_blob.danger_zone):
            kick_chance -= 1 # Enemy in danger zone? Finish him!
        if(blob.boost_timer): # Boosting? Finish him!
            kick_chance -= 2

        if(blob.kick_cooldown == 0 and 150 < abs(blob.x_center - ball.x_center) < 185\
            and (blob.y_center > ball.y_center) and random.randint(0, 10) == 0):
            if(blob.player == 1 and blob.x_center < ball.x_center):
                pressed.append('kick')
            elif(blob.player == 2 and blob.x_center > ball.x_center):
                pressed.append('kick')

        if(blob.kick_cooldown == 0 and 150 > abs(blob.x_center - other_blob.x_center)\
            and random.randint(0, kick_chance) == 0):
            pressed.append('kick')

        block_attacks(blob, other_blob, pressed)

        if(blob.boost_cooldown_timer == 0 and blob.special_ability_meter >= blob.boost_cost\
             and not random.randint(0, 5) and not (self_position == 'away_dz' or self_position == self_position == 'away_mid')):
            pressed.append('boost')

    ability_dict = {
        'fire': fire_blob,
        'ice': ice_blob,
        'water': water_blob,
        'rock': rock_blob,
        'lightning': lightning_blob,
        'wind': wind_blob,
    }
    if(blob.species in ability_dict):
        ability_dict[blob.species](blob, other_blob, ball, pressed)

    # Convert to Player Specific Move Codes
    if(blob.player == 1):
        for i in range(len(pressed)):
            if(pressed[i] == 'toward'):
                pressed[i] = 'right'
                if(blob.facing == 'left' and random.randint(0, 4) > 1): # Wavebounce suppression
                    pressed.append('p1_left')
            elif(pressed[i] == 'away'):
                pressed[i] = 'left'
                if(blob.facing == 'right' and random.randint(0, 4) > 1): # Wavebounce suppression
                    pressed.append('p1_right')
            pressed[i] = "p1_" + pressed[i]
    else:
        for i in range(len(pressed)):
            if(pressed[i] == 'toward'):
                pressed[i] = 'left'
                if(blob.facing == 'right' and random.randint(0, 4) > 1): # Wavebounce suppression
                    pressed.append('p2_right')
            elif(pressed[i] == 'away'):
                pressed[i] = 'right'
                if(blob.facing == 'left' and random.randint(0, 4) > 1): # Wavebounce suppression
                    pressed.append('p2_left')
                
            pressed[i] = "p2_" + pressed[i]

    return pressed, logic_memory