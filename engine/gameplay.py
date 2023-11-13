import pygame as pg
import sys
from engine.environmental_modifiers import clear_environmental_modifiers, return_environmental_modifiers, update_environmental_modifiers
import engine.handle_input
import engine.blobs
import engine.ball
from engine.game_mode_flags import return_game_mode
import time
from json import dumps, loads
from engine.endgame import update_game_stats, update_mu_chart
from engine.replays import return_replay_info, save_replay
from resources.graphics_engine.display_graphics import capture_screen
from resources.graphics_engine.display_gameplay import return_image_cache
import engine.cpu_logic
import random
from engine.get_random_blob import get_random_blob
from resources.graphics_engine.display_particles import clear_particle_memory
from resources.sound_engine.sfx_event import createSFXEvent
random_seed = None
squad_dict = {}
def initialize_players(player_info, ruleset, settings, set_seed = None):
    global random_seed
    if(set_seed == None):
        random_seed = random.randint(-2147483648, 2147483647)
    else:
        random_seed = set_seed
    random.seed(random_seed)
    global goal_limit
    global time_limit
    global time_bonus
    global squad_dict
    blob_dict = {}
    ball_dict = {}
    squad_dict = {}
    for player_menu in player_info:
        dir_facing = 'right'
        x_pos = 100
        if(player_menu == 2):
            dir_facing = 'left'
            x_pos = 1600
        selected_blob = player_info[player_menu].token.current_blob
        if(selected_blob == 'random'):
            selected_blob = get_random_blob()
        blob_dict[player_menu] = engine.blobs.Blob(species = selected_blob, player = player_menu, x_pos = x_pos, facing = dir_facing, special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'], is_cpu = (player_info[player_menu].token.current_blob == 'cpu'), stat_overrides = ruleset['p1_modifiers'], costume = player_info[player_menu].token.current_costume)
        if(return_game_mode() == "squadball"):
            squad_dict[player_menu] = {}
            blob_count = 0
            for blob in player_info[player_menu].menu.stored_blobs:
                selected_blob = blob['blob']
                if(selected_blob == 'random'):
                    selected_blob = get_random_blob()
                squad_dict[player_menu][blob_count] = engine.blobs.Blob(species = selected_blob, player = player_menu, x_pos = x_pos, facing = dir_facing, special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'], is_cpu = (player_info[player_menu].token.current_blob == 'cpu'), stat_overrides = ruleset['p1_modifiers'], costume = blob['costume'])
                squad_dict[player_menu][blob_count].max_hp //= 2
                squad_dict[player_menu][blob_count].hp //= 2
                blob_count += 1
            blob_dict[player_menu] = squad_dict[player_menu][0]
        if(player_menu == 2):
            break
    ball = engine.ball.Ball()
    goal_limit = ruleset['goal_limit']
    if(ruleset['time_limit'] == 0):
        time_limit = "NO LIMIT"
    else:
        time_limit = ruleset['time_limit']
    time_bonus = ruleset['time_bonus']
    ball_dict = {
            0: ball
        } 
    if(return_game_mode() == "classic"):
        for blob in blob_dict:
            blob_dict[blob].all_blobs = blob_dict
        for ball in ball_dict:
            ball_dict[ball].all_blobs = blob_dict 
    elif(return_game_mode() == "squadball"):
        for squad in squad_dict:
            for blob in squad_dict[squad]:
                squad_dict[squad][blob].all_blobs = blob_dict
        for ball in ball_dict:
            ball_dict[ball].all_blobs = blob_dict 
    return blob_dict, ball_dict

initialized = False
p1_blob = None
p2_blob = None
p1_squad_number = 0
p2_squad_number = 0
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

def reset_round(ruleset, player = None):
    global blob_dict
    global ball_dict
    global squad_dict
    global p1_ko
    global p2_ko
    for blob in blob_dict:
        blob_dict[blob].reset(ruleset)
    #p1_blob.reset(ruleset)
    #p2_blob.reset(ruleset)
    if(return_game_mode() == "squadball"):
        update_squad(player)
    ball_dict[0].reset()
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

def update_squad(player):
    global blob_dict
    global squad_dict
    global p1_squad_number
    global p2_squad_number
    print(squad_dict)
    other_player = 1 if player == 2 else 2 # TODO: Write nicer code
    if(player == 1):
        p1_squad_number += 1
        if(p1_squad_number >= len(squad_dict[player])):
            p1_squad_number = 0
        squad_number = p1_squad_number
    if(player == 2):
        p2_squad_number += 1
        if(p2_squad_number >= len(squad_dict[player])):
            p2_squad_number = 0
        squad_number = p2_squad_number
    print(blob_dict[player])
    blob_dict[player] = squad_dict[player][squad_number]
    blob_dict[other_player].kick_cooldown -= blob_dict[other_player].kick_cooldown_max//3
    if(blob_dict[other_player].kick_cooldown <= 0):
        blob_dict[other_player].kick_cooldown = 0
        blob_dict[other_player].recharge_indicators['kick'] = 1
    blob_dict[other_player].block_cooldown -= blob_dict[other_player].block_cooldown_max//3
    if(blob_dict[other_player].block_cooldown <= 0):
        blob_dict[other_player].block_cooldown = 0
        blob_dict[other_player].recharge_indicators['block'] = 1
    blob_dict[other_player].boost_cooldown_timer -= blob_dict[other_player].boost_cooldown_max//3
    if(blob_dict[other_player].boost_cooldown_timer <= 0):
        blob_dict[other_player].boost_cooldown_timer = 0
        blob_dict[other_player].recharge_indicators['boost'] = 1
    blob_dict[other_player].special_ability_cooldown -= blob_dict[other_player].special_ability_cooldown_max//3
    if(blob_dict[other_player].special_ability_cooldown <= 0):
        blob_dict[other_player].special_ability_cooldown = 0
        blob_dict[other_player].recharge_indicators['ability'] = 1
    #print(blob_dict[player])
    image_cache = return_image_cache()
    image_cache['initialized'] = False
    image_cache['ui_initialized'] = False


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
    global blob_dict
    global ball_dict
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
    global p1_squad_number
    global p2_squad_number
    
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
        if(is_replay): #TODO: Change the replay format to support the new gameplay.py
            blob_dict, ball_dict = initialize_players(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu, p1_costume=p1_costume, p2_costume=p2_costume, set_seed = return_replay_info()[0])
        else:
            blob_dict, ball_dict = initialize_players(player_info, ruleset, settings)
        initialized = True

    else:
        if(timer == 0):
            movement_string = ""
            '''if(p1_blob.is_cpu): # TODO: Handle CPU Logic later
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
            '''
            for blob in blob_dict:
                movement_string += convert_inputs_to_replay(blob_dict[blob].move(pressed), blob)

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
            if(blob_dict[2].hp <= 0):
                    timer = 120
                    p2_ko = True
                    blob_dict[1].cooldown()
                    blob_dict[1].info['points_from_kos'] += 1
                    blob_dict[2].damage_flash_timer = 0
            
            if(blob_dict[1].hp <= 0):
                    timer = 120
                    p1_ko = True
                    blob_dict[2].cooldown()
                    blob_dict[2].info['points_from_kos'] += 1
                    blob_dict[1].damage_flash_timer = 0

            for blob in blob_dict.values():
                blob.cooldown()

            for sball in ball_dict.values():
                sball.move()
                sball.check_blob_collisions()
                
            # TODO: Figure out how to handle goals
            for ball in ball_dict.values():
                if(ball.x_pos < 60 and ball.y_pos > 925): #Left Goal
                    createSFXEvent('goal')
                    goal_scorer = 1
                    goal_scored = True
                    countdown = 60
                    timer = 60
                    #p2_blob.info['points_from_goals'] += 1
                    blob_dict[2].info['points_from_goals'] += 1
                    
                elif(ball.x_pos > 1745 and ball.y_pos > 925): #Right Goal
                    createSFXEvent('goal')            
                    goal_scorer = 0
                    goal_scored = True
                    countdown = 60
                    timer = 60
                    #p1_blob.info['points_from_goals'] += 1
                    blob_dict[1].info['points_from_goals'] += 1
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
                blob_ko(blob_dict[1])
                if(blob_dict[1].y_pos >= 1800):
                    game_state, winner_info = score_goal(1, goal_limit, ruleset, is_replay)
                    p1_ko = False
                    blob_dict[1].hp = blob_dict[1].max_hp
                    reset_round(ruleset, player=2)

            elif(p2_ko and not p1_ko):
                blob_ko(blob_dict[2])
                if(blob_dict[2].y_pos >= 1800):
                    game_state, winner_info = score_goal(0, goal_limit, ruleset, is_replay)
                    blob_dict[2].hp = blob_dict[2].max_hp
                    p2_ko = False
                    reset_round(ruleset, player=1)
            elif(p1_ko and p2_ko):
                blob_ko(blob_dict[1])
                blob_ko(blob_dict[2])
                if(p1_blob.y_pos >= 1800 or blob_dict[2].y_pos >= 1800):
                    game_state, winner_info = score_goal(1, goal_limit, ruleset, is_replay)
                    game_state, winner_info = score_goal(0, goal_limit, ruleset, is_replay)
                    p1_ko, p2_ko = False, False
                    blob_dict[1].hp = blob_dict[1].max_hp
                    blob_dict[2].hp = blob_dict[2].max_hp
                    reset_round(ruleset, player=1)
                    reset_round(ruleset, player=2)

            if(goal_scored):
                ball_dict[0].image = engine.ball.type_to_image("goal_ball")
                ball_dict[0].special_timer = 2
                ball_dict[0].move()
                for blob in blob_dict.values():
                    blob.move([])
                    blob.impact_land_frames = 0
                    blob.used_ability = {}
                countdown -= 1
                if(countdown == 0):
                    game_state, winner_info = score_goal(goal_scorer, goal_limit, ruleset, is_replay)
                    goal_scored = False
                    print(goal_scorer)
                    team_update = goal_scorer+1
                    goal_scorer = None
                    reset_round(ruleset, player=team_update)
                    
            timer -= 1
            if timer == 0:
                for blob in blob_dict.values():
                    blob.heal_hp(ruleset['hp_regen'])


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
                #game_info['avg_collisions_per_goal'] = (ball.info['blob_standard_collisions'] + ball.info['blob_reflect_collisions'] + ball.info['blob_warp_collisions']) / (p1_blob.info['points_from_goals'] + p2_blob.info['points_from_goals'])
                pass
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
                if(return_game_mode() != "squadball"):
                    save_replay(random_seed, ruleset, replay_inputs, p1_blob, p2_blob, game_info)
                    update_game_stats(game_info, p1_blob, p2_blob, ball)
                    update_mu_chart(game_score, p1_blob, p2_blob)
            else:
                game_state = "replay_win"                   
            clear_particle_memory()
            # How did we end up with such an ugly structure?
            return game_state, [blob_dict, ball_dict, game_score, timer, game_state, (return_game_mode(), winner_info, player_info, ball_dict, game_score, game_info['time_seconds'], squad_dict)]
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