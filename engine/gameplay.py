import pygame as pg
import sys
from engine.environmental_modifiers import clear_environmental_modifiers, return_environmental_modifiers, update_environmental_modifiers
import engine.handle_input
import engine.blobs
import engine.ball
import time
from json import dumps, loads
from engine.endgame import update_game_stats, update_mu_chart
from engine.replays import return_replay_info, save_replay
from resources.graphics_engine.display_graphics import capture_screen
import engine.cpu_logic
import random
from resources.graphics_engine.display_particles import clear_particle_memory
from resources.sound_engine.sfx_event import createSFXEvent
random_seed = None
def initialize_players(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu, set_seed = None, p1_costume = 0, p2_costume = 0):
    global random_seed
    if(set_seed == None):
        random_seed = random.randint(-2147483648, 2147483647)
    else:
        random_seed = set_seed
    random.seed(random_seed)
    global goal_limit
    global time_limit
    global time_bonus
    p1_blob = engine.blobs.Blob(species = p1_selected, player = 1, x_pos = 100, facing = 'right', special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'], is_cpu = p1_is_cpu, stat_overrides = ruleset['p1_modifiers'], costume = p1_costume)
    p2_blob = engine.blobs.Blob(species = p2_selected, player = 2, x_pos = 1600, facing = 'left', special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'], is_cpu = p2_is_cpu, stat_overrides = ruleset['p2_modifiers'], costume = p2_costume)
    ball = engine.ball.Ball()
    goal_limit = ruleset['goal_limit']
    if(ruleset['time_limit'] == 0):
        time_limit = "NO LIMIT"
    else:
        time_limit = ruleset['time_limit']
    time_bonus = ruleset['time_bonus']
    return p1_blob, p2_blob, ball

initialized = False
p1_blob = None
p2_blob = None
blob_dict = {}
ball = None
ball_dict = {}
game_score = [0, 0]
timer = 180
countdown = 0
p1_ko = False
p2_ko = False
goal_scored = False
goal_scorer = None
replay_inputs = []
#goal_limit = 5 #Defaults to 5 goals
#time_limit = 3600 #Defaults to 3600, or 1 minute
#time_bonus = 600 #Defaults to 600, or 10 seconds
game_info = {
        'game_score': game_score,
        'time': 0,
        'time_seconds': 0,
        'avg_collisions_per_goal': 0,
        }

def reset_round(ruleset):
    global p1_blob
    global p2_blob
    global ball
    global p1_ko
    global p2_ko
    p1_blob.reset(ruleset)
    p2_blob.reset(ruleset)
    ball.reset()
    p1_ko = False
    p2_ko = False
    clear_environmental_modifiers()

def score_goal(winner, goal_limit, ruleset, is_replay = False):
    global timer
    global time_limit
    global time_bonus
    if not time_limit == "NO LIMIT":
        time_limit += time_bonus
    game_score[winner] += 1
    timer = 60
    if(game_score[winner] >= goal_limit):
        if(game_score[0] != game_score[1]):
            return "casual_win", (winner + 1)
        else:
            return "casual_win", 3
    #reset_round(ruleset)
    if(is_replay):
        return "replay_match", 0
    else:
        return "casual_match", 0

input_to_code = {
    'p1_ability': '1',
    'p1_kick': '2',
    'p1_block': '3',
    'p1_boost': '4',
    'p1_up': '5',
    'p1_down': '6',
    'p1_left': '7',
    'p1_right': '8',
    'p2_ability': 'a',
    'p2_kick': 'b',
    'p2_block': 'c',
    'p2_boost': 'd',
    'p2_up': 'e',
    'p2_down': 'f',
    'p2_left': 'g',
    'p2_right': 'h',
    
}
def convert_inputs_to_replay(inputs, player):
    global input_to_code
    encoded_string = ""
    for rinput in inputs:
        input = "p" + str(player) + "_" + rinput
        if(input in input_to_code):
            encoded_string += input_to_code[input]
    return encoded_string

code_to_input = {v: k for k, v in input_to_code.items()} # All keys are now values

def convert_replay_to_inputs(inputs):
    global input_to_code
    decoded_inputs = []
    for rinput in inputs:
        decoded_inputs.append(code_to_input[rinput])
    return decoded_inputs

def handle_gameplay(player_info, ruleset, settings, pause_timer, is_replay = False):
    # TODO: For loop that allows you to have variable blobs
    
    if(is_replay):
        game_state = "replay_match"
        #if(game_info['time'] > 2460):
        #    print(return_replay_info()[4][game_info['time']:])
        try:
            pressed = return_replay_info()[6][game_info['time']]
        except:
            print(game_info['time'])
            clear_particle_memory()
            raise KeyError
        pressed = convert_replay_to_inputs(pressed)
    else:
        game_state = "casual_match"
        pressed = engine.handle_input.gameplay_input()
    global initialized
    global p1_blob
    global p2_blob
    global ball
    global game_score
    global timer
    global p1_ko
    global p2_ko
    global countdown
    global goal_scorer
    global goal_scored
    global score_goal
    global goal_limit
    global time_limit
    global replay_inputs
    global blob_dict
    global ball_dict
    
    if('escape' in pressed and not pause_timer):
        game_state = "pause"
        capture_screen()
    elif(is_replay):
        pause_check = engine.handle_input.gameplay_input()
        if('escape' in pause_check and not pause_timer):
            game_state = "pause"
            capture_screen()
            game_state = "replay_pause"


    def blob_ko(blob):
        blob.blob_ko()

    # TODO: For loopify everything so the game will run regardless of blobs + balls loaded

    if not initialized:
        '''
        Upon game startup, initialize all the actors
        '''
        if(is_replay):
            blobs = initialize_players(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu, p1_costume=p1_costume, p2_costume=p2_costume, set_seed = return_replay_info()[0])
        else:
            blobs = initialize_players(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu, p1_costume=p1_costume, p2_costume=p2_costume)
        p1_blob = blobs[0]
        p2_blob = blobs[1]
        ball = blobs[2]
        blob_dict = {
            1: p1_blob,
            2: p2_blob
        }
        p1_blob.all_blobs = blob_dict
        p2_blob.all_blobs = blob_dict
        ball_dict = {
            0: ball
        }        
        ball.all_blobs = blob_dict
        initialized = True
    else:
        if(timer == 0):
            movement_string = ""
            if(p1_blob.is_cpu):
                cpu_logic, cpu_memory = engine.cpu_logic.handle_logic_beta(p1_blob, p2_blob, ball, game_score, game_info['time'])
                p1_blob.cpu_memory = cpu_memory
                movement_string += convert_inputs_to_replay(p1_blob.move(cpu_logic), 1)
            else:
                movement_string += convert_inputs_to_replay(p1_blob.move(pressed), 1)
            if(p2_blob.is_cpu):
                cpu_logic, cpu_memory = engine.cpu_logic.handle_logic_beta(p2_blob, p1_blob, ball, game_score, game_info['time'])
                p2_blob.cpu_memory = cpu_memory
                
                movement_string += convert_inputs_to_replay(p2_blob.move(cpu_logic), 2)
            else:
                movement_string += convert_inputs_to_replay(p2_blob.move(pressed), 2)
            
            #print(game_info['time'], movement_string)
            replay_inputs.append(movement_string)

            update_environmental_modifiers()

            env_mod = return_environmental_modifiers()
            for blob in blob_dict.values():
                blob.check_environmental_collisions(env_mod)

            for sball in ball_dict.values():
                sball.check_environmental_collisions(env_mod)
                sball.check_block_collisions()
                sball.check_blob_ability()
                
            for blob in blob_dict.values():
                for other_blob in blob_dict.values():
                    if(blob.kick_timer == 1 and blob.player != other_blob.player):
                        blob.check_blob_collision(other_blob)

            for blob in blob_dict.values():
                for other_blob in blob_dict.values():

                    if(blob.player != other_blob.player):
                        blob.check_ability_collision(other_blob)

            # TODO: Figure out how to loopify this
            if(p2_blob.hp <= 0):
                    timer = 120
                    p2_ko = True
                    p1_blob.cooldown()
                    p1_blob.info['points_from_kos'] += 1
                    p2_blob.damage_flash_timer = 0
            
            if(p1_blob.hp <= 0):
                    timer = 120
                    p1_ko = True
                    p2_blob.cooldown()
                    p2_blob.info['points_from_kos'] += 1
                    p1_blob.damage_flash_timer = 0

            for blob in blob_dict.values():
                blob.cooldown()

            for sball in ball_dict.values():
                sball.move()
                sball.check_blob_collisions()
                
            # TODO: Figure out how to handle goals
            if(ball.x_pos < 60 and ball.y_pos > 925): #Left Goal
                createSFXEvent('goal')
                goal_scorer = 1
                goal_scored = True
                countdown = 60
                timer = 60
                p2_blob.info['points_from_goals'] += 1
                
            elif(ball.x_pos > 1745 and ball.y_pos > 925): #Right Goal
                createSFXEvent('goal')            
                goal_scorer = 0
                goal_scored = True
                countdown = 60
                timer = 60
                p1_blob.info['points_from_goals'] += 1
            if not (ruleset['time_limit'] == 0):
                time_limit -= 1
                if(time_limit <= 0):
                    print("TIME UP?!")
                    if(game_score[0] > game_score[1]):
                        winner_info = 1
                    elif(game_score[0] < game_score[1]):
                        winner_info = 2
                    else:
                        winner_info = 3
                    game_state = "casual_win"
            game_info['time'] += 1
            
        else:
            '''
            Triggers upon scoring a goal or KO
            '''
            # TODO: Figure out how to handle KO's
            if(p1_ko and not p2_ko):
                blob_ko(p1_blob)
                if(p1_blob.y_pos >= 1800):
                    game_state, winner_info = score_goal(1, goal_limit, ruleset, is_replay)
                    p1_ko = False
                    p1_blob.hp = p1_blob.max_hp
                    reset_round(ruleset)

            elif(p2_ko and not p1_ko):
                blob_ko(p2_blob)
                if(p2_blob.y_pos >= 1800):
                    game_state, winner_info = score_goal(0, goal_limit, ruleset, is_replay)
                    p2_blob.hp = p2_blob.max_hp
                    p2_ko = False
                    reset_round(ruleset)
            elif(p1_ko and p2_ko):
                blob_ko(p1_blob)
                blob_ko(p2_blob)
                if(p1_blob.y_pos >= 1800 or p2_blob.y_pos >= 1800):
                    game_state, winner_info = score_goal(1, goal_limit, ruleset, is_replay)
                    game_state, winner_info = score_goal(0, goal_limit, ruleset, is_replay)
                    p1_ko, p2_ko = False, False
                    p1_blob.hp = p1_blob.max_hp
                    p2_blob.hp = p2_blob.max_hp
                    reset_round(ruleset)

            if(goal_scored):
                ball.image = engine.ball.type_to_image("goal_ball")
                ball.special_timer = 2
                ball.move()
                p1_blob.move([])
                p2_blob.move([])
                p1_blob.impact_land_frames = 0
                p2_blob.impact_land_frames = 0
                p1_blob.used_ability = {}
                p2_blob.used_ability = {}
                countdown -= 1
                if(countdown == 0):
                    game_state, winner_info = score_goal(goal_scorer, goal_limit, ruleset, is_replay)
                    goal_scored = False
                    goal_scorer = None
                    reset_round(ruleset)
            timer -= 1
            if timer == 0:
                p1_blob.heal_hp(ruleset['hp_regen'])
                p2_blob.heal_hp(ruleset['hp_regen'])

        if(game_state == "casual_win"):
            game_info["game_score"] = game_score
            game_info["time_seconds"] = round(game_info['time']/60, 2)
            try:
                game_info["avg_goal_time"] = round(game_info['time']/(game_score[0] + game_score[1]), 2)
                game_info["avg_goal_time_seconds"] = round(game_info['time_seconds']/(game_score[0] + game_score[1]) , 2)
            except:
                game_info['avg_goal_time'] = 0
                game_info['avg_goal_time_seconds'] = 0
            try:
                game_info['avg_collisions_per_goal'] = (ball.info['blob_standard_collisions'] + ball.info['blob_reflect_collisions'] + ball.info['blob_warp_collisions']) / (p1_blob.info['points_from_goals'] + p2_blob.info['points_from_goals'])
            except:
                game_info['avg_collisions_per_goal'] = 0
            
            '''with open('blob_ball_results.txt', 'a') as bbr:
                bbr.write("MATCH COMPLETED: " + time.ctime(time.time()))
                bbr.write("\n")
                bbr.write("RANDOM SEED:" + str(random_seed))
                bbr.write("\n")
                bbr.write("RULESET: " + dumps(ruleset))
                bbr.write("\n")
                bbr.write("GENERAL INFO: " + dumps(game_info))
                bbr.write("\n")
                bbr.write("PLAYER 1: " + dumps(p1_blob.info))
                bbr.write("\n")
                bbr.write("PLAYER 2: " + dumps(p2_blob.info))
                bbr.write("\n")
                bbr.write("BALL: " + dumps(ball.info))
                bbr.write("\n")
                bbr.write("\n")
                '''
            if(is_replay == False):
                replay_inputs.append("")
                #print(game_info['time'], len(replay_inputs))
                save_replay(random_seed, ruleset, replay_inputs, p1_blob, p2_blob, game_info)
                update_game_stats(game_info, p1_blob, p2_blob, ball)
                update_mu_chart(game_score, p1_blob, p2_blob)
            else:
                game_state = "replay_win"                   
            clear_particle_memory()
            return game_state, [blob_dict, ball_dict, game_score, timer, game_state, (winner_info, p1_blob, p2_blob, ball, game_score, game_info['time_seconds'])]
    return game_state, [blob_dict, ball_dict, game_score, timer,  time_limit] # TODO: Fix/Parity the Output

def clear_info_cache():
    global game_score
    global timer
    global countdown
    global time_limit
    global game_info
    global initialized
    global p1_blob
    global p2_blob
    global p1_ko
    global p2_ko
    global ball
    global goal_scored
    global replay_inputs
    game_score = [0, 0]
    timer = 180
    countdown = 0
    time_limit = 3600
    game_info['time'] = 0
    initialized = False
    p1_blob = None
    p2_blob = None
    p1_ko = False
    p2_ko = False
    goal_scored = False
    ball = None
    replay_inputs = []
    clear_environmental_modifiers(true_reset=True)